from .config import ClearBladeConfig
from .http_client import SyncClient, AsyncClient
import os
import json

class ClearBladeConfigManager:
    def __init__(self) -> None:
        self._admin_config:ClearBladeConfig = None
        self._regional_config:ClearBladeConfig = None
        self._region_name:str = os.environ.get("CLEARBLADE_REGION")
        self._registry_name:str = os.environ.get("CLEARBLADE_REGISTRY")

    def _set_admin_clearblade_config(self):
        if self._admin_config:
            return

        service_account_file_path = os.environ.get("CLEARBLADE_CONFIGURATION")
        service_account_data = None
        #parse the file and get all te required details.
        with open(service_account_file_path, mode='r') as service_account_file:
            service_account_data = json.load(service_account_file)

        if service_account_data is None:
            #TODO: raise exception
            return None

        system_key = service_account_data['systemKey']
        auth_token = service_account_data['token']
        api_url = service_account_data['url']
        project = service_account_data['project']

        self._admin_config = ClearBladeConfig(system_key=system_key, auth_token=auth_token,
                                                 api_url=api_url, project=project)

    def _create_regional_config(self, regional_json: json = None)-> ClearBladeConfig :
        system_key = regional_json['systemKey']
        auth_token = regional_json['serviceAccountToken']
        api_url = regional_json['url']
        region = regional_json['region']

        return ClearBladeConfig(system_key=system_key, auth_token=auth_token, api_url=api_url,
                                region=region, project=self._admin_config.project)

    def _set_regional_config(self, region:str = None, registry:str = None):
        self._set_admin_clearblade_config()

        if not region:
            region = self._region_name

        if not registry:
            registry = self.registry_name

        sync_client = SyncClient(clearblade_config=self._admin_config)
        request_body = {'region':region,'registry':registry, 'project':self._admin_config.project}
        response = sync_client.post(api_name="getRegistryCredentials", is_webhook_folder=False,
                                    request_body=request_body)

        if response.status_code != 200:
            #TODO: raise some exceptions
            return None

        response_json = response.json()
        response_json['region'] = region
        self._regional_config = self._create_regional_config(regional_json=response_json)

    async def _set_regional_config_async(self, region:str = None, registry:str = None):

        self._set_admin_clearblade_config()

        if not region:
            region = self._region_name

        if not registry:
            registry = self.registry_name

        async_client = AsyncClient(clearblade_config=self._admin_config)
        request_body = {'region':region,'registry':registry, 'project':self._admin_config.project}
        response = await async_client.post(api_name="getRegistryCredentials",
                                           is_webhook_folder=False,
                                           request_body=request_body)

        if response.status_code != 200:
            #TODO: raise some exceptions
            return None

        response_json = response.json()
        response_json['region'] = region
        self._regional_config = self._create_regional_config(regional_json=response_json)


    @property
    def admin_config(self):
        if not self._admin_config:
            self._set_admin_clearblade_config()

        return self._admin_config

    @property
    def regional_config(self):
        if not self._regional_config:
            self._set_regional_config()

        return self._regional_config

    @property
    async def regional_config_async(self):
        if not self._regional_config:
            await self._set_regional_config_async()

        return self._regional_config

    @property
    def registry_name(self):
        return self._registry_name

    @property
    def region_name(self):
        return self._region_name