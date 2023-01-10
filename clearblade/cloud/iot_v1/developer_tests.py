from client import DeviceManagerClient, DeviceManagerAsyncClient
from device_types import *
from registry import *
from registry_types import *
import asyncio

def test_send_command():
    client = DeviceManagerClient()
    request = SendCommandToDeviceRequest(name='python_1', binary_data=b'QUJD')
    response = client.send_command_to_device(request)
    print(response)

async def test_send_command_async():
    async_client = DeviceManagerAsyncClient()
    request = SendCommandToDeviceRequest(name='python_1', binary_data=b'R2FyZ2l0ZXN0aW5n')
    response = await async_client.send_command_to_device(request=request)
    print(response)

def test_create_device():
    client = DeviceManagerClient()
    device = Device(id="Python_101", name="Python_101")
    request = CreateDeviceRequest(device=device)
    response = client.create_device(request=request)
    print(response)

async def test_create_device_async():
    async_client = DeviceManagerAsyncClient()
    device = Device(id="Python_12", name="Python_12")
    request = CreateDeviceRequest(device=device)
    response = await async_client.create_device(request=request)
    print(response)

def test_modify_cloud_to_device_config():
    client =  DeviceManagerClient()
    modify_cloud_config_device_request = ModifyCloudToDeviceConfigRequest(name='python_1', binary_data=b'QUJD', version_to_update=1)
    response = client.modify_cloud_to_device_config(request=modify_cloud_config_device_request)
    print(response)

async def test_modify_cloud_to_device_config_async():
    async_client =  DeviceManagerAsyncClient()
    modify_cloud_config_device_request = ModifyCloudToDeviceConfigRequest(name='Python_101', binary_data=b'QUJD', version_to_update=2)
    response = await async_client.modify_cloud_to_device_config(request=modify_cloud_config_device_request)
    print(response)

def test_delete_device():
    client =  DeviceManagerClient()
    delete_device_request = DeleteDeviceRequest(name='Python_12')
    response = client.delete_device(request=delete_device_request)
    print(response)

async def test_delete_device_async():
    async_client =  DeviceManagerAsyncClient()
    delete_device_request = DeleteDeviceRequest(name='Python_10')
    response = await async_client.delete_device(request=delete_device_request)
    print(response)

def test_get_device():
    client =  DeviceManagerClient()
    get_device_request = GetDeviceRequest(name='Python_101')
    response = client.get_device(request=get_device_request)
    print(response)

async def test_get_device_async():
    async_client =  DeviceManagerAsyncClient()
    get_device_request = GetDeviceRequest(name='Python_101')
    response = await async_client.get_device(request=get_device_request)
    print(response)

def test_bind_gateway_device():
    client =  DeviceManagerClient()
    bind_device_request = BindDeviceToGatewayRequest(deviceId='Python_101',gatewayId='gateway1')
    response = client.bind_device_to_gateway(request=bind_device_request)
    print(response)

async def test_bind_gateway_device_async():
    async_client =  DeviceManagerAsyncClient()
    bind_device_request = BindDeviceToGatewayRequest(deviceId='mandar_device',gatewayId='gateway1')
    response = await async_client.bind_device_to_gateway(request=bind_device_request)
    print(response)

def test_unbind_gateway_device():
    client =  DeviceManagerClient()
    bind_device_request = UnbindDeviceFromGatewayRequest(deviceId='Python_101',gatewayId='gateway1')
    response = client.unbind_device_from_gateway(request=bind_device_request)
    print(response)

async def test_unbind_gateway_device_async():
    async_client =  DeviceManagerAsyncClient()
    bind_device_request = UnbindDeviceFromGatewayRequest(deviceId='mandar_device',gatewayId='gateway1')
    response = await async_client.unbind_device_from_gateway(request=bind_device_request)
    print(response)

def test_get_device_states():
    client = DeviceManagerClient()
    request = ListDeviceStatesRequest(name='Python_5', num_states=3)
    response = client.list_device_states(request)
    print(response)

async def test_get_device_states_async():
    async_client = DeviceManagerAsyncClient()
    request = ListDeviceStatesRequest(name='Python_6', num_states=3)
    response = await async_client.list_device_states(request=request)
    print(response)

def test_get_device_configVersions():
    client = DeviceManagerClient()
    request = ListDeviceConfigVersionsRequest(name='Python_6', numVersions=1)
    response = client.list_device_config_versions(request)
    device_configs = response.device_configs
    for device_config in device_configs:
        print("Device version = {} Device Ack Time {} \n".format(device_config.version,
        device_config.cloud_update_time))

async def test_get_device_configVersions_async():
    async_client = DeviceManagerAsyncClient()
    request = ListDeviceConfigVersionsRequest(name='Python_6', numVersions=1)
    response = await async_client.list_device_config_versions(request=request)
    print(response)

def test_get_devices_list():
    client =  DeviceManagerClient()
    get_devices_list_request = ListDevicesRequest(parent='projects/ingressdevelopmentenv/locations/us-central1', pageSize=2)
    page_result = client.list_devices(request=get_devices_list_request)
    for response in page_result:
       print(response)

async def test_get_devices_list_async():
    async_client = DeviceManagerAsyncClient()
    get_devices_list_request = ListDevicesRequest(parent='projects/ingressdevelopmentenv/locations/us-central1')
    page_result = await async_client.list_devices(request=get_devices_list_request)
    async for response in page_result:
        print(response)

def test_update_device():
    client =  DeviceManagerClient()
    update_device_request = UpdateDeviceRequest(name='Rashmi_Device_Test',id='Rashmi_Device_Test',logLevel='NONE',blocked=True, updateMask='logLevel')
    response = client.update_device(request=update_device_request)
    print(response)

