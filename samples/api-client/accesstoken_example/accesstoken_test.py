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

# Generate gcp access token, use gcp access token to create gcs bucket
# upload data to gcs bucket, download data from gcs bucket
# delete data from gcs bucket
def test_generate_gcp_jwt_token_gcs():
    device_id = device_id_template.format(uuid.uuid4())
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
    accesstoken.access_token_gcs(
        cloud_region,
        project_id,
        registry_id,
        device_id,
        scope,
        "RS256",
        rsa_private_path,
        gcs_bucket_name,
    )
    # Delete device
    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )
    # Delete registry
    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)


# Generate gcp access token, use gcp access token to create pubsub
def test_access_token_pubsub():
    device_id = device_id_template.format(uuid.uuid4())
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
    accesstoken.access_token_pubsub(
        cloud_region,
        project_id,
        registry_id,
        device_id,
        scope,
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


# Generate gcp access token, exchange ubermint token for service account access token
# Use service account access token to send cloud iot command
def test_exchange_gcp_token_for_service_account_token():
    device_id = device_id_template.format(uuid.uuid4())
    scope = "https://www.googleapis.com/auth/cloud-platform"
    service_account_email = (
        "cloud-iot-test@python-docs-samples-tests.iam.gserviceaccount.com"
    )
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
    accesstoken.access_token_iot_send_command(
        cloud_region,
        project_id,
        registry_id,
        device_id,
        scope,
        "RS256",
        rsa_private_path,
        service_account_email,
    )

    # Delete device
    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )
    # Delete registry
    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)
