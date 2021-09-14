#!/usr/bin/env python

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


"""
This sample app demonstrates the capabilites of Google Cloud IoT Core 
device federated authentication feature. For more information, see 
https://cloud.google.com/iot/alpha/docs/how-tos/federated_auth.

Usage example:

    python accesstoken.py \\
      --project_id=my-project-id \\
      --cloud_region=us-central1 \\
      --registry_id=my-registry-id \\
      --device_id=my-device-id \\
      --private_key_file=/rsa_private.pem \\
      --scope="scope1 scope2"
"""

import argparse
import base64
from datetime import datetime, timedelta
import io
import json
import os
import time
import jwt
import requests as req


def create_jwt(project_id, algorithm, private_key_file):
    """Generate Cloud IoT device jwt token."""
    jwt_payload = '{{"iat":{},"exp":{},"aud":"{}"}}'.format(
        time.time(),
        time.mktime((datetime.now() + timedelta(hours=6)).timetuple()),
        project_id,
    )
    private_key_bytes = ""
    with io.open(private_key_file) as f:
        private_key_bytes = f.read()
    encoded_jwt = jwt.encode(
        json.loads(jwt_payload), private_key_bytes, algorithm=algorithm
    )
    return encoded_jwt


def generate_access_token(
    project_id, cloud_region, registry_id, device_id, scope, algorithm, private_key_file
):
    """Generate device access token."""
    # [START iot_generate_access_token]
    # project_id = 'YOUR_PROJECT_ID'
    # cloud_region = 'us-central1'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # scope = 'scope1 scope2' # See the full list of scopes \
    #     at: https://developers.google.com/identity/protocols/oauth2/scopes
    # algorithm = 'RS256'
    # private_key_file = 'path/to/private_key.pem'

    def generate_device_access_token(
        cloud_region, project_id, registry_id, device_id, jwt_token, scopes
    ):
        """Exchange IoT device jwt token for device access token."""
        request_path = "https://cloudiottoken.googleapis.com/v1beta1/projects/{}/locations/{}/registries/{}/devices/{}:generateAccessToken".format(
            project_id, cloud_region, registry_id, device_id
        )
        headers = {"authorization": "Bearer {}".format(jwt_token)}
        request_payload = {"scope": scopes, "device": resource_url}
        resp = req.post(url=request_path, data=request_payload, headers=headers)
        print(resp.raise_for_status())
        return resp.json()["access_token"]

    # Generate IoT device JWT. See https://cloud.google.com/iot/docs/how-tos/credentials/jwts
    jwt = create_jwt(project_id, algorithm, private_key_file)

    access_token = generate_device_access_token(
        cloud_region, project_id, registry_id, device_id, jwt, scope
    )
    return access_token
    # [END iot_generate_access_token]


def publish_pubsub_message(
    cloud_region,
    project_id,
    registry_id,
    device_id,
    scope,
    algorithm,
    rsa_private_key_path,
    topic_id,
):
    """Publish message to Cloud Pub/Sub using device access token"""
    # [START iot_access_token_pubsub]
    # cloud_region = 'us-central1'
    # project_id = 'YOUR_PROJECT_ID'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # scope = 'scope1 scope2' # See the full list of scopes \
    #     at: https://developers.google.com/identity/protocols/oauth2/scopes
    # algorithm = 'RS256'
    # rsa_private_key_path = 'path/to/private_key.pem'
    # topic_id = 'pubsub-topic-id'

    # Generate device access token
    token = generate_access_token(
        project_id,
        cloud_region,
        registry_id,
        device_id,
        scope,
        algorithm,
        rsa_private_key_path,
    )
    # Create Pub/Sub topic
    request_path = "https://pubsub.googleapis.com/v1/projects/{}/topics/{}".format(
        project_id, topic_id
    )
    headers = {
        "Authorization": "Bearer {}".format(token),
        "content-type": "application/json",
        "cache-control": "no-cache",
    }
    resp = req.put(url=request_path, data={}, headers=headers)
    print(resp.raise_for_status())
    assert resp.ok

    # Publish message to Pub/Sub topic
    publish_payload = {
        "messages": [
            {"data": str(base64.b64encode(bytes("MESSAGE_DATA", "utf-8")), "utf-8")}
        ]
    }
    publish_request_path = (
        "https://pubsub.googleapis.com/v1/projects/{}/topics/{}:publish".format(
            project_id, topic_id
        )
    )
    publish_resp = req.post(
        url=publish_request_path, data=json.dumps(publish_payload), headers=headers
    )
    print("Response: ", publish_resp.json())
    print(publish_resp.raise_for_status())
    assert publish_resp.ok

    # Delete Pub/Sub topic
    pubsub_delete_request_path = (
        "https://pubsub.googleapis.com/v1/projects/{}/topics/{}".format(
            project_id, topic_id
        )
    )
    delete_resp = req.delete(url=pubsub_delete_request_path, headers=headers)

    print(delete_resp.raise_for_status())
    assert delete_resp.ok
    # [END iot_access_token_pubsub]


