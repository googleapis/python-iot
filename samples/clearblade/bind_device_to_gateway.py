from clearblade.cloud import iot_v1

def sample_bind_device_to_gateway():
    client = iot_v1.DeviceManagerClient()
    request = iot_v1.BindDeviceToGatewayRequest(deviceId='Python_101',gatewayId='gateway1')
    response = client.bind_device_to_gateway(request)
    print(response)