from clearblade.cloud import iot_v1

async def sample_bind_device_to_gateway_async():
    async_client = iot_v1.DeviceManagerAsyncClient()
    request = iot_v1.BindDeviceToGatewayRequest(deviceId='Python_101',gatewayId='gateway1')
    response = await async_client.bind_device_to_gateway(request)
    print(response)