from .config_manager import ClearBladeConfigManager
from .http_client import AsyncClient, SyncClient
from .pagers import ListDeviceRegistriesAsyncPager, ListDeviceRegistryPager
from .registry_types import *


class ClearBladeRegistryManager():
    def __init__(self) -> None:
        self._cb_config = ClearBladeConfigManager()

    def _create_registry_body(self, registry: DeviceRegistry) :
        registry_json = {'id':registry.id}
        if registry.credentials:
            registry_json['credentials']=registry.credentials
        if registry.http_config:
            registry_json['httpConfig']=registry.http_config
        if registry.mqtt_config:
            registry_json['mqttConfig']=registry.mqtt_config
        if registry.state_notification_config:
            registry_json['stateNotificationConfig']=registry.state_notification_config
        if registry.event_notification_configs:
            registry_json['eventNotificationConfigs']=registry.event_notification_configs
        if registry.log_level:
            registry_json['logLevel']=registry.log_level
        return registry_json

    def _prepare_params_for_registry_list(self, request:ListDeviceRegistriesRequest):
        request_params = {'parent':request.parent}
        if request.page_size:
            request_params['page_size'] = request.page_size
        if request.page_token:
            request_params['page_token'] = request.page_token
        return request_params

    def create(self,
        request: CreateDeviceRegistryRequest = None)->DeviceRegistry:
        body = self._create_registry_body(request.device_registry)
        params = {'parent':request.parent}
        sync_client = SyncClient(clearblade_config=self._cb_config.admin_config)
        response = sync_client.post(api_name = "cloudiot",request_body=body,request_params=params)
        return DeviceRegistry.from_json(response.json())

    async def create_async(self,
        request: CreateDeviceRegistryRequest = None)->DeviceRegistry:
        body = self._create_registry_body(request.device_registry)
        params = {'parent':request.parent}
        async_client = AsyncClient(clearblade_config=self._cb_config.admin_config)
        response = await async_client.post(api_name = "cloudiot",request_body=body,request_params=params)
        return DeviceRegistry.from_json(response.json())

    def get(self,
            request: GetDeviceRegistryRequest = None):
        if request.name == None:
            raise Exception('Registry Path is not present in the request')

        clearblade_config = self._cb_config.regional_config(request.name)

        sync_client = SyncClient(clearblade_config=clearblade_config)
        response = sync_client.get(api_name = "cloudiot")
        return DeviceRegistry.from_json(response.json())

    async def get_async(self,
                        request: GetDeviceRegistryRequest = None):
        
        if request.name == None:
            raise Exception('Registry Path is not present in the request')

        clearblade_config=await self._cb_config.regional_config_async(request.name)
        async_client = AsyncClient(clearblade_config=clearblade_config)
        response = await async_client.get(api_name = "cloudiot")
        return DeviceRegistry.from_json(response.json())

    def get_device_registry_list(self, request: ListDeviceRegistriesRequest):
        request_params = self._prepare_params_for_registry_list(request=request)
        sync_client = SyncClient(clearblade_config=self._cb_config.admin_config)
        response = sync_client.get(api_name = "cloudiot",request_params=request_params)

        if response.status_code == 200:
            return ListDeviceRegistriesResponse.from_json(response.json())
        return None

    def list(self,
            request: ListDeviceRegistriesRequest = None):

        list_device_registry_response = self.get_device_registry_list(request=request)
        if list_device_registry_response:
            return ListDeviceRegistryPager(method=self.get_device_registry_list,
                                           request=request,
                                           response=list_device_registry_response)

    async def get_device_registry_list_async(self, request: ListDeviceRegistriesRequest):
        request_params = self._prepare_params_for_registry_list(request=request)
        async_client = AsyncClient(clearblade_config=self._cb_config.admin_config)
        response = await async_client.get(api_name = "cloudiot",request_params=request_params)

        if response.status_code == 200:
            return ListDeviceRegistriesResponse.from_json(response.json())
        return None

    async def list_async(self, request: ListDeviceRegistriesRequest):
        list_device_registry_response = await self.get_device_registry_list_async(request=request)
        if list_device_registry_response:
            return ListDeviceRegistriesAsyncPager(method=self.get_device_registry_list_async,
                                                  request=request,
                                                  response=list_device_registry_response)
        return None

    def delete(self,
            request: DeleteDeviceRegistryRequest = None):
        params = {'name':request.name}
        sync_client = SyncClient(clearblade_config=self._cb_config.admin_config)
        response = sync_client.delete(api_name = "cloudiot",request_params=params)
        return response

    async def delete_async(self,
            request: DeleteDeviceRegistryRequest = None):
        params = {'name':request.name}
        async_client = AsyncClient(clearblade_config=self._cb_config.admin_config)
        response = await async_client.delete(api_name = "cloudiot",request_params=params)
        return response

    def patch(self,
        request: UpdateDeviceRegistryRequest = None)->DeviceRegistry:
        if request.name == None:
            raise Exception('Registry Path is not present in the request')

        clearblade_config = self._cb_config.regional_config(request.name)
        
        body = self._create_registry_body(request.device_registry)
        params = {'name':request.name, 'updateMask': request.update_mask}
        sync_client = SyncClient(clearblade_config=clearblade_config)
        response = sync_client.patch(api_name = "cloudiot",request_body=body,request_params=params)
        return DeviceRegistry.from_json(response.json())

    async def patch_async(self,
        request: UpdateDeviceRegistryRequest = None)->DeviceRegistry:
        
        if request.name == None:
            raise Exception('Registry Path is not present in the request')

        body = self._create_registry_body(request.device_registry)
        params = {'name':request.name, 'updateMask': request.update_mask}
        clearblade_config=await self._cb_config.regional_config_async(request.name)
        async_client = AsyncClient(clearblade_config=clearblade_config)
        response = await async_client.patch(api_name = "cloudiot",request_body=body,request_params=params)
        return DeviceRegistry.from_json(response.json())