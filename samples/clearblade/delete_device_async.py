from clearblade.cloud import iot_v1

async def sample_device_delete_async():
    client = iot_v1.DeviceManagerAsyncClient()

    request = iot_v1.DeleteDeviceRequest(name='Python_12')

    response = await client.delete_device(request)