def download_cloud_storage_file(
    cloud_region,
    project_id,
    registry_id,
    device_id,
    scope,
    algorithm,
    rsa_private_key_path,
    bucket_name,
    data_path,
):
    """Download a file from Cloud Storage using device access token"""
    # [START iot_access_token_gcs]
    # cloud_region = 'us-central1'
    # project_id = 'YOUR_PROJECT_ID'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # scope = 'scope1 scope2' # See the full list of scopes \
    #     at: https://developers.google.com/identity/protocols/oauth2/scopes
    # algorithm = 'RS256'
    # rsa_private_key_path = 'path/to/private_key.pem'
    # bucket_name = 'name-of-gcs-bucket'
    # data_path = 'path/to/file/to/be/uploaded.png'

    # Generate device access token
    token = generate_access_token(
        project_id,
        cloud_region,
        registry_id,
        device_id,
        scope,
        algorithm,
        rsa_private_key_path,
    )

    # Create GCS bucket
    create_payload = {
        "name": bucket_name,
        "location": cloud_region,
        "storageClass": "STANDARD",
        "iamConfiguration": {
            "uniformBucketLevelAccess": {"enabled": True},
        },
    }
    create_request_path = (
        "https://storage.googleapis.com/storage/v1/b?project={}".format(project_id)
    )
    headers = {
        "authorization": "Bearer {}".format(token),
        "content-type": "application/json",
        "cache-control": "no-cache",
    }
    create_resp = req.post(
        url=create_request_path,
        data=bytes(json.dumps(create_payload), "utf-8"),
        headers=headers,
    )
    print(create_resp.raise_for_status())
    assert create_resp.ok

    # Upload data to GCS bucket.
    data_name = "testFILE"
    binary_data = open(data_path, "rb").read()
    upload_request_path = "https://storage.googleapis.com/upload/storage/v1/b/{}/o?uploadType=media&name={}".format(
        bucket_name, data_name
    )
    upload_resp = req.post(url=upload_request_path, data=binary_data, headers=headers)

    print(upload_resp.raise_for_status())
    assert upload_resp.ok

    # Download data from GCS bucket.
    download_request_path = (
        "https://storage.googleapis.com/storage/v1/b/{}/o/{}?alt=media".format(
            bucket_name, data_name
        )
    )
    download_resp = req.get(url=download_request_path, headers=headers)

    print(download_resp.raise_for_status())
    assert download_resp.ok

    # Delete data from GCS bucket.
    delete_request_path = "https://storage.googleapis.com/storage/v1/b/{}/o/{}".format(
        bucket_name, data_name
    )
    delete_data_resp = req.delete(url=delete_request_path, headers=headers)

    print(delete_data_resp.raise_for_status())
    assert delete_data_resp.ok

    # Delete GCS Bucket
    gcs_delete_request_path = "https://storage.googleapis.com/storage/v1/b/{}".format(
        bucket_name
    )
    delete_resp = req.delete(url=gcs_delete_request_path, headers=headers)

    print(delete_resp.raise_for_status())
    assert delete_resp.ok
    # [END iot_access_token_gcs]


