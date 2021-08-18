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

    python access.py \\
      --project_id=my-project-id \\
      --cloud_region=us-central1 \\
      --registry_id=my-registry-id \\
      --device_id=my-device-id \\
      --certificate_path=/my-certificate.pem \\
      --scope="scope1 scope2"
"""
import argparse
import io
import json
import os
from datetime import datetime, timedelta
import time


import jwt
import requests as req

HOST = "https://cloudiottoken.googleapis.com"


def generate_gcp_token(
    project_id, cloud_region, registry_id, device_id, scope, algorithm, certificate_file
):
    """Generate GCP access token."""
    # [START iot_generate_gcp_token]
    # project_id = 'YOUR_PROJECT_ID'
    # cloud_region = 'us-central1'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # scope = 'scope1 scope2'
    # algorithm = 'RS256'
    # certificate_file = 'path/to/certificate.pem'

    jwt_token = generate_iot_jwt_token(project_id, algorithm, certificate_file)
    token = exchange_iot_jwt_token_with_gcp_token(
        cloud_region, project_id, registry_id, device_id, jwt_token, scope
    )
    return token
    # [END iot_generate_gcp_token]


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
    # scopes = 'scope1 scope2' https://developers.google.com/identity/protocols/oauth2/scopes
    global HOST
    resource_url = "projects/{}/locations/{}/registries/{}/devices/{}".format(project_id, cloud_region, registry_id, device_id)
    request_path = "{}/v1alpha1/{}:generateAccessToken".format(
        HOST, resource_url
    )
    headers = {"authorization": "Bearer {}".format(jwt_token)}
    request_payload = {"scope": scopes, "device": resource_url}
    resp = req.post(url=request_path, data=request_payload, headers=headers)
    print(resp.raise_for_status())
    return resp.json()
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
        "--scope", default=None, help="Scope for GCP token. Space delimited strings"
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
    token = generate_gcp_token(
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
