import os

from clearblade.cloud import iot_v1


def sample_modify_cloud_to_device_config():
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry",
        "test-dev-1")

    modify_cloud_config_device_request = iot_v1.ModifyCloudToDeviceConfigRequest(name=device_path, binary_data=b'aGVsbG8gcmFqYXMgd2Fzc3Vw', version_to_update=4)
    response = client.modify_cloud_to_device_config(request=modify_cloud_config_device_request)
    print(response)


os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
sample_modify_cloud_to_device_config()
