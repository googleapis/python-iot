from .device_types import *
from .devices import *
from .registry import *
from .registry_types import *

class Client():
    def device_path(
        self,
        project: str,
        location: str,
        registry: str,
        device: str
        ) -> str:
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.device_path(project=project, 
                                             location=location, 
                                             registry=registry, 
                                             device=device)
    
    def registry_path(
        self,
        project: str,
        location: str,
        registry: str
        ) -> str:
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.registry_path(project=project, 
                                               location=location, 
                                               registry=registry)

class DeviceManagerClient(Client):

    def send_command_to_device(self,request:SendCommandToDeviceRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.send_command(request)

    def create_device(self, request):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.create(request=request)

    def modify_cloud_to_device_config(self, request: ModifyCloudToDeviceConfigRequest,
                                      name: str = None,
                                      version_to_update = "",
                                      binary_data:bytes = None):

        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.modify_cloud_device_config(request=request,
                                                            name=name,
                                                            version_to_update=version_to_update,
                                                            binary_data=binary_data)

    def delete_device(self, request):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.delete(request=request)

    def get_device(self, request):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.get(request=request)

    def bind_device_to_gateway(self, request : BindDeviceToGatewayRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.bindGatewayToDevice(request=request)

    def unbind_device_from_gateway(self, request : UnbindDeviceFromGatewayRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.unbindGatewayFromDevice(request=request)

    def list_device_states(self, request : ListDeviceStatesRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.states_list(request=request)

    def list_device_config_versions(self, request : ListDeviceConfigVersionsRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.config_versions_list(request=request)

    def list_devices(self, request : ListDevicesRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.list(request=request)

    def update_device(self, request : UpdateDeviceRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.update(request=request)

    def list_device_registries(self, request: ListDeviceRegistriesRequest):
        cb_registry_manager = ClearBladeRegistryManager()
        return cb_registry_manager.list(request=request)

    def get_device_registry(self, request=GetDeviceRegistryRequest):
        cb_registry_manager = ClearBladeRegistryManager()
        return cb_registry_manager.get(request=request)

    def create_device_registry(self, request=CreateDeviceRegistryRequest):
        cb_registry_manager = ClearBladeRegistryManager()
        return cb_registry_manager.create(request=request)

    def delete_device_registry(self, request=DeleteDeviceRegistryRequest):
        cb_registry_manager = ClearBladeRegistryManager()
        return cb_registry_manager.delete(request=request)

    def update_device_registry(self, request=UpdateDeviceRegistryRequest):
        cb_registry_manager = ClearBladeRegistryManager()
        return cb_registry_manager.patch(request=request)

class DeviceManagerAsyncClient(Client):

    async def send_command_to_device(self, request:SendCommandToDeviceRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.send_command_async(request)

    async def create_device(self, request):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.create_async(request)

    async def modify_cloud_to_device_config(self, request: ModifyCloudToDeviceConfigRequest,
                                            name: str = None,
                                            version_to_update = "",
                                            binary_data:bytes = None):

        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.modify_cloud_device_config_async(request=request,
                                                            name=name,
                                                            version_to_update=version_to_update,
                                                            binary_data=binary_data)

    async def delete_device(self, request):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.delete_async(request=request)

    async def get_device(self, request):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.get_async(request=request)

    async def bind_device_to_gateway(self, request : BindDeviceToGatewayRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.bindGatewayToDevice_async(request=request)

    async def unbind_device_from_gateway(self, request : UnbindDeviceFromGatewayRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.unbindGatewayFromDevice_async(request=request)

    async def list_device_states(self, request : ListDeviceStatesRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.states_list_async(request=request)

    async def list_device_config_versions(self, request : ListDeviceConfigVersionsRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.config_versions_list_async(request=request)

    async def list_devices(self, request : ListDevicesRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.list_async(request=request)

    async def update_device(self, request : UpdateDeviceRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.update_async(request=request)

    async def list_device_registries(self, request: ListDeviceRegistriesRequest):
        cb_registry_manager = ClearBladeRegistryManager()
        return await cb_registry_manager.list_async(request=request)

    async def get_device_registry(self, request=GetDeviceRegistryRequest):
        cb_registry_manager = ClearBladeRegistryManager()
        return await cb_registry_manager.get_async(request=request)

    async def create_device_registry(self, request=CreateDeviceRegistryRequest):
        cb_registry_manager = ClearBladeRegistryManager()
        return await cb_registry_manager.create_async(request=request)

    async def delete_device_registry(self, request=DeleteDeviceRegistryRequest):
        cb_registry_manager = ClearBladeRegistryManager()
        return await cb_registry_manager.delete_async(request=request)

    async def update_device_registry(self, request=UpdateDeviceRegistryRequest):
        cb_registry_manager = ClearBladeRegistryManager()
        return await cb_registry_manager.patch_async(request=request)
