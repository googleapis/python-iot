from clearblade.cloud import iot_v1

async def sample_get_device_states_list_async():
    async_client = iot_v1.DeviceManagerAsyncClient()

    request = iot_v1.GetDeviceStatesList(name='Rashmi_Device_Test', numStates=3)
    response = await async_client.list_device_states(request)
    