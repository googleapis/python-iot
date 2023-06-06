"""
"Copyright 2023 ClearBlade Inc."

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Copyright 2018 Google LLC
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Copyright 2023 ClearBlade Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Copyright 2018 Google LLC
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import List
from .resources import GatewayType, LogLevel, PublicKeyFormat, PublicKeyCredential, DeviceCredential
from .utils import get_value
import os
from proto.datetime_helpers import DatetimeWithNanoseconds
import base64

def convertCredentialsFormatsFromString(credentials):
    if credentials is not None:
        # Converts public Key Format from string to object of class PublicKeyFormat
        for index, credential in enumerate(credentials):
            if 'publicKey' in credential:
                credential['publicKey']['format'] = PublicKeyFormat(credential['publicKey']['format'])
                credentials[index] = DeviceCredential(credential['publicKey'], credential['expirationTime'])
    return credentials

class Device():
    """
    Data class for Clearblade Device
    """
    # TODO: find a better way to construct the Device object. I dont like so much parameter in a constructor
    # From google SDK docs: The field ``name`` must be empty. The server generates ``name`` from the device 
    # registry ``id`` and the ``parent`` field.

    def __init__(self, id: str, num_id: str = None,
                 credentials: list = [], last_heartbeat_time: str = None, last_event_time: str = None,
                 last_state_time: str = None, last_config_ack_time: str = None,
                 last_config_send_time: str = None, blocked: bool = False,
                 last_error_time: str = None, last_error_status_code: dict = None,
                 config: dict = {"cloudUpdateTime":None, "version":""} ,
                 state: dict = {"updateTime":None, "binaryData":None},
                 log_level: str = LogLevel.NONE, meta_data: dict = {}, gateway_config : dict = {"gatewayType": GatewayType.NON_GATEWAY}) -> None:

        self._id = id
        self._name = ''
        self._num_id = num_id
        self._credentials = credentials
        self._last_heartbeat_time = last_heartbeat_time
        self._last_event_time = last_event_time
        self._last_state_time = last_state_time
        self._last_config_ack_time = last_config_ack_time
        self._last_config_send_time = last_config_send_time
        self._blocked = blocked
        self._last_error_time = last_error_time
        self._last_error_status_code = last_error_status_code
        self._config = config
        self._state = state
        self._log_level = log_level
        self._meta_data = meta_data
        self._gateway_config = gateway_config

    @staticmethod
    def from_json(json):
        lastHeartbeatTimeFromJson = get_value(json,'lastHeartbeatTime')
        lastEventTimeFromJson = get_value(json, 'lastEventTime')
        lastStateTimeFromJson = get_value(json, 'lastStateTime')
        lastConfigAckTimeFromJson = get_value(json, 'lastConfigAckTime')
        lastConfigSendTimeFromJson = get_value(json, 'lastConfigSendTime')
        lastErrorTimeFromJson = get_value(json, 'lastErrorTime')
        configFromJson = get_value(json, 'config')
        stateFromJson = get_value(json, 'state')
        
        convert_times_to_datetime_with_nanoseconds = (False if os.environ.get("BINARYDATA_AND_TIME_GOOGLE_FORMAT") == None else os.environ.get("BINARYDATA_AND_TIME_GOOGLE_FORMAT").lower() == "true")
        if convert_times_to_datetime_with_nanoseconds:
            last_heartbeat_time = None if lastHeartbeatTimeFromJson in [None, ""] else DatetimeWithNanoseconds.from_rfc3339(lastHeartbeatTimeFromJson)
            last_event_time = None if lastEventTimeFromJson in [None, ""] else DatetimeWithNanoseconds.from_rfc3339(lastEventTimeFromJson)
            last_state_time = None if lastStateTimeFromJson in [None, ""] else DatetimeWithNanoseconds.from_rfc3339(lastStateTimeFromJson)
            last_config_ack_time = None if lastConfigAckTimeFromJson in [None, ""] else DatetimeWithNanoseconds.from_rfc3339(lastConfigAckTimeFromJson)
            last_config_send_time = None if lastConfigSendTimeFromJson in [None, ""] else DatetimeWithNanoseconds.from_rfc3339(lastConfigSendTimeFromJson)
            last_error_time = None if lastErrorTimeFromJson in [None, ""] else DatetimeWithNanoseconds.from_rfc3339(lastErrorTimeFromJson) 
        else:
            last_heartbeat_time = lastHeartbeatTimeFromJson
            last_event_time = lastEventTimeFromJson
            last_state_time = lastStateTimeFromJson
            last_config_ack_time = lastConfigAckTimeFromJson
            last_config_send_time = lastConfigSendTimeFromJson
            last_error_time = lastErrorTimeFromJson

        return Device(
            id=get_value(json, 'id'),
            num_id=get_value(json, 'numId'),
            credentials=convertCredentialsFormatsFromString(get_value(json, 'credentials')),
            last_heartbeat_time=last_heartbeat_time,
            last_event_time=last_event_time,
            last_state_time=last_state_time,
            last_config_ack_time=last_config_ack_time,
            last_config_send_time=last_config_send_time,
            last_error_time=last_error_time,
            blocked=get_value(json, 'blocked'),
            last_error_status_code=get_value(json, 'lastErrorStatus'),
            config=DeviceConfig.from_json(configFromJson),
            state=DeviceState.from_json(stateFromJson),
            log_level=get_value(json, 'logLevel'),
            meta_data=get_value(json, 'metadata'),
            gateway_config=get_value(json, 'gatewayConfig')
        )

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def num_id(self):
        return self._num_id

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        self._credentials = credentials

    @property
    def last_error_status(self):
        return self._last_error_status_code

    @property
    def config(self):
        return self._config

    @property
    def state(self):
        return self._state

    @property
    def log_level(self):
        return self._log_level
    
    @log_level.setter
    def log_level(self, log_level):
        self._log_level = log_level

    @property
    def meta_data(self):
        return self._meta_data

    @meta_data.setter
    def meta_data(self, meta_data):
        self._meta_data = meta_data

    @property
    def gateway_config(self):
        return self._gateway_config

    @gateway_config.setter
    def gateway_config(self, gateway_config):
        self._gateway_config = gateway_config

    @property
    def log_level(self):
        return self._log_level

    @property
    def last_heartbeat_time(self):
        return self._last_heartbeat_time
    
    @property
    def last_event_time(self):
        return self._last_event_time
    
    @property
    def last_state_time(self):
        return self._last_state_time

    @property
    def last_config_ack_time(self):
        return self._last_config_ack_time

    @property
    def last_config_send_time(self):
        return self._last_config_send_time
    
    @property
    def last_error_time(self):
        return self._last_error_time

    @property
    def blocked(self):
        return self._blocked

    @blocked.setter
    def blocked(self, blocked):
        self._blocked = blocked


# classes to mock googles request & response

class DeviceState():
    def __init__(self, update_time: str = None, binary_data:str = None) -> None:
        self.updateTime = update_time
        self.binaryData = binary_data

    def __getitem__(self, arg):
        return getattr(self, arg)

    def get(self, arg):
        return getattr(self, arg)

    @property
    def update_time(self):
        return self.updateTime

    @property
    def binary_data(self):
        return self.binaryData

    @staticmethod
    def from_json(response_json):
        updateTimeFromJson = get_value(response_json, 'updateTime')
        binaryDataFromJson = get_value(response_json, 'binaryData')
        
        convert_times_to_datetime_with_nanoseconds = (False if os.environ.get("BINARYDATA_AND_TIME_GOOGLE_FORMAT") == None else os.environ.get("BINARYDATA_AND_TIME_GOOGLE_FORMAT").lower() == "true")
        if convert_times_to_datetime_with_nanoseconds:
            update_time = None if updateTimeFromJson in [None, ""] else DatetimeWithNanoseconds.from_rfc3339(updateTimeFromJson)
        else:
            update_time = updateTimeFromJson

        if (binaryDataFromJson not in [None, ""]):
            convert_binarydata_to_bytes = (False if os.environ.get("BINARYDATA_AND_TIME_GOOGLE_FORMAT") == None else os.environ.get("BINARYDATA_AND_TIME_GOOGLE_FORMAT").lower() == "true")
            if convert_binarydata_to_bytes:
                binary_data = binaryDataFromJson.encode('utf-8')
            else:
                binary_data = binaryDataFromJson
        else:
            binary_data = binaryDataFromJson

        return DeviceState(update_time=update_time,
                           binary_data=binary_data)
       
class Request():
    def __init__(self, parent) -> None:
        self._parent = parent

    @property
    def parent(self):
        return self._parent


class SendCommandToDeviceRequest(Request):
    def __init__(self, name: str = None,
                 binary_data: bytes = None,
                 subfolder: str = None) -> None:
        super().__init__(name)
        self._binary_data = binary_data
        self._subfolder = subfolder

    @property
    def binary_data(self):
        return self._binary_data

    @property
    def sub_folder(self):
        return self._subfolder


class CreateDeviceRequest(Request):
    def __init__(self, parent: str = None,
                 device: Device = None) -> None:
        super().__init__(parent)
        self._device = device

    @property
    def device(self):
        return self._device


class ModifyCloudToDeviceConfigRequest(Request):
    def __init__(self, name:str = None ,
                 version_to_update: str = "",
                 binary_data: bytes = None) -> None:
        super().__init__(name)
        self._version_to_update = version_to_update
        self._binary_data = binary_data

    @property
    def version_to_update(self):
        return self._version_to_update

    @property
    def binary_data(self):
        return self._binary_data


class DeviceConfig(Request):
    def __init__(self, name,
                 version,
                 cloud_update_time,
                 device_ack_time,
                 binary_data) -> None:
        super().__init__(name)
        self._version = version
        self.cloudUpdateTime = cloud_update_time
        self.deviceAckTime = device_ack_time
        self.binaryData = binary_data

    def __getitem__(self, arg):
        return getattr(self, arg)

    def get(self, arg):
        return getattr(self, arg)

    @property
    def version(self):
        return self._version

    @property
    def cloud_update_time(self):
        return self.cloudUpdateTime

    @property
    def device_ack_time(self):
        return self.deviceAckTime

    @property
    def binary_data(self):
        return self.binaryData

    @staticmethod
    def from_json(json):
        cloudUpdateTimeFromJson = get_value(json,'cloudUpdateTime')
        deviceAckTimeFromJson = get_value(json, 'deviceAckTime')
        binaryDataFromJson = get_value(json,'binaryData')

        convert_times_to_datetime_with_nanoseconds = (False if os.environ.get("BINARYDATA_AND_TIME_GOOGLE_FORMAT") == None else os.environ.get("BINARYDATA_AND_TIME_GOOGLE_FORMAT").lower() == "true")
        if convert_times_to_datetime_with_nanoseconds:
            cloud_update_time = None if cloudUpdateTimeFromJson in [None, ""] else DatetimeWithNanoseconds.from_rfc3339(cloudUpdateTimeFromJson)
            device_ack_time = None if deviceAckTimeFromJson in [None, ""] else DatetimeWithNanoseconds.from_rfc3339(deviceAckTimeFromJson)
        else:
            cloud_update_time = cloudUpdateTimeFromJson
            device_ack_time = deviceAckTimeFromJson
        
        if binaryDataFromJson not in [None, ""]:
            convert_binarydata_to_bytes = (False if os.environ.get("BINARYDATA_AND_TIME_GOOGLE_FORMAT") == None else os.environ.get("BINARYDATA_AND_TIME_GOOGLE_FORMAT").lower() == "true")
            if convert_binarydata_to_bytes:
                binary_data = base64.b64decode(binaryDataFromJson.encode('utf-8'))
            else:
                binary_data = binaryDataFromJson
        else:
            binary_data = binaryDataFromJson

        return DeviceConfig(name='',
                            version=get_value(json, 'version'),
                            cloud_update_time=cloud_update_time,
                            device_ack_time=device_ack_time,
                            binary_data=binary_data)


class DeleteDeviceRequest(Request):
    def __init__(self, name: str = None) -> None:
        super().__init__(name)


class GetDeviceRequest(Request):
    def __init__(self, name: str = None) -> None:
        super().__init__(name)


class BindUnBindGatewayDeviceRequest(Request):
    def __init__(self, parent:str = None,
                 deviceId: str = None,
                 gatewayId: str = None) -> None:
        self._parent = parent
        self._deviceid = deviceId
        self._gatewayid = gatewayId

    @property
    def parent(self):
        return self._parent

    @property
    def deviceId(self):
        return self._deviceid

    @property
    def gatewayId(self):
        return self._gatewayid


class BindDeviceToGatewayRequest(BindUnBindGatewayDeviceRequest):
    def __init__(self, parent: str = None,
                 deviceId: str = None,
                 gatewayId: str = None) -> None:
        super().__init__(parent, deviceId, gatewayId)


class UnbindDeviceFromGatewayRequest(BindUnBindGatewayDeviceRequest):
    def __init__(self, parent: str = None,
                 deviceId: str = None,
                 gatewayId: str = None) -> None:
        super().__init__(parent, deviceId, gatewayId)


class ListDeviceStatesRequest(Request):
    def __init__(self, name: str = None,
                 numStates: int = None) -> None:
        super().__init__(name)
        self._numStates = numStates

    @property
    def numStates(self):
        return self._numStates


class ListDeviceStatesResponse():
    def __init__(self, device_states:List[DeviceState] = []) -> None:
        self._device_states = device_states

    @property
    def device_states(self):
        return self._device_states

    @staticmethod
    def from_json(response_json):
        device_states_json = get_value(response_json, 'deviceStates')
        device_states = []
        for device_state_json in device_states_json:
            device_state = DeviceState.from_json(device_state_json)
            device_states.append(device_state)

        return ListDeviceStatesResponse(device_states=device_states)


class ListDeviceConfigVersionsRequest(Request):
    def __init__(self, name: str = None,
                 numVersions: int = None) -> None:
        super().__init__(name)
        self._numversions = numVersions

    @property
    def numVersions(self):
        return self._numversions


class ListDeviceConfigVersionsResponse():
    def __init__(self, device_configs) -> None:
        self._device_configs = device_configs

    @property
    def device_configs(self):
        return self._device_configs

    @staticmethod
    def from_json(response_json):
        device_configs_json = response_json['deviceConfigs']
        deviceConfigs = []
        for device_config_json in device_configs_json:
            deviceConfig = DeviceConfig.from_json(device_config_json)
            deviceConfigs.append(deviceConfig)

        return ListDeviceConfigVersionsResponse(device_configs=deviceConfigs)


class UpdateDeviceRequest(Request):
    def __init__(self, parent: str = None, device: Device = None, updateMask: str = None) -> None:
        self._parent = parent
        self._device = device
        self._update_mask = updateMask

    def _prepare_params_body_for_update(self):
        params = {'name': self._device.id}
        if self._update_mask is not None:
            params['updateMask'] = self._update_mask

        body = {}
        if self._device.log_level is not None:
            body['logLevel'] = self._device.log_level
        if self._device.gateway_config is not None:
            body['gatewayConfig'] = self._device.gateway_config
        if self._device.meta_data is not None:
            body['metadata'] = self._device.meta_data
        if self._device._blocked is not None:
            body['blocked'] = self._device._blocked
        if self._device._credentials is not None:
            body['credentials'] = DeviceCredential.convert_credentials_for_create_update(self._device._credentials)

        return params, body


class ListDevicesRequest(Request):
    def __init__(self, parent:str = None ,
                 deviceNumIds: str = None,
                 deviceIds: str = None,
                 fieldMask: str = None,
                 gatewayListOptions: dict = None,
                 pageSize: int = None,
                 pageToken: str = None) -> None:
        self._parent = parent
        self._device_num_ids = deviceNumIds
        self._device_ids = deviceIds
        self._field_mask = fieldMask
        self._gateway_list_options = gatewayListOptions
        self._page_size = pageSize
        self._page_token = pageToken

    @property
    def parent(self):
        return self._parent

    @property
    def device_num_ids(self):
        return self._device_num_ids

    @property
    def device_ids(self):
        return self._device_ids

    @property
    def field_mask(self):
        return self._field_mask

    @property
    def gateway_list_options(self):
        return self._gateway_list_options

    @property
    def page_size(self):
        return self._page_size

    @property
    def page_token(self):
        return self._page_token

    @page_token.setter
    def page_token(self, page_token):
        self._page_token = page_token

    def _prepare_params_for_list(self):
        params = {'parent':self.parent}
        if self.page_size:
            params['pageSize'] = self.page_size
        if self.device_num_ids:
            params['deviceNumIds'] = self.device_num_ids
        if self.device_ids:
            params['deviceIds'] = self.device_ids
        if self.field_mask:
            params['fieldMask'] = self.field_mask
        if self.gateway_list_options :
            if 'associationsDeviceId' in self.gateway_list_options:
                params['gatewayListOptions.associationsDeviceId'] = self.gateway_list_options['associationsDeviceId']
            if 'associationsGatewayId' in self.gateway_list_options:
                params['gatewayListOptions.associationsGatewayId'] = self.gateway_list_options['associationsGatewayId']
            if 'gatewayType' in self.gateway_list_options:
                params['gatewayListOptions.gatewayType'] = self.gateway_list_options['gatewayType']
        if self.page_token:
            params['pageToken'] = self.page_token

        return params


class ListDevicesResponse():

    def __init__(self, devices, next_page_token) -> None:
        self._devices = devices
        self._next_page_token = next_page_token

    @property
    def raw_pages(self):
        return self

    @property
    def devices(self):
        return self._devices

    @property
    def next_page_token(self):
        return self._next_page_token

    @staticmethod
    def from_json(devices_list_json):
        devices = []
        next_page_token = None
        if 'devices' in devices_list_json:
            devices_json = devices_list_json['devices']
            for device_json in devices_json:
                device = Device.from_json(device_json)
                devices.append(device)

        if 'nextPageToken' in devices_list_json:
            next_page_token = devices_list_json['nextPageToken']

        return ListDevicesResponse(devices=devices, next_page_token=next_page_token)
