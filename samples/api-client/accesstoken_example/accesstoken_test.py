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

import os
import sys
import time
import uuid

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
