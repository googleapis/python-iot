import io
import os

from clearblade.cloud import iot_v1


def create_device_in_dev_iot(name, keyFile):

    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry")

    with io.open(keyFile) as f:
        public_key = f.read()

    device = iot_v1.Device(
        id=name,
        credentials=[
            {
                "publicKey": {
                    "format": iot_v1.PublicKeyFormat.RSA_PEM,
                    "key": public_key,
                }
            }])
    request = iot_v1.CreateDeviceRequest(parent=parent, device=device)
    return client.create_device(request=request)


device_name = "python_sdk_device_dummy"
key_path = "../api-client/manager/resources/ec_public.pem"
os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/rajas/Downloads/test-credentials.json"
create_device_in_dev_iot(device_name, key_path)
