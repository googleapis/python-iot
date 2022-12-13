import os

from clearblade.cloud import iot_v1


def sample_get_devices_list():
    client = iot_v1.DeviceManagerClient()

    registry_path = client.registry_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry")

    request = iot_v1.ListDevicesRequest(parent=registry_path)

    response = client.list_devices(request=request)
    for page_result in response:
        print(page_result)


os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
sample_get_devices_list()
