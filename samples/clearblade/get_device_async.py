import asyncio
import os

from clearblade.cloud import iot_v1


async def sample_device_get_async():
    client = iot_v1.DeviceManagerAsyncClient()

    device_path = client.device_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry",
        "test-dev-1")

    request = iot_v1.GetDeviceRequest(name=device_path)

    response = await client.get_device(request)

    print(response.id)

os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
asyncio.run(sample_device_get_async())
