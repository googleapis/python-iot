from clearblade.cloud import iot_v1

def sample_unbind_device_from_gateway():
    client = iot_v1.DeviceManagerClient()
    request = iot_v1.UnbindDeviceFromGatewayRequest(deviceId='Python_101',gatewayId='gateway1')
    response = client.unbind_device_from_gateway(request)
    print(response)