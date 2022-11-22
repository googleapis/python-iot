from clearblade.cloud import iot_v1

async def sample_modify_cloud_to_device_config_async():
    async_client = iot_v1.DeviceManagerAsyncClient()
    modify_cloud_config_device_request = iot_v1.ModifyCloudToDeviceConfigRequest(name='python_1', binary_data=b'QUJD', version_to_update=1)
    response = await async_client.modify_cloud_to_device_config(request=modify_cloud_config_device_request)
    print(response)