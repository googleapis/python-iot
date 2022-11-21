from clearblade.cloud import iot_v1

def sample_send_command_to_device():
    client = iot_v1.DeviceManagerClient()
    request = iot_v1.SendCommandToDeviceRequest(name='python_1', binary_data=b"QUJD")
    response = client.send_command_to_device(request)
    print(response)