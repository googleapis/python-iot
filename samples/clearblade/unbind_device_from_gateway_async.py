from clearblade.cloud import iot_v1

async def sample_unbind_device_from_gateway_async():
    async_client = iot_v1.DeviceManagerAsyncClient()
    request = iot_v1.UnbindDeviceFromGatewayRequest(deviceId='Python_101',gatewayId='gateway1')
    response = await async_client.unbind_device_from_gateway(request)
    print(response)