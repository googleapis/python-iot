import os

from clearblade.cloud import iot_v1


def sample_device_delete():
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry",
        "Python_11")

    request = iot_v1.DeleteDeviceRequest(name=device_path)
    response = client.delete_device(request)
    print(response)


os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
sample_device_delete()
