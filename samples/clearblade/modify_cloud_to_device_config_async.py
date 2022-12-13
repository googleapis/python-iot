import asyncio
import os

from clearblade.cloud import iot_v1


async def sample_modify_cloud_to_device_config_async():
    async_client = iot_v1.DeviceManagerAsyncClient()
    device_path = async_client.device_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry",
        "test-dev-1")

    modify_cloud_config_device_request = iot_v1.ModifyCloudToDeviceConfigRequest(name=device_path, binary_data=b'QUJD', version_to_update=6)
    response = await async_client.modify_cloud_to_device_config(request=modify_cloud_config_device_request)
    print(response)

os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
asyncio.run(sample_modify_cloud_to_device_config_async())
