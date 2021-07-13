
import argparse
import io
import os
import time
from datetime import datetime, timedelta

import jwt

import requests as req


HOST = ""

def generate_gcp_token(project_id,
    cloud_region,
    registry_id,
    device_id,
    scope,
    algorithm,
    certificate_path):
  jwt_token = generate_jwt_token(
    project_id,
     algorithm,
     certificate_path
     )
  token = exchange_jwt_token_with_gcp_token(cloud_region,
   project_id,
   registry_id,
  device_id,
  jwt_token,
  scope)
  return token

def generate_jwt_token(project_id, algorithm, path_to_private_certificate):
  jwt_payload = "{{'iat':{},'exp':{},'aud':{}}}".format(time.time(), time.mktime((datetime.now() + timedelta(hours=6)).timetuple()),project_id);
  private_key_bytes = ""
  with io.open(path_to_private_certificate) as f:
        private_key_bytes = f.read()
  encoded_jwt = jwt.encode(jwt_payload, private_key_bytes, algorithm=algorithm);
  return encoded_jwt


def exchange_jwt_token_with_gcp_token(cloud_region, project_id, registry_id, device_id, jwt_token, scopes):
  request_path = "{}/v1alpha1/projects/{}/locations/{}/registries/{}/devices/{}:generateAccessToken".format(HOST,project_id, cloud_region,registry_id, device_id )
  payload = {}
  headers = {'authorization' : "Bearer {}".format(jwt_token)}
  resp = req.post(url = request_path, data = payload, headers = headers)
  print(resp.raise_for_status())
  return resp.json()

def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Optional arguments
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
    parser.add_argument("--scope", default=None, help="Scope for GCP token. Space delimited strings")

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
    """Calls the program using the specified command."""
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
    token = generate_gcp_token(args.project_id,
    args.cloud_region,
    args.registry_id,
    args.device_id,
    args.scope,
    args.algorithm,
    args.certificate_path)
    print("Generated GCP compatible token: ", token)


if __name__ == "__main__":
    args = parse_command_line_args()
    run_program(args)
