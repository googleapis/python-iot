import os

from clearblade.cloud import iot_v1


def sample_get_device_config_versions_list():
    client = iot_v1.DeviceManagerClient()

    device_path = client.device_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry",
        "test-dev-1")

    request = iot_v1.ListDeviceConfigVersionsRequest(name=device_path, numVersions=1)
    response = client.list_device_config_versions(request)
    print(response.device_configs)


os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
sample_get_device_config_versions_list()
