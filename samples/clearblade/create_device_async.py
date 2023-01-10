import asyncio
import os

from clearblade.cloud import iot_v1


async def sample_create_device_async():
    async_client = iot_v1.DeviceManagerAsyncClient()

    parent = async_client.registry_path(
        "api-project-320446546234",
        "asia-east1",
        "test-asia-east1")

    device = iot_v1.Device(id="Python_SDK")
    request = iot_v1.CreateDeviceRequest(parent=parent, device=device)

    response = await async_client.create_device(request)

    print(response)

os.environ["CLEARBLADE_CONFIGURATION"] = "D:/DummyUser/test-credentials.json"
asyncio.run(sample_create_device_async())