def exchange_device_access_token_for_service_account_access_token(
    device_access_token, scope, service_account_email
):
    # [START iot_access_token_service_account_token]
    # device_access_token = 'device-access-token'
    # scope = 'scope1 scope2' # See the full list of scopes \
    #     at: https://developers.google.com/identity/protocols/oauth2/scopes
    # service_account_email  = 'your-service-account@your-project.iam.gserviceaccount.com'
    headers = {
        "Authorization": "Bearer {}".format(device_access_token),
        "content-type": "application/json",
        "cache-control": "no-cache",
    }
    # Exchange access token for service account access token.
    exchange_payload = {"scope": [scope]}
    exchange_url = "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/{}:generateAccessToken".format(
        service_account_email
    )
    exchange_resp = req.post(
        url=exchange_url, data=json.dumps(exchange_payload), headers=headers
    )
    print(exchange_resp.raise_for_status())
    assert exchange_resp.ok

    service_account_token = exchange_resp.json()["accessToken"]
    return service_account_token
    # [END iot_access_token_service_account_token]


def send_iot_command_to_device(
    cloud_region,
    project_id,
    registry_id,
    device_id,
    scope,
    algorithm,
    rsa_private_key_path,
    service_account_email,
    command_to_be_sent_to_device,
):
    """Send command to an Cloud IoT device using access token"""
    # [START iot_access_token_iot_send_command]
    # cloud_region = 'us-central1'
    # project_id = 'YOUR_PROJECT_ID'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # scope = 'scope1 scope2' # See the full list of scopes \
    #     at: https://developers.google.com/identity/protocols/oauth2/scopes
    # algorithm = 'RS256'
    # rsa_private_key_path = 'path/to/private_key.pem'
    # service_account_email = 'your-service-account@your-project.iam.gserviceaccount.com'
    # command_to_be_sent_to_device = 'command-to-device'

    # Generate GCP access token
    token = generate_access_token(
        project_id,
        cloud_region,
        registry_id,
        device_id,
        scope,
        algorithm,
        rsa_private_key_path,
    )
    service_account_token = (
        exchange_device_access_token_for_service_account_access_token(
            token, scope, service_account_email
        )
    )
    # Sending a command to a Cloud IoT Core device
    command_payload = json.dumps(
        {
            "binaryData": str(
                base64.b64encode(bytes(command_to_be_sent_to_device, "utf-8")), "utf-8"
            )
        }
    )
    command_url = "https://cloudiot.googleapis.com/v1/projects/{}/locations/{}/registries/{}/devices/{}:sendCommandToDevice".format(
        project_id, cloud_region, registry_id, device_id
    )
    command_resp = req.post(
        url=command_url,
        data=command_payload,
        headers={
            "authorization": "Bearer {}".format(service_account_token),
            "content-type": "application/json",
            "cache-control": "no-cache",
        },
    )
    print("Response: ", command_resp.json())
    print(command_resp.raise_for_status())
    assert command_resp.ok
    # [END iot_access_token_iot_send_command]


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--algorithm",
        default="RS256",
        choices=("RS256", "ES256"),
        help="Which encryption algorithm to use to generate the JWT.",
    )
    parser.add_argument("--private_key_file", help="Path to private key file.")
    parser.add_argument(
        "--cloud_region", default="us-central1", help="GCP cloud region"
    )

    parser.add_argument("--device_id", default=None, help="Device id.")
    parser.add_argument(
        "--scope",
        default=None,
        help="Scope for GCP token. Space delimited strings. See the full list of scopes at: https://developers.google.com/identity/protocols/oauth2/scopes",
    )

    parser.add_argument(
        "--project_id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        help="GCP cloud project name.",
    )
    parser.add_argument(
        "--registry_id",
        default=None,
        help="Registry id. If not set, a name will be generated.",
    )
    return parser.parse_args()


def run_program(args):
    """Calls the program."""
    if args.registry_id is None:
        print("You must specify a registry ID.")
        return
    if args.project_id is None:
        print("You must specify a project ID or set the environment variable.")
        return
    if args.device_id is None:
        print("You must specify a device ID.")
    if args.private_key_file is None:
        print("You must specify a private key file.")
        return
    if args.scope is None:
        print("You must specify the scope.")
        return
    token = generate_access_token(
        args.project_id,
        args.cloud_region,
        args.registry_id,
        args.device_id,
        args.scope,
        args.algorithm,
        args.private_key_file,
    )
    print("Generated GCP compatible token: ", token)


if __name__ == "__main__":
    args = parse_command_line_args()
    run_program(args)
