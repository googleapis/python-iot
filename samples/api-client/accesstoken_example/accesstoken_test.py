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

import base64
import os
import sys
import time
import uuid

import requests as req

# Add command receiver for bootstrapping device registry / device for testing

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "manager"))  # noqa

import manager  # noqa

import accesstoken  # noqa

cloud_region = "us-central1"
device_id_template = "test-device-{}"
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

# Generate gcp access token, use gcp access token to create pubsub


def test_generate_gcp_jwt_token_pubsub():
    device_id = device_id_template.format("RSA256")
    scope = "https://www.googleapis.com/auth/pubsub"
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
    # Generate GCP access token
    token = accesstoken.generate_gcp_token(
        project_id,
        cloud_region,
        registry_id,
        device_id,
        scope,
        "RS256",
        rsa_private_path,
    )

    # Create pubsub topic
    request_path = "https://pubsub.googleapis.com/v1/projects/{}/topics/{}".format(
        project_id, test_topic_id
    )
    headers = {"authorization": "Bearer {}".format(token)}
    resp = req.put(url=request_path, data={}, headers=headers)

    print(resp.raise_for_status())
    assert resp.ok

    # Publish messgae to pubsub topic
    publish_payload = {
        "messages": [
            {
                "attributes": {
                    "test": "VALUE",
                },
                "data": base64.b64encode(bytes("MESSAGE_DATA", "utf-8")),
            }
        ]
    }
    publish_request_path = (
        "https://pubsub.googleapis.com/v1/projects/{}/topics/{}:publish".format(
            project_id, test_topic_id
        )
    )
    publish_resp = req.post(
        url=publish_request_path, data=publish_payload, headers=headers
    )

    print(publish_resp.raise_for_status())
    assert publish_resp.ok
    # Clean up

    # Delete Pubsub topic
    pubsub_delete_request_path = (
        "https://pubsub.googleapis.com/v1/projects/{}/topics/{}".format(
            project_id, test_topic_id
        )
    )
    delete_resp = req.delete(url=pubsub_delete_request_path, headers=headers)

    print(delete_resp.raise_for_status())
    assert delete_resp.ok

    # Delete device
    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )
    # Delete registry
    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)


# Generate gcp access token, use gcp access token to create gcs bucket
# upload data to gcs bucket, download data from gcs bucket
# delete data from gcs bucket
def test_generate_gcp_jwt_token_gcs():
    device_id = device_id_template.format("RSA256")
    scope = "https://www.googleapis.com/auth/devstorage.full_control"
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
    # Generate GCP access token
    token = accesstoken.generate_gcp_token(
        project_id,
        cloud_region,
        registry_id,
        device_id,
        scope,
        "RS256",
        rsa_private_path,
    )

    # Create GCS bucket
    create_payload = {
        "name": gcs_bucket_name,
        "location": cloud_region,
        "storageClass": "STANDARD",
        "iamConfiguration": {
            "uniformBucketLevelAccess": {"enabled": True},
        },
    }
    create_request_path = (
        "https://storage.googleapis.com/storage/v1/b?project={}".format(project_id)
    )
    headers = {"authorization": "Bearer {}".format(token)}
    create_resp = req.post(
        url=create_request_path, data=create_payload, headers=headers
    )

    print(create_resp.raise_for_status())
    assert create_resp.ok

    # Upload data to GCS bucket.
    data_name = "testFILE"
    binary_data = open("./resources/logo.png", "r").read()
    upload_request_path = "https://storage.googleapis.com/upload/storage/v1/b/{}/o?uploadType=media&name={}".format(
        gcs_bucket_name, data_name
    )
    upload_resp = req.post(url=upload_request_path, data=binary_data, headers=headers)

    print(upload_resp.raise_for_status())
    assert upload_resp.ok

    # Download data from GCS bucket.
    download_request_path = (
        "https://storage.googleapis.com/storage/v1/b/${}/o/${}?alt=media".format(
            gcs_bucket_name, data_name
        )
    )
    download_resp = req.get(url=download_request_path, headers=headers)

    print(download_resp.raise_for_status())
    assert download_resp.ok

    # Delete data from GCS bucket.
    delete_request_path = (
        "https://storage.googleapis.com/storage/v1/b/${}/o/${}".format(
            gcs_bucket_name, data_name
        )
    )
    delete_data_resp = req.delete(url=delete_request_path, headers=headers)

    print(delete_data_resp.raise_for_status())
    assert delete_data_resp.ok

    # Clean up
    # Delete GCS Bucket
    gcs_delete_request_path = "https://storage.googleapis.com/storage/v1/b/{}".format(
        create_resp.json().name
    )
    delete_resp = req.delete(url=gcs_delete_request_path, headers=headers)

    print(delete_resp.raise_for_status())
    assert delete_resp.ok
    # Delete device
    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )
    # Delete registry
    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)


# Generate gcp access token, exchange ubermint token for service account access token
# Use service account access token to send cloud iot command
def test_exchange_gcsp_token_for_service_account_token():
    device_id = device_id_template.format("RSA256")
    scope = "https://www.googleapis.com/auth/cloud-platform"
    service_account_email = ""
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
    # Generate GCP access token
    token = accesstoken.generate_gcp_token(
        project_id,
        cloud_region,
        registry_id,
        device_id,
        scope,
        "RS256",
        rsa_private_path,
    )
    headers = {"authorization": "Bearer {}".format(token)}
    # Exchange uber mint token for service account access token.
    exchange_payload = {"scope": [scope]}
    exchange_url = "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/{}:generateAccessToken".format(
        service_account_email
    )
    exchange_resp = req.post(url=exchange_url, data=exchange_payload, headers=headers)
    print(exchange_resp.raise_for_status())

    assert exchange_resp.ok
    assert exchange_resp.json["accessToken"] != ""

    service_account_token = exchange_resp.json["accessToken"]

    # Sending a command to a Cloud IoT Core device
    command_payload = {"binaryData": bytes("CLOSE DOOR", "utf-8")}
    command_url = "https://cloudiot.googleapis.com/v1/projects/{}/locations/{}/registries/{}/devices/{}:sendCommandToDevice".format(
        project_id, cloud_region, registry_id, device_id
    )
    command_resp = req.post(
        url=command_url,
        data=command_payload,
        headers={"authorization": "Bearer {}".format(service_account_token)},
    )

    print(command_resp.raise_for_status())
    assert command_resp.ok
