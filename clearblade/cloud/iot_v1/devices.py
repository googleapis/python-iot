# -*- coding: utf-8 -*-
# Copyright 2023 ClearBlade Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from .config_manager import ClearBladeConfigManager
from .device_types import *
from .http_client import AsyncClient, SyncClient
from .pagers import ListDevicesAsyncPager, ListDevicesPager
import base64


class ClearBladeDeviceManager():

    def __init__(self) -> None:
        # create the ClearBladeConfig object
        self._config_manager = ClearBladeConfigManager()

    def _prepare_for_send_command(self,
                                  request: SendCommandToDeviceRequest,
                                  name: str = None,
                                  binary_data: bytes = None,
                                  subfolder: str = None):
        has_flattened_params = any([name, binary_data])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if request is None:
            request = SendCommandToDeviceRequest(name, binary_data, subfolder)
        params = {'name':request.parent,'method':'sendCommandToDevice'}
        body = {'binaryData':base64.b64encode(request.binary_data).decode("utf-8"), 'subfolder':request.sub_folder}

        return params,body

    def _create_device_body(self, device: Device) :
        return {'id':device.id,
                'credentials':device.credentials,
                'config':device.config,
                'blocked': device.blocked,
                'logLevel':device.log_level, 'metadata':device.meta_data,
                'gatewayConfig':device.gateway_config}

    def _create_device_from_response(self, json_response) -> Device :
        return Device.from_json(json=json_response)

    def _prepare_modify_cloud_config_device(self,
                                            request: ModifyCloudToDeviceConfigRequest,
                                            name, binary_data, version_to_update):

        has_flattened_params = any([name, binary_data])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if request is None:
            request = ModifyCloudToDeviceConfigRequest(name=name,version_to_update=version_to_update, binary_data=binary_data)

        params = {'name': request.parent, 'method': 'modifyCloudToDeviceConfig'}
        body = {'binaryData': request.binary_data.decode("utf-8"), 'versionToUpdate':request.version_to_update}

        return params, body

    def _create_device_config(self, response):
        return DeviceConfig.from_json(response)

    def _create_device_list_from_response(self, json_response):
        devicesList = []
        for deviceJson in json_response['devices']:
            devicesList.append(Device.from_json(json=deviceJson))
        return devicesList

    def _set_project_location_region(self, data):
        if 'locations' in data:
            self._config_manager.region_name = data['locations']

        if 'registries' in data:
            self._config_manager.registry_name = data['registries']

    def device_path(self,
                    project,
                    location,
                    registry,
                    device) -> str:
        """Returns a fully-qualified device string."""

        return "projects/{project}/locations/{location}/registries/{registry}/devices/{device}".format(
            project=project,
            location=location,
            registry=registry,
            device=device,
        )

    def registry_path(self,
                      project: str,
                      location: str,
                      registry: str,
                      ) -> str:
        """Returns a fully-qualified registry string."""

        return "projects/{project}/locations/{location}/registries/{registry}".format(
            project=project,
            location=location,
            registry=registry,
        )

    def send_command(self,
                     request: SendCommandToDeviceRequest,
                     name: str = None,
                     binary_data: bytes = None,
                     subfolder: str = None):
        if not request.parent:
            raise Exception('Device path must be supplied to the request object.')

        clearblade_config = self._config_manager.regional_config(parent=request.parent)

        params, body = self._prepare_for_send_command(request, name, binary_data, subfolder)
        sync_client = SyncClient(clearblade_config=clearblade_config)
        return sync_client.post(api_name="cloudiot_devices", request_params=params, request_body=body)

    async def send_command_async(self,
                                 request: SendCommandToDeviceRequest = None,
                                 name: str = None,
                                 binary_data: str = None,
                                 subfolder: str = None):

        if not request.parent:
            raise Exception('Device path must be supplied to the request object.')

        params, body = self._prepare_for_send_command(request, name, binary_data, subfolder)
        clearblade_config = await self._config_manager.regional_config_async(request.parent)
        async_client = AsyncClient(clearblade_config=clearblade_config)
        return await async_client.post(api_name="cloudiot_devices",
                                       request_params=params,
                                       request_body=body)

    def create(self, request: CreateDeviceRequest) -> Device:
        body = self._create_device_body(request.device)

        if not request.parent:
            raise Exception('Parent must be supplied to the request object.')

        clearblade_config = self._config_manager.regional_config(parent=request.parent)

        sync_client = SyncClient(clearblade_config=clearblade_config)
        response = sync_client.post(api_name="cloudiot_devices",
                                    request_body=body)

        # return the device only if status code is 200
        # other wise return None
        if response.status_code == 200:
            return self._create_device_from_response(response.json())
        return response.json()

    async def create_async(self, request: CreateDeviceRequest,
                           parent: str = None,
                           device: Device = None) -> Device:
        if not request.parent:
            raise Exception('Parent must be supplied to the request object.')

        body = self._create_device_body(request.device)
        clearblade_config = await self._config_manager.regional_config_async(request.parent)
        async_client = AsyncClient(clearblade_config=clearblade_config)
        response = await async_client.post(api_name="cloudiot_devices", request_body=body)

        if response.status_code == 200:
            return self._create_device_from_response(response.json())
        return response.json()

    def modify_cloud_device_config(self,
                                   request: ModifyCloudToDeviceConfigRequest,
                                   name:str = None,
                                   version_to_update : int = None,
                                   binary_data: bytes = None):
        if not request.parent:
            raise Exception('Device path must be supplied to the request object.')

        clearblade_config = self._config_manager.regional_config(parent=request.parent)

        params, body = self._prepare_modify_cloud_config_device(request=request, name=name,
                                                                binary_data=binary_data,
                                                                version_to_update=version_to_update)
        sync_client = SyncClient(clearblade_config=clearblade_config)
        response = sync_client.post(api_name="cloudiot_devices", request_params=params, request_body=body)

        if response.status_code == 200:
            return self._create_device_config(response.json())

        return response.json()

    async def modify_cloud_device_config_async(self,
                                               request: ModifyCloudToDeviceConfigRequest,
                                               name:str = None,
                                               version_to_update : int = None,
                                               binary_data: bytes = None):
        if not request.parent:
            raise Exception('Device path must be supplied to the request object.')

        params, body = self._prepare_modify_cloud_config_device(request=request, name=name,
                                                                binary_data=binary_data,
                                                                version_to_update=version_to_update)

        clearblade_config = await self._config_manager.regional_config_async(request.parent)
        async_client = AsyncClient(clearblade_config=clearblade_config)
        response = await async_client.post(api_name="cloudiot_devices",
                                           request_params=params,
                                           request_body=body)
        if response.status_code == 200:
            return self._create_device_config(response.json())
        return response

    def get_device_list_response(self, request:ListDevicesRequest):
        if not request.parent:
            raise Exception('Registry path must be supplied to the request object.')

        clearblade_config = self._config_manager.regional_config(parent=request.parent)

        sync_client = SyncClient(clearblade_config=clearblade_config)

        params = request._prepare_params_for_list()
        response = sync_client.get(api_name="cloudiot_devices",request_params=params)

        if response.status_code == 200:
            return ListDevicesResponse.from_json(response.json())
        return response

    def list(self,
             request: ListDevicesRequest):

        device_list_response = self.get_device_list_response(request=request)
        if device_list_response:
            return ListDevicesPager(method=self.get_device_list_response,
                                    request=request, response=device_list_response)
        return None

    async def get_device_list_async(self, request: ListDevicesRequest):

        if not request.parent:
            raise Exception('Registry path must be supplied to the request object.')

        params = request._prepare_params_for_list()
        clearblade_config = await self._config_manager.regional_config_async(request.parent)
        async_client = AsyncClient(clearblade_config=clearblade_config)
        response = await async_client.get(api_name="cloudiot_devices",request_params=params)

        if response.status_code == 200:
            return ListDevicesResponse.from_json(response.json())
        return response

    async def list_async(self,
                         request: ListDevicesRequest):
        device_list_response = await self.get_device_list_async(request=request)
        if device_list_response:
            return ListDevicesAsyncPager(method=self.get_device_list_async,
                                         request=request, response=device_list_response)
        return None

    def get(self,
            request: GetDeviceRequest) -> Device:

        if not request.parent:
            raise Exception('Device path must be supplied to the request object.')

        clearblade_config = self._config_manager.regional_config(parent=request.parent)

        params = {'name':request.parent}
        sync_client = SyncClient(clearblade_config=clearblade_config)
        response = sync_client.get(api_name="cloudiot_devices", request_params=params)

        if response.status_code == 200:
            return self._create_device_from_response(response.json())
        return response

    async def get_async(self,
                        request: GetDeviceRequest) -> Device:
        if not request.parent:
            raise Exception('Device path must be supplied to the request object.')

        params = {'name':request.parent}
        clearblade_config = await self._config_manager.regional_config_async(request.parent)
        async_client = AsyncClient(clearblade_config=clearblade_config)
        response = await async_client.get(api_name="cloudiot_devices", request_params=params)

        if response.status_code == 200:
            return self._create_device_from_response(response.json())

        return response

    def delete(self,
               request: DeleteDeviceRequest):
        if not request.parent:
            raise Exception('Parent must be supplied to the request object.')

        clearblade_config = self._config_manager.regional_config(parent=request.parent)

        params = {'name':request.parent}

        sync_client = SyncClient(clearblade_config=clearblade_config)
        response = sync_client.delete(api_name="cloudiot_devices",request_params=params)
        return response

    async def delete_async(self,
                           request: DeleteDeviceRequest):

        if not request.parent:
            raise Exception('Device path must be supplied to the request object.')

        params = {'name':request.parent}
        clearblade_config = await self._config_manager.regional_config_async(request.parent)
        async_client = AsyncClient(clearblade_config=clearblade_config)
        response = await async_client.delete(api_name="cloudiot_devices", request_params=params)
        return response

    def update(self,
               request: UpdateDeviceRequest) -> Device:
        if not request.parent:
            raise Exception('Device path must be supplied to the request object.')

        clearblade_config = self._config_manager.regional_config(parent=request.parent)

        params, body = request._prepare_params_body_for_update()
        sync_client = SyncClient(clearblade_config=clearblade_config)
        response = sync_client.patch(api_name="cloudiot_devices",request_body=body, request_params=params)

        if response.status_code == 200:
            return self._create_device_from_response(json_response=response.json())
        return response

    async def update_async(self,
                           request: UpdateDeviceRequest) -> Device:
        if not request.parent:
            raise Exception('Parent must be supplied to the request object.')

        params, body = request._prepare_params_body_for_update()
        clearblade_config = await self._config_manager.regional_config_async(request.parent)
        async_client = AsyncClient(clearblade_config=clearblade_config)
        response = await async_client.patch(api_name="cloudiot_devices",request_body=body, request_params=params)

        if response.status_code == 200:
            return self._create_device_from_response(json_response=response.json())
        return response

    def bindGatewayToDevice(self,
                            request: BindDeviceToGatewayRequest) :
        body = {'deviceId':request.deviceId, 'gatewayId':request.gatewayId}
        params = {'method':'bindDeviceToGateway'}

        if not request.parent:
            raise Exception('Parent must be supplied to the request object.')

        clearblade_config = self._config_manager.regional_config(parent=request.parent)
        sync_client = SyncClient(clearblade_config=clearblade_config)
        response = sync_client.post(api_name="cloudiot", request_params=params, request_body=body)

        return response

    async def bindGatewayToDevice_async(self,
                                        request: BindDeviceToGatewayRequest) :
        if not request.parent:
            raise Exception('Parent must be supplied to the request object.')

        body = {'deviceId':request.deviceId, 'gatewayId':request.gatewayId}
        params = {'method':'bindDeviceToGateway'}
        clearblade_config = await self._config_manager.regional_config_async(request.parent)
        async_client = AsyncClient(clearblade_config=clearblade_config)
        response = await async_client.post(api_name="cloudiot", request_params=params, request_body=body)
        return response

    def unbindGatewayFromDevice(self,
                                request: UnbindDeviceFromGatewayRequest) :
        if not request.parent:
            raise Exception('Parent must be supplied to the request object.')

        clearblade_config = self._config_manager.regional_config(request.parent)
        sync_client = SyncClient(clearblade_config=clearblade_config)
        body = {'deviceId':request.deviceId, 'gatewayId':request.gatewayId}
        params = {'method':'unbindDeviceFromGateway'}
        response = sync_client.post(api_name="cloudiot", request_params=params, request_body=body)
        return response

    async def unbindGatewayFromDevice_async(self,
                                            request: UnbindDeviceFromGatewayRequest) :
        if not request.parent:
            raise Exception('Parent must be supplied to the request object.')

        body = {'deviceId':request.deviceId, 'gatewayId':request.gatewayId}
        params = {'method':'unbindDeviceFromGateway'}

        clearblade_config = await self._config_manager.regional_config_async(request.parent)
        async_client = AsyncClient(clearblade_config=clearblade_config)
        response = await async_client.post(api_name="cloudiot",request_params=params, request_body=body)
        return response

    def states_list(self,
                    request: ListDeviceStatesRequest):
        if not request.parent:
            raise Exception('Device Path must be supplied to the request object.')

        clearblade_config = self._config_manager.regional_config(request.parent)

        params = {'name':request.parent, 'numStates':request.numStates}
        sync_client = SyncClient(clearblade_config=clearblade_config)
        response = sync_client.get(api_name="cloudiot_devices_states",request_params=params)

        if response.status_code == 200:
            return ListDeviceStatesResponse.from_json(response.json())
        return response

    async def states_list_async(self,
                                request: ListDeviceStatesRequest):

        if not request.parent:
            raise Exception('Device Path must be supplied to the request object.')

        params = {'name':request.parent, 'numStates':request.numStates}
        clearblade_config = await self._config_manager.regional_config_async(request.parent)
        async_client = AsyncClient(clearblade_config=clearblade_config)
        response = await async_client.get(api_name="cloudiot_devices_states", request_params=params)

        if response.status_code == 200:
            return ListDeviceStatesResponse.from_json(response.json())
        return response

    def config_versions_list(self,
                             request: ListDeviceConfigVersionsRequest):
        if not request.parent:
            raise Exception('Device Path must be supplied to the request object.')

        clearblade_config = self._config_manager.regional_config(request.parent)
        params = {'name':request.parent, 'numVersions':request.numVersions}
        sync_client = SyncClient(clearblade_config=clearblade_config)
        response = sync_client.get(api_name="cloudiot_devices_configVersions",request_params=params)

        if response.status_code == 200:
            return ListDeviceConfigVersionsResponse.from_json(response.json())
        return response

    async def config_versions_list_async(self,
                                         request: ListDeviceConfigVersionsRequest):
        if not request.parent:
            raise Exception('Device Path must be supplied to the request object.')

        params = {'name':request.parent, 'numVersions':request.numVersions}
        clearblade_config = await self._config_manager.regional_config_async(request.parent)
        async_client = AsyncClient(clearblade_config=clearblade_config)
        response = await async_client.get(api_name="cloudiot_devices_configVersions", request_params=params)

        if response.status_code == 200:
            return ListDeviceConfigVersionsResponse.from_json(response.json())
        return response
