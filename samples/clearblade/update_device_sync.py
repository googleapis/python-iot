from clearblade.cloud import iot_v1

def sample_update_device():
    client = iot_v1.DeviceManagerClient()

    request = iot_v1.UpdateDeviceRequest(name='Rashmi_Device_Test',id='Rashmi_Device_Test',logLevel='NONE',blocked=True, updateMask='logLevel')

    response = client.update_device(request)
