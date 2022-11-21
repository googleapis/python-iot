from clearblade.cloud import iot_v1

async def sample_send_command_to_device_async():
    async_client = iot_v1.DeviceManagerAsyncClient()
    request = iot_v1.SendCommandToDeviceRequest(name='python_1', binary_data="QUJD")
    response = await async_client.send_command_to_device(request)
    print(response)