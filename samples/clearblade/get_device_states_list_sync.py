from clearblade.cloud import iot_v1

def sample_get_device_states_list():
    client = iot_v1.DeviceManagerClient()

    request = iot_v1.GetDeviceStatesList(name='Rashmi_Device_Test', numStates=3)
    response = client.list_device_states(request)
    