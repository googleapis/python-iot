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

from google.cloud import pubsub_v1
from google.cloud import storage
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

# Generate gcp access token, use gcp access token to enable pubsub notification
#  from gcs bucket


def test_generate_gcp_jwt_token_():
    device_id = device_id_template.format("RSA256")
    scope = "https://www.googleapis.com/auth/pubsub https://www.googleapis.com/auth/devstorage.full_control'"
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
    # Create GCS Bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket_name)
    bucket.storage_class = "COLDLINE"
    new_bucket = storage_client.create_bucket(bucket, location=cloud_region)

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )

    # Create GCP PubSub
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, test_topic_id)

    publisher.create_topic({"name": topic_path})

    token = accesstoken.generate_gcp_token(
        project_id,
        cloud_region,
        registry_id,
        device_id,
        scope,
        "RS256",
        rsa_private_path,
    )
    payload = {"topic": topic_path, "payload_format": "JSON_API_V1"}
    request_path = (
        "https://storage.googleapis.com/storage/v1/b/{}/notificationConfigs".format(
            gcs_bucket_name
        )
    )
    headers = {"authorization": "Bearer {}".format(token)}
    resp = req.post(url=request_path, data=payload, headers=headers)
    print(resp.raise_for_status())

    assert resp.ok

    # clean up

    publisher.delete_topic(request={"topic": topic_path})

    new_bucket.delete()
    print("Bucket {} deleted".format(gcs_bucket_name))

    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)
    return token
