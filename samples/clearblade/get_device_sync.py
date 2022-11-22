from clearblade.cloud import iot_v1

def sample_device_get():
    client = iot_v1.DeviceManagerClient()

    request = iot_v1.GetDeviceRequest(name='Python_12')

    response = client.get_device(request)