async def test_update_device_async():
    async_client = DeviceManagerAsyncClient()
    update_device_request = UpdateDeviceRequest(name='Rashmi_Device_Test',id='Rashmi_Device_Test',logLevel='ERROR',blocked=True, updateMask='logLevel')
    response = await async_client.update_device(request=update_device_request)
    print(response)

def test_list_registries():
    client = DeviceManagerClient()
    request = ListDeviceRegistriesRequest(parent="projects/ingressdevelopmentenv/locations/us-central1")
    response = client.list_device_registries(request=request)
    for page_result in response:
        print(page_result)

async def test_list_registries_async():
    client = DeviceManagerAsyncClient()
    request = ListDeviceRegistriesRequest(parent="projects/ingressdevelopmentenv/locations/us-central1")
    response = await client.list_device_registries(request=request)
    async for page_result in response:
        print(page_result)

def test_get_registry():
    client = DeviceManagerClient()
    request = GetDeviceRegistryRequest()
    response = client.get_device_registry(request=request)
    print(response)

async def test_get_registry_async():
    async_client = DeviceManagerAsyncClient()
    request = GetDeviceRegistryRequest()
    response = await async_client.get_device_registry(request=request)
    print(response)

def test_create_registry():
    client = DeviceManagerClient()
    registry = DeviceRegistry(id='deleteTest5', mqttConfig={'mqttEnabledState':'MQTT_ENABLED'},
                              httpConfig={'httpEnabledState':'HTTP_ENABLED'},
                              logLevel='ERROR', 
                              eventNotificationConfigs=[{'pubsubTopicName':'projects/ingressdevelopmentenv/topics/deleting'}])
    request = CreateDeviceRegistryRequest(parent="projects/ingressdevelopmentenv/locations/us-central1",device_registry=registry)
    response = client.create_device_registry(request=request)
    print(response)

async def test_create_registry_async():
    async_client = DeviceManagerAsyncClient()
    registry = DeviceRegistry(id='deletetest3', name='deletetest3', mqttConfig={'mqttEnabledState':'MQTT_ENABLED'},httpConfig={'httpEnabledState':'HTTP_ENABLED'},logLevel='ERROR', eventNotificationConfigs=[{'pubsubTopicName':'projects/ingressdevelopmentenv/topics/deleting'}])
    request = CreateDeviceRegistryRequest(parent="projects/ingressdevelopmentenv/locations/us-central1",device_registry=registry)
    response = await async_client.create_device_registry(request=request)
    print(response)

def test_delete_registry():
    client = DeviceManagerClient()
    request = DeleteDeviceRegistryRequest(name="projects/ingressdevelopmentenv/locations/us-central1/registries/deleteTest2")
    response = client.delete_device_registry(request=request)
    print(response)

async def test_delete_registry_async():
    async_client = DeviceManagerAsyncClient()
    request = DeleteDeviceRegistryRequest(name="projects/ingressdevelopmentenv/locations/us-central1/registries/deleteTest3")
    response = await async_client.delete_device_registry(request=request)
    print(response)

def test_update_registry():
    client = DeviceManagerClient()
    registry = DeviceRegistry(id='deleteTest5', name='deleteTest5', mqttConfig={'mqttEnabledState':'MQTT_DISABLED'},logLevel='ERROR')
    request = UpdateDeviceRegistryRequest(name="projects/ingressdevelopmentenv/locations/us-central1/registries/deleteTest5", updateMask='mqttConfig.mqtt_enabled_state,logLevel', device_registry=registry)
    response = client.update_device_registry(request=request)
    print(response)

async def test_update_registry_async():
    async_client = DeviceManagerAsyncClient()
    registry = DeviceRegistry(id='deleteTest5', name='deleteTest5', mqttConfig={'mqttEnabledState':'MQTT_ENABLED'},logLevel='DEBUG')
    request = UpdateDeviceRegistryRequest(name="projects/ingressdevelopmentenv/locations/us-central1/registries/deleteTest5", updateMask='mqttConfig.mqtt_enabled_state,logLevel', device_registry=registry)
    response = await async_client.update_device_registry(request=request)
    print(response)

if __name__ ==  '__main__':
    #test_send_command()
    #asyncio.run(test_send_command_async())
    #test_create_device()
    #asyncio.run(test_create_device_async())
    #test_modify_cloud_to_device_config()
    #asyncio.run(test_modify_cloud_to_device_config_async())
    #test_delete_device()
    #asyncio.run(test_delete_device_async())
    #test_get_device()
    #asyncio.run(test_get_device_async())
    #test_bind_gateway_device()
    #asyncio.run(test_bind_gateway_device_async())
    #test_unbind_gateway_device()
    #asyncio.run(test_unbind_gateway_device_async())
    #test_get_device_states()
    #asyncio.run(test_get_device_states_async())
    #test_get_device_configVersions()
    #asyncio.run(test_get_device_configVersions_async())
    
    test_list_registries()
    asyncio.run(test_list_registries_async())

    test_get_devices_list()
    asyncio.run(test_get_devices_list_async())
    
    #test_update_device()
    #asyncio.run(test_update_device_async())
    #test_list_registries()
    #test_get_registry()
    #asyncio.run(test_get_registry_async())
    #test_create_registry()
    #asyncio.run(test_create_registry_async())
    #test_delete_registry()
    #asyncio.run(test_delete_registry_async())
    #test_update_registry()
    #asyncio.run(test_update_registry_async())
