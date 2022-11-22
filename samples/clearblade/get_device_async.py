from clearblade.cloud import iot_v1

async def sample_device_get_async():
    client = iot_v1.DeviceManagerAsyncClient()

    request = iot_v1.GetDeviceRequest(name='Python_12')

    response = await client.get_device(request)