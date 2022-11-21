from clearblade.cloud import iot_v1

async def sample_create_device_async():
    client = iot_v1.DeviceManagerAsyncClient()

    device = iot_v1.Device(id="Python_11", name="Python_11")
    request = iot_v1.CreateDeviceRequest(device=device)

    response = await client.create_device(request)

