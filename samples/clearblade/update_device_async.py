import asyncio
import os

from clearblade.cloud import iot_v1


async def sample_update_device_async():
    client = iot_v1.DeviceManagerAsyncClient()

    registry_path = client.registry_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry")

    device = iot_v1.Device(id="test-dev-1", blocked=True, log_level=iot_v1.LogLevel.ERROR)

    request = iot_v1.UpdateDeviceRequest(
        parent=registry_path,
        device=device,
        updateMask="logLevel,blocked")

    response = await client.update_device(request)

    print(response)

os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
asyncio.run(sample_update_device_async())
