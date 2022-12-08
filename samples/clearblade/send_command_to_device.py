import os

from clearblade.cloud import iot_v1


def sample_send_command_to_device():
    client = iot_v1.DeviceManagerClient()
    
    device_path = client.device_path(
        "api-project-320446546234", 
        "us-central1", 
        "rajas-test",
        "test-dev-1")

    request = iot_v1.SendCommandToDeviceRequest(name=device_path, binary_data=b"QUJD")
    response = client.send_command_to_device(request)
    print(response)

os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/rajas/Downloads/test-credentials.json"
sample_send_command_to_device()
