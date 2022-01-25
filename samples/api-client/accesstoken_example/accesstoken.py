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
This sample app demonstrates the capabilites of Google Cloud IoT Core device federated authentication feature.
Devices authenticated to Cloud IoT Core can use the [Token Service](https://cloud.google.com/iot/alpha/docs/reference/cloudiottoken/rest) federated authentication to request [OAuth 2.0 access tokens](https://developers.google.com/identity/protocols/oauth2) in exchange for their [Cloud IoT Core JWTs](https://cloud.google.com/iot/docs/how-tos/credentials/jwts).
The OAuth 2.0 credentials can be used to call different [Google Cloud APIs](https://developers.google.com/identity/protocols/oauth2/scopes) with fine-grained permissions and access control using [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation).
For more information, see https://cloud.google.com/iot/alpha/docs/how-tos/federated_auth

Usage example:

    python accesstoken.py \\
      --project_id=my-project-id \\
      --cloud_region=us-central1 \\
      --registry_id=my-registry-id \\
      --device_id=my-device-id \\
      --private_key_file=./resources/rsa_private.pem \\
      --scope=https://www.googleapis.com/auth/cloud-platform \\
      --algorithm=RS256 \\
      generate-access-token
"""

import argparse
import base64
from datetime import datetime, timedelta
import io
import json
import os
import time

from google.cloud import pubsub
from google.cloud import storage
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
    return encoded_jwt.decode() if isinstance(encoded_jwt, bytes) else encoded_jwt


def generate_access_token(
    cloud_region, project_id, registry_id, device_id, scope, algorithm, private_key_file
):
    """Generates OAuth 2.0 Google Access Token."""
    # [START iot_generate_access_token]
    # cloud_region = 'us-central1'
    # project_id = 'YOUR_PROJECT_ID'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # scope = 'scope1 scope2' # See the full list of scopes \
    #     at: https://developers.google.com/identity/protocols/oauth2/scopes
    # algorithm = 'RS256'
    # private_key_file = 'path/to/private_key.pem'

    # Generate IoT device JWT. See https://cloud.google.com/iot/docs/how-tos/credentials/jwts
    jwt = create_jwt(project_id, algorithm, private_key_file)

    # Generate OAuth 2.0 access token. See https://developers.google.com/identity/protocols/oauth2
    resource_path = "projects/{}/locations/{}/registries/{}/devices/{}".format(
        project_id, cloud_region, registry_id, device_id
    )
    request_url = "https://cloudiottoken.googleapis.com/v1beta1/{}:generateAccessToken".format(
        resource_path
    )
    headers = {"authorization": "Bearer {}".format(jwt)}
    request_payload = {"scope": scope, "device": resource_path}
    resp = req.post(url=request_url, data=request_payload, headers=headers)
    assert resp.ok, resp.raise_for_status()
    access_token = resp.json()["access_token"]
    print("Device access token: {}".format(access_token))
    return access_token
    # [END iot_generate_access_token]


def publish_pubsub_message(
    cloud_region,
    project_id,
    registry_id,
    device_id,
    algorithm,
    rsa_private_key_path,
    topic_id,
):
    """Publishes a message to Cloud Pub/Sub topic."""
    # [START iot_access_token_pubsub]
    # cloud_region = 'us-central1'
    # project_id = 'YOUR_PROJECT_ID'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # algorithm = 'RS256'
    # rsa_private_key_path = 'path/to/private_key.pem'
    # topic_id = 'pubsub-topic-id'
    scope = "https://www.googleapis.com/auth/pubsub"

    # Generate device access token
    access_token = generate_access_token(
        cloud_region,
        project_id,
        registry_id,
        device_id,
        scope,
        algorithm,
        rsa_private_key_path,
    )

    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project_id, topic_id)
    pubsub_client.create_topic(request={"name": topic_path})
    print("Successfully created Pub/Sub topic: {}.".format(topic_id))

    headers = {
        "Authorization": "Bearer {}".format(access_token),
        "content-type": "application/json",
        "cache-control": "no-cache",
    }

    # Publish message to Pub/Sub topic
    publish_payload = {
        "messages": [
            {"data": str(base64.b64encode(bytes("MESSAGE_DATA", "utf-8")), "utf-8")}
        ]
    }
    publish_request_path = "https://pubsub.googleapis.com/v1/projects/{}/topics/{}:publish".format(
        project_id, topic_id
    )
    publish_resp = req.post(
        url=publish_request_path, data=json.dumps(publish_payload), headers=headers
    )
    assert publish_resp.ok, publish_resp.raise_for_status()
    print(
        "Pub/Sub message has been successfully published to {}: {}".format(
            topic_id, publish_resp.json()
        )
    )

    # Delete Pub/Sub topic
    pubsub_client.delete_topic(request={"topic": topic_path})
    print("Successfully deleted Pub/Sub topic: {}".format(topic_id))
    # [END iot_access_token_pubsub]


def download_cloud_storage_file(
    cloud_region,
    project_id,
    registry_id,
    device_id,
    algorithm,
    rsa_private_key_path,
    bucket_name,
    data_path,
):
    """Downloads a file from Cloud Storage bucket."""
    # [START iot_access_token_gcs]
    # cloud_region = 'us-central1'
    # project_id = 'YOUR_PROJECT_ID'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # algorithm = 'RS256'
    # rsa_private_key_path = 'path/to/private_key.pem'
    # bucket_name = 'name-of-gcs-bucket'
    # data_path = 'path/to/file/to/be/uploaded.png'
    scope = "https://www.googleapis.com/auth/devstorage.full_control"

    # Generate device access token
    access_token = generate_access_token(
        cloud_region,
        project_id,
        registry_id,
        device_id,
        scope,
        algorithm,
        rsa_private_key_path,
    )

    headers = {
        "authorization": "Bearer {}".format(access_token),
        "content-type": "application/json",
        "cache-control": "no-cache",
    }

    # Create GCS bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "COLDLINE"
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    storage_client.create_bucket(bucket, location=cloud_region)
    print("Successfully created Storage bucket: {}".format(bucket_name))

    # Upload data to GCS bucket.
    data_name = "testFile.ext"
    binary_data = open(data_path, "rb").read()
    upload_request_path = "https://storage.googleapis.com/upload/storage/v1/b/{}/o?uploadType=media&name={}".format(
        bucket_name, data_name
    )
    upload_resp = req.post(url=upload_request_path, data=binary_data, headers=headers)
    print("Upload response: ", upload_resp.json())
    assert upload_resp.ok, upload_resp.raise_for_status()
    print(
        "Successfully uploaded {} as {} to bucket {}.".format(
            data_path, data_name, bucket_name
        )
    )

    # Download data from GCS bucket.
    download_request_path = "https://storage.googleapis.com/storage/v1/b/{}/o/{}?alt=media".format(
        bucket_name, data_name
    )
    download_resp = req.get(url=download_request_path, headers=headers)
    assert download_resp.ok, download_resp.raise_for_status()
    print("Successfully downloaded {} from bucket {}.".format(data_name, bucket_name))

    # Delete data from GCS bucket.
    blob = bucket.blob(data_name)
    blob.delete()
    print("Successfully deleted {} from bucket {}.".format(data_name, bucket_name))

    # Delete GCS Bucket
    bucket.delete()
    print("Successfully deleted bucket: {}".format(bucket_name))
    # [END iot_access_token_gcs]


def exchange_device_access_token_for_service_account_access_token(
    device_access_token, service_account_email
):
    """Exchanges device access token to service account access token."""
    # [START iot_access_token_service_account_token]
    # device_access_token = 'device-access-token'
    # service_account_email  = 'your-service-account@your-project.iam.gserviceaccount.com'
    scope = "https://www.googleapis.com/auth/cloud-platform"
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
    assert exchange_resp.ok, exchange_resp.raise_for_status()
    service_account_token = exchange_resp.json()["accessToken"]
    print("Service account access token: {}".format(service_account_token))
    return service_account_token
    # [END iot_access_token_service_account_token]


def send_iot_command_to_device(
    cloud_region,
    project_id,
    registry_id,
    device_id,
    algorithm,
    rsa_private_key_path,
    service_account_email,
    command_to_be_sent_to_device,
):
    """Sends a command to an IoT device."""
    # [START iot_access_token_iot_send_command]
    # cloud_region = 'us-central1'
    # project_id = 'YOUR_PROJECT_ID'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # algorithm = 'RS256'
    # rsa_private_key_path = 'path/to/private_key.pem'
    # service_account_email = 'your-service-account@your-project.iam.gserviceaccount.com'
    # command_to_be_sent_to_device = 'command-to-device'
    scope = "https://www.googleapis.com/auth/cloud-platform"

    # Generate device access token
    access_token = generate_access_token(
        cloud_region,
        project_id,
        registry_id,
        device_id,
        scope,
        algorithm,
        rsa_private_key_path,
    )
    service_account_token = exchange_device_access_token_for_service_account_access_token(
        access_token, service_account_email
    )

    # Sending a command to a Cloud IoT Core device
    command_payload = json.dumps(
        {
            "binaryData": base64.urlsafe_b64encode(
                command_to_be_sent_to_device.encode("utf-8")
            ).decode("utf-8")
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
    assert command_resp.ok, command_resp.raise_for_status()
    print(
        "Successfully sent command {} to device.".format(command_to_be_sent_to_device)
    )
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
        help="Encryption algorithm used to generate the device JWT.",
    )
    parser.add_argument("--private_key_file", help="Path to private key file.")
    parser.add_argument(
        "--cloud_region", default="us-central1", help="GCP cloud region."
    )

    parser.add_argument("--device_id", default=None, help="Device ID.")
    parser.add_argument(
        "--scope",
        default=None,
        help="Scope for OAuth 2.0 access token. Space delimited strings. See the full list of scopes at: https://developers.google.com/identity/protocols/oauth2/scopes",
    )

    parser.add_argument(
        "--project_id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        help="GCP cloud project name.",
    )
    parser.add_argument(
        "--registry_id", default=None, help="Registry ID.",
    )
    parser.add_argument(
        "--topic_id", default=None, help="Cloud Pub/Sub topic ID.",
    )
    parser.add_argument(
        "--bucket_name", default=None, help="Cloud Storage bucket name.",
    )
    parser.add_argument(
        "--data_path", default=None, help="Path to file to be uploaded.",
    )
    parser.add_argument(
        "--service_account_email",
        default=None,
        help="Service account email to exchange device access token to service account token.",
    )
    parser.add_argument(
        "--device_access_token",
        default=None,
        help="Device access token to exchange for service account access token.",
    )
    parser.add_argument(
        "--command_to_be_sent_to_device",
        default=None,
        help="Command to be sent to the IoT device.",
    )

    # Command subparser
    command = parser.add_subparsers(dest="command")
    command.add_parser("generate-access-token", help=generate_access_token.__doc__)
    command.add_parser("publish-pubsub-message", help=publish_pubsub_message.__doc__)
    command.add_parser(
        "send-command-to-iot-device", help=send_iot_command_to_device.__doc__
    )
    command.add_parser(
        "download-cloud-storage-file", help=download_cloud_storage_file.__doc__
    )
    command.add_parser(
        "exchange-device-token-for-service-account-token",
        help=exchange_device_access_token_for_service_account_access_token.__doc__,
    )
    return parser.parse_args()


def run_program(args):
    """Calls the program."""
    if args.command == "exchange-device-token-for-service-account-token":
        if args.service_account_email is None:
            print("Please specify the service_account_email parameter.")
            return
        if args.device_access_token is None:
            print("Please specify the device_access_token parameter.")
            return
        exchange_device_access_token_for_service_account_access_token(
            args.device_access_token, args.service_account_email
        )
        return

    if args.registry_id is None:
        print("Please specify the registry_id parameter.")
        return
    if args.project_id is None:
        print(
            "Please specify the project_id parameter or set the GOOGLE_CLOUD_PROJECT environment variable."
        )
        return
    if args.device_id is None:
        print("Please specify the device_id parameter.")
    if args.algorithm is None:
        print("Please specify the algorithm parameter.")
        return
    if args.private_key_file is None:
        print("Please specify the private_key_file parameter.")
        return

    if args.command == "generate-access-token":
        if args.scope is None:
            print("Please specify the scope parameter.")
            return
        generate_access_token(
            args.cloud_region,
            args.project_id,
            args.registry_id,
            args.device_id,
            args.scope,
            args.algorithm,
            args.private_key_file,
        )
        return
    elif args.command == "publish-pubsub-message":
        if args.topic_id is None:
            print("Please specify the topic_id parameter")
            return
        publish_pubsub_message(
            args.cloud_region,
            args.project_id,
            args.registry_id,
            args.device_id,
            args.algorithm,
            args.private_key_file,
            args.topic_id,
        )
        return
    elif args.command == "send-command-to-iot-device":
        if args.service_account_email is None:
            print("Please specify the service_account_email parameter.")
            return
        if args.command_to_be_sent_to_device is None:
            print("Please specify command_to_be_sent_to_device parameter.")
            return
        send_iot_command_to_device(
            args.cloud_region,
            args.project_id,
            args.registry_id,
            args.device_id,
            args.algorithm,
            args.private_key_file,
            args.service_account_email,
            args.command_to_be_sent_to_device,
        )
        return
    elif args.command == "download-cloud-storage-file":
        if args.bucket_name is None:
            print("Please specify the bucket_name parameter.")
            return
        if args.data_path is None:
            print("Please specify the data_path parameter.")
            return
        download_cloud_storage_file(
            args.cloud_region,
            args.project_id,
            args.registry_id,
            args.device_id,
            args.algorithm,
            args.private_key_file,
            args.bucket_name,
            args.data_path,
        )
        return
    else:
        print("Invalid command.")
        return


if __name__ == "__main__":
    args = parse_command_line_args()
    run_program(args)
