import asyncio
import os

from clearblade.cloud import iot_v1


async def sample_get_devices_list_async():
    client = iot_v1.DeviceManagerAsyncClient()

    registry_path = client.registry_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry")

    request = iot_v1.ListDevicesRequest(parent=registry_path)

    page_result = await client.list_devices(request)
    async for response in page_result:
        print(response)

os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
asyncio.run(sample_get_devices_list_async())
