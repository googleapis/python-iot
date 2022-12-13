import asyncio
import os

from clearblade.cloud import iot_v1


async def sample_send_command_to_device_async():
    async_client = iot_v1.DeviceManagerAsyncClient()

    device_path = async_client.device_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry",
        "test-dev-1")

    request = iot_v1.SendCommandToDeviceRequest(name=device_path, binary_data=b"QUJD")
    response = await async_client.send_command_to_device(request)
    print(response)

os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
asyncio.run(sample_send_command_to_device_async())
