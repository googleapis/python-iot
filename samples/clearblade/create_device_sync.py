import os

from clearblade.cloud import iot_v1


def sample_create_device():
    client = iot_v1.DeviceManagerClient()
    parent = client.registry_path(
        "api-project-320446546234", 
        "us-central1", 
        "deleteTest5")

    device = iot_v1.Device(id="Python_11", name="Python_11")
    request = iot_v1.CreateDeviceRequest(parent=parent, device=device)

    response = client.create_device(request)
    print(response)

os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/rajas/Downloads/test-credentials.json"
sample_create_device()
