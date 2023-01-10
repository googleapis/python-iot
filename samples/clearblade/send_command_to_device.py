import json
import os

from clearblade.cloud import iot_v1


def sample_send_command_to_device():
    client = iot_v1.DeviceManagerClient()

    data = json.dumps({
        "device_code": "1",
        "command": "test",
        "command_option": "0",
        "seq_no": 10
    }).encode("utf-8")

    device_path = client.device_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry",
        "test-dev-1")

    request = iot_v1.SendCommandToDeviceRequest(name=device_path, binary_data=data)
    response = client.send_command_to_device(request)
    print(response)


os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
sample_send_command_to_device()
