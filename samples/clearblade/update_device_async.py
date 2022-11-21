from clearblade.cloud import iot_v1

async def sample_update_device_async():
    client = iot_v1.DeviceManagerAsyncClient()

    request = iot_v1.UpdateDeviceRequest(name='Rashmi_Device_Test',id='Rashmi_Device_Test',logLevel='NONE',blocked=True, updateMask='logLevel')

    response = await client.update_device(request)
