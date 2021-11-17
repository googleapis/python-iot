# Copyright 2021 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import os
import sys
import time
import uuid

import pytest

# Add command receiver for bootstrapping device registry / device for testing

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "manager"))  # noqa
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "mqtt_example"))  # noqa

import cloudiot_mqtt_example  # noqa
import manager  # noqa

import accesstoken  # noqa

cloud_region = "us-central1"
device_id_template = "test-device-256-{}"
rsa_cert_path = "resources/rsa_cert.pem"
rsa_private_path = "resources/rsa_private.pem"  # Must match rsa_cert
device_topic_id = "test-device-events-{}".format(uuid.uuid4())
gcs_bucket_name = "test-bucket-name-{}".format(uuid.uuid4())
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
service_account_json = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
device_pubsub_topic = "projects/{}/topics/{}".format(project_id, device_topic_id)
test_topic_id = "test-pubsub-{}".format(uuid.uuid4())

# This format is used in the `clean_up_registries()` below.
registry_id = "test-registry-{}-{}".format(uuid.uuid4().hex, int(time.time()))


@pytest.fixture(scope="session", autouse=True)
def clean_up_registries():
    all_registries = list(
        manager.list_registries(service_account_json, project_id, cloud_region)
    )

    for registry in all_registries:
        registry_id = registry.id
        if registry_id.find("test-registry-") == 0:
            time_str = registry_id[registry_id.rfind("-") + 1 : len(registry_id)]
            try:
                test_date = datetime.datetime.utcfromtimestamp(int(time_str))
            except ValueError:
                # skip incorrect formatted registry
                continue
            now_date = datetime.datetime.utcfromtimestamp(int(time.time()))
            difftime = now_date - test_date

            # *NOTE* Restrict to registries used in the tests older than 30
            #        days to prevent thrashing in the case of async tests
            if difftime.days > 30:
                client = manager.get_client(service_account_json)
                gateways = (
                    client.projects()
                    .locations()
                    .registries()
                    .devices()
                    .list(parent=registry.name, fieldMask="config,gatewayConfig")
                    .execute()
                    .get("devices", [])
                )
                devices = (
                    client.projects()
                    .locations()
                    .registries()
                    .devices()
                    .list(parent=registry.name)
                    .execute()
                    .get("devices", [])
                )

                # Unbind devices from each gateway and delete
                for gateway in gateways:
                    gateway_id = gateway.get("id")
                    bound = (
                        client.projects()
                        .locations()
                        .registries()
                        .devices()
                        .list(
                            parent=registry.name,
                            gatewayListOptions_associationsGatewayId=gateway_id,
                        )
                        .execute()
                    )
                    if "devices" in bound:
                        for device in bound["devices"]:
                            bind_request = {
                                "deviceId": device.get("id"),
                                "gatewayId": gateway_id,
                            }
                            client.projects().locations().registries().unbindDeviceFromGateway(
                                parent=registry.get("name"), body=bind_request
                            ).execute()
                    gateway_name = "{}/devices/{}".format(registry.name, gateway_id)
                    client.projects().locations().registries().devices().delete(
                        name=gateway_name
                    ).execute()

                # Delete the devices
                # Assumption is that the devices are not bound to gateways
                for device in devices:
                    device_name = "{}/devices/{}".format(
                        registry.name, device.get("id")
                    )
                    print(device_name)
                    remove_device = True
                    try:
                        client.projects().locations().registries().devices().get(
                            name=device_name
                        ).execute()
                    except Exception:
                        remove_device = False

                    if remove_device:
                        print("removing  ggg{}".format(device_name))
                        client.projects().locations().registries().devices().delete(
                            name=device_name
                        ).execute()

                # Delete the old test registry
                client.projects().locations().registries().delete(
                    name=registry.name
                ).execute()


# Generate device access token, use device access token to create pubsub topic,
# publish message to pubsub.
def test_publish_pubsub_message():
    device_id = device_id_template.format(uuid.uuid4())
    manager.open_registry(
        service_account_json, project_id, cloud_region, device_pubsub_topic, registry_id
    )

    manager.create_rs256_device(
        service_account_json,
        project_id,
        cloud_region,
        registry_id,
        device_id,
        rsa_cert_path,
    )
    accesstoken.publish_pubsub_message(
        cloud_region,
        project_id,
        registry_id,
        device_id,
        "RS256",
        rsa_private_path,
        test_topic_id,
    )

    # Delete device
    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )
    # Delete registry
    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)


# Generate device access token, use access token to create GCS bucket,
# upload a file to bucket, download file from bucket
def test_download_cloud_storage_file():
    device_id = device_id_template.format(uuid.uuid4())
    data_path = "./resources/logo.png"

    manager.open_registry(
        service_account_json, project_id, cloud_region, device_pubsub_topic, registry_id
    )

    manager.create_rs256_device(
        service_account_json,
        project_id,
        cloud_region,
        registry_id,
        device_id,
        rsa_cert_path,
    )
    accesstoken.download_cloud_storage_file(
        cloud_region,
        project_id,
        registry_id,
        device_id,
        "RS256",
        rsa_private_path,
        gcs_bucket_name,
        data_path,
    )
    # Delete device
    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )
    # Delete registry
    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)


# Generate device access token, exchange device access token for service account access token,
# use service account access token to send cloud iot device command
def test_send_iot_command_to_device():
    device_id = device_id_template.format(uuid.uuid4())
    service_account_email = (
        "cloud-iot-test@python-docs-samples-tests.iam.gserviceaccount.com"
    )
    command_to_be_sent_to_device = "OPEN_DOOR"
    manager.open_registry(
        service_account_json, project_id, cloud_region, device_pubsub_topic, registry_id
    )

    manager.create_rs256_device(
        service_account_json,
        project_id,
        cloud_region,
        registry_id,
        device_id,
        rsa_cert_path,
    )
    # Create device MQTT client and connect to cloud iot mqtt bridge.
    mqtt_bridge_hostname = "mqtt.googleapis.com"
    mqtt_bridge_port = 8883
    mqtt_tls_cert = "resources/roots.pem"
    client = cloudiot_mqtt_example.get_client(
        project_id,
        cloud_region,
        registry_id,
        device_id,
        rsa_private_path,
        "RS256",
        mqtt_tls_cert,
        mqtt_bridge_hostname,
        mqtt_bridge_port,
    )
    accesstoken.send_iot_command_to_device(
        cloud_region,
        project_id,
        registry_id,
        device_id,
        "RS256",
        rsa_private_path,
        service_account_email,
        command_to_be_sent_to_device,
    )

    client.disconnect()
    # Delete device
    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )
    # Delete registry
    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)
