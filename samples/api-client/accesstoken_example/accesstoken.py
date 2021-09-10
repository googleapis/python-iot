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
Example of using the Google Cloud IoT Core access_token to generate
gcp compatible token.

Usage example:

    python accesstoken.py \\
      --project_id=my-project-id \\
      --cloud_region=us-central1 \\
      --registry_id=my-registry-id \\
      --device_id=my-device-id \\
      --certificate_path=/my-certificate.pem \\
      --scope="scope1 scope2"
"""
import argparse
import base64
from datetime import datetime, timedelta
import io
import json
import os
import time
from urllib.parse import quote


import jwt
import requests as req

HOST = "https://cloudiottoken.googleapis.com"


def access_token_pubsub(
    cloud_region,
    project_id,
    registry_id,
    device_id,
    scope,
    algorithm,
    rsa_private_key_path,
    topic_id,
):
    """Access Token pubsub"""
    # [START iot_access_token_pubsub]
    # cloud_region = 'us-central1'
    # project_id = 'YOUR_PROJECT_ID'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # scope = 'scope1 scope2' # See the full list of scopes at:
    # https://developers.google.com/identity/protocols/oauth2/scopes
    # algorithm = 'RS256'
    # rsa_private_key_path = 'path/to/certificate.pem'
    # topic_id = 'pubsub topic id'

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
    # Create pubsub topic
    request_path = "https://pubsub.googleapis.com/v1/projects/{}/topics/{}".format(
        project_id, topic_id
    )
    headers = {
        "authorization": "Bearer {}".format(token),
        "content-type": "application/json",
        "cache-control": "no-cache",
    }
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
            project_id, topic_id
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
            project_id, topic_id
        )
    )
    delete_resp = req.delete(url=pubsub_delete_request_path, headers=headers)

    print(delete_resp.raise_for_status())
    assert delete_resp.ok
    # [END iot_access_token_pubsub]


def access_token_gcs(
    cloud_region,
    project_id,
    registry_id,
    device_id,
    scope,
    algorithm,
    rsa_private_key_path,
    bucket_name,
):
    """Access Token GCS"""
    # [START iot_access_token_gcs]
    # cloud_region = 'us-central1'
    # project_id = 'YOUR_PROJECT_ID'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # scope = 'scope1 scope2' # See the full list of scopes at:
    # https://developers.google.com/identity/protocols/oauth2/scopes
    # algorithm = 'RS256'
    # rsa_private_key_path = 'path/to/certificate.pem'
    # bucket_name = 'name of gcs bucket.'

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
    binary_data = open("./resources/logo.png", "rb").read()
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

    # Clean up
    # Delete GCS Bucket
    gcs_delete_request_path = "https://storage.googleapis.com/storage/v1/b/{}".format(
        bucket_name
    )
    delete_resp = req.delete(url=gcs_delete_request_path, headers=headers)

    print(delete_resp.raise_for_status())
    assert delete_resp.ok
    # [END iot_access_token_gcs]


def access_token_iot_send_command(
    cloud_region,
    project_id,
    registry_id,
    device_id,
    scope,
    algorithm,
    rsa_private_key_path,
    service_account_email,
):
    """Access Token Iot Send Command"""
    # [START iot_access_token_iot_send_command]
    # cloud_region = 'us-central1'
    # project_id = 'YOUR_PROJECT_ID'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # scope = 'scope1 scope2' # See the full list of scopes at:
    # https://developers.google.com/identity/protocols/oauth2/scopes
    # algorithm = 'RS256'
    # rsa_private_key_path = 'path/to/certificate.pem'
    # service_account_email = 'service account to be impersonated.'

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
    headers = {
        "authorization": "Bearer {}".format(token),
        "content-type": "application/json",
        "cache-control": "no-cache",
    }
    # Exchange access token for service account access token.
    exchange_payload = {"scope": [scope]}
    exchange_url = "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/{}:generateAccessToken".format(
        quote(service_account_email)
    )
    exchange_resp = req.post(url=exchange_url, data=exchange_payload, headers=headers)
    print(exchange_resp.request.url)
    print(exchange_resp.request.body)
    print(exchange_resp.request.headers)
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
        headers={
            "authorization": "Bearer {}".format(service_account_token),
            "content-type": "application/json",
            "cache-control": "no-cache",
        },
    )

    print(command_resp.raise_for_status())
    assert command_resp.ok
    # [END iot_access_token_iot_send_command]


def generate_access_token(
    project_id, cloud_region, registry_id, device_id, scope, algorithm, certificate_file
):
    """Generate GCP access token."""
    # [START iot_generate_access_token]
    # project_id = 'YOUR_PROJECT_ID'
    # cloud_region = 'us-central1'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # scope = 'scope1 scope2' # See the full list of scopes at:
    # https://developers.google.com/identity/protocols/oauth2/scopes
    # algorithm = 'RS256'
    # certificate_file = 'path/to/certificate.pem'

    jwt_token = generate_iot_jwt_token(project_id, algorithm, certificate_file)
    token = exchange_iot_jwt_token_with_gcp_token(
        cloud_region, project_id, registry_id, device_id, jwt_token, scope
    )
    return token
    # [END iot_generate_access_token]


def generate_iot_jwt_token(project_id, algorithm, path_to_private_certificate):
    """Generate cloud iot jwt token."""
    # [START iot_generate_iot_jwt_token]
    # project_id = 'YOUR_PROJECT_ID'
    # algorithm = 'RS256'
    # certificate_file = 'path/to/certificate.pem'
    jwt_payload = '{{"iat":{},"exp":{},"aud":"{}"}}'.format(
        time.time(),
        time.mktime((datetime.now() + timedelta(hours=6)).timetuple()),
        project_id,
    )
    private_key_bytes = ""
    with io.open(path_to_private_certificate) as f:
        private_key_bytes = f.read()
    encoded_jwt = jwt.encode(
        json.loads(jwt_payload), private_key_bytes, algorithm=algorithm
    )
    return encoded_jwt
    # [END iot_generate_iot_jwt_token]


def exchange_iot_jwt_token_with_gcp_token(
    cloud_region, project_id, registry_id, device_id, jwt_token, scopes
):
    """Exchange iot jwt token for gcp token."""
    # [START iot_exchange_iot_jwt_token_with_gcp_token]
    # cloud_region = 'us-central1'
    # project_id = 'YOUR_PROJECT_ID'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # jwt_token = 'CLOUD_IOT_GENERATE_JWT_TOKEN'
    # scopes = 'scope1 scope2' # See the full list of scopes at:
    # https://developers.google.com/identity/protocols/oauth2/scopes
    global HOST
    resource_url = "projects/{}/locations/{}/registries/{}/devices/{}".format(
        project_id, cloud_region, registry_id, device_id
    )
    request_path = "{}/v1beta1/{}:generateAccessToken".format(HOST, resource_url)
    headers = {"authorization": "Bearer {}".format(jwt_token)}
    request_payload = {"scope": scopes, "device": resource_url}
    resp = req.post(url=request_path, data=request_payload, headers=headers)
    print(resp.raise_for_status())
    return resp.json()["access_token"]
    # [END iot_exchange_iot_jwt_token_with_gcp_token]


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
    parser.add_argument("--certificate_path", help="Path to private certificate.")
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
    if args.certificate_path is None:
        print("You must specify a certificate file.")
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
        args.certificate_path,
    )
    print("Generated GCP compatible token: ", token)


if __name__ == "__main__":
    args = parse_command_line_args()
    run_program(args)
