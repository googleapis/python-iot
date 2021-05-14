# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from .services.device_manager import DeviceManagerClient
from .services.device_manager import DeviceManagerAsyncClient

from .types.device_manager import BindDeviceToGatewayRequest
from .types.device_manager import BindDeviceToGatewayResponse
from .types.device_manager import CreateDeviceRegistryRequest
from .types.device_manager import CreateDeviceRequest
from .types.device_manager import DeleteDeviceRegistryRequest
from .types.device_manager import DeleteDeviceRequest
from .types.device_manager import GatewayListOptions
from .types.device_manager import GetDeviceRegistryRequest
from .types.device_manager import GetDeviceRequest
from .types.device_manager import ListDeviceConfigVersionsRequest
from .types.device_manager import ListDeviceConfigVersionsResponse
from .types.device_manager import ListDeviceRegistriesRequest
from .types.device_manager import ListDeviceRegistriesResponse
from .types.device_manager import ListDevicesRequest
from .types.device_manager import ListDevicesResponse
from .types.device_manager import ListDeviceStatesRequest
from .types.device_manager import ListDeviceStatesResponse
from .types.device_manager import ModifyCloudToDeviceConfigRequest
from .types.device_manager import SendCommandToDeviceRequest
from .types.device_manager import SendCommandToDeviceResponse
from .types.device_manager import UnbindDeviceFromGatewayRequest
from .types.device_manager import UnbindDeviceFromGatewayResponse
from .types.device_manager import UpdateDeviceRegistryRequest
from .types.device_manager import UpdateDeviceRequest
from .types.resources import Device
from .types.resources import DeviceConfig
from .types.resources import DeviceCredential
from .types.resources import DeviceRegistry
from .types.resources import DeviceState
from .types.resources import EventNotificationConfig
from .types.resources import GatewayConfig
from .types.resources import HttpConfig
from .types.resources import MqttConfig
from .types.resources import PublicKeyCertificate
from .types.resources import PublicKeyCredential
from .types.resources import RegistryCredential
from .types.resources import StateNotificationConfig
from .types.resources import X509CertificateDetails
from .types.resources import GatewayAuthMethod
from .types.resources import GatewayType
from .types.resources import HttpState
from .types.resources import LogLevel
from .types.resources import MqttState
from .types.resources import PublicKeyCertificateFormat
from .types.resources import PublicKeyFormat

__all__ = (
    "DeviceManagerAsyncClient",
    "BindDeviceToGatewayRequest",
    "BindDeviceToGatewayResponse",
    "CreateDeviceRegistryRequest",
    "CreateDeviceRequest",
    "DeleteDeviceRegistryRequest",
    "DeleteDeviceRequest",
    "Device",
    "DeviceConfig",
    "DeviceCredential",
    "DeviceManagerClient",
    "DeviceRegistry",
    "DeviceState",
    "EventNotificationConfig",
    "GatewayAuthMethod",
    "GatewayConfig",
    "GatewayListOptions",
    "GatewayType",
    "GetDeviceRegistryRequest",
    "GetDeviceRequest",
    "HttpConfig",
    "HttpState",
    "ListDeviceConfigVersionsRequest",
    "ListDeviceConfigVersionsResponse",
    "ListDeviceRegistriesRequest",
    "ListDeviceRegistriesResponse",
    "ListDeviceStatesRequest",
    "ListDeviceStatesResponse",
    "ListDevicesRequest",
    "ListDevicesResponse",
    "LogLevel",
    "ModifyCloudToDeviceConfigRequest",
    "MqttConfig",
    "MqttState",
    "PublicKeyCertificate",
    "PublicKeyCertificateFormat",
    "PublicKeyCredential",
    "PublicKeyFormat",
    "RegistryCredential",
    "SendCommandToDeviceRequest",
    "SendCommandToDeviceResponse",
    "StateNotificationConfig",
    "UnbindDeviceFromGatewayRequest",
    "UnbindDeviceFromGatewayResponse",
    "UpdateDeviceRegistryRequest",
    "UpdateDeviceRequest",
    "X509CertificateDetails",
)
