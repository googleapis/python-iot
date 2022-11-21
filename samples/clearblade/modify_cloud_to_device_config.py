from clearblade.cloud import iot_v1

def sample_modify_cloud_to_device_config():
    client = iot_v1.DeviceManagerClient()
    modify_cloud_config_device_request = ModifyCloudToDeviceConfigRequest(name='python_1', binary_data=b'QUJD', version_to_update=1)
    response = client.modify_cloud_to_device_config(request=modify_cloud_config_device_request)
    print(response)