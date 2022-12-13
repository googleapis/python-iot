import asyncio
import os

from clearblade.cloud import iot_v1


async def sample_get_device_config_versions_list_async():
    async_client = iot_v1.DeviceManagerAsyncClient()

    device_path = async_client.device_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry",
        "test-dev-1")

    request = iot_v1.ListDeviceConfigVersionsRequest(name=device_path, numVersions=3)
    response = await async_client.list_device_config_versions(request)
    print(response.device_configs)

os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
asyncio.run(sample_get_device_config_versions_list_async())
