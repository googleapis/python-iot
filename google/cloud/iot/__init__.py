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

from google.cloud.iot_v1.services.device_manager.client import DeviceManagerClient
from google.cloud.iot_v1.services.device_manager.async_client import (
    DeviceManagerAsyncClient,
)

from google.cloud.iot_v1.types.device_manager import BindDeviceToGatewayRequest
from google.cloud.iot_v1.types.device_manager import BindDeviceToGatewayResponse
from google.cloud.iot_v1.types.device_manager import CreateDeviceRegistryRequest
from google.cloud.iot_v1.types.device_manager import CreateDeviceRequest
from google.cloud.iot_v1.types.device_manager import DeleteDeviceRegistryRequest
from google.cloud.iot_v1.types.device_manager import DeleteDeviceRequest
from google.cloud.iot_v1.types.device_manager import GatewayListOptions
from google.cloud.iot_v1.types.device_manager import GetDeviceRegistryRequest
from google.cloud.iot_v1.types.device_manager import GetDeviceRequest
from google.cloud.iot_v1.types.device_manager import ListDeviceConfigVersionsRequest
from google.cloud.iot_v1.types.device_manager import ListDeviceConfigVersionsResponse
from google.cloud.iot_v1.types.device_manager import ListDeviceRegistriesRequest
from google.cloud.iot_v1.types.device_manager import ListDeviceRegistriesResponse
from google.cloud.iot_v1.types.device_manager import ListDevicesRequest
from google.cloud.iot_v1.types.device_manager import ListDevicesResponse
from google.cloud.iot_v1.types.device_manager import ListDeviceStatesRequest
from google.cloud.iot_v1.types.device_manager import ListDeviceStatesResponse
from google.cloud.iot_v1.types.device_manager import ModifyCloudToDeviceConfigRequest
from google.cloud.iot_v1.types.device_manager import SendCommandToDeviceRequest
from google.cloud.iot_v1.types.device_manager import SendCommandToDeviceResponse
from google.cloud.iot_v1.types.device_manager import UnbindDeviceFromGatewayRequest
from google.cloud.iot_v1.types.device_manager import UnbindDeviceFromGatewayResponse
from google.cloud.iot_v1.types.device_manager import UpdateDeviceRegistryRequest
from google.cloud.iot_v1.types.device_manager import UpdateDeviceRequest
from google.cloud.iot_v1.types.resources import Device
from google.cloud.iot_v1.types.resources import DeviceConfig
from google.cloud.iot_v1.types.resources import DeviceCredential
from google.cloud.iot_v1.types.resources import DeviceRegistry
from google.cloud.iot_v1.types.resources import DeviceState
from google.cloud.iot_v1.types.resources import EventNotificationConfig
from google.cloud.iot_v1.types.resources import GatewayConfig
from google.cloud.iot_v1.types.resources import HttpConfig
from google.cloud.iot_v1.types.resources import MqttConfig
from google.cloud.iot_v1.types.resources import PublicKeyCertificate
from google.cloud.iot_v1.types.resources import PublicKeyCredential
from google.cloud.iot_v1.types.resources import RegistryCredential
from google.cloud.iot_v1.types.resources import StateNotificationConfig
from google.cloud.iot_v1.types.resources import X509CertificateDetails
from google.cloud.iot_v1.types.resources import GatewayAuthMethod
from google.cloud.iot_v1.types.resources import GatewayType
from google.cloud.iot_v1.types.resources import HttpState
from google.cloud.iot_v1.types.resources import LogLevel
from google.cloud.iot_v1.types.resources import MqttState
from google.cloud.iot_v1.types.resources import PublicKeyCertificateFormat
from google.cloud.iot_v1.types.resources import PublicKeyFormat

__all__ = (
    "DeviceManagerClient",
    "DeviceManagerAsyncClient",
    "BindDeviceToGatewayRequest",
    "BindDeviceToGatewayResponse",
    "CreateDeviceRegistryRequest",
    "CreateDeviceRequest",
    "DeleteDeviceRegistryRequest",
    "DeleteDeviceRequest",
    "GatewayListOptions",
    "GetDeviceRegistryRequest",
    "GetDeviceRequest",
    "ListDeviceConfigVersionsRequest",
    "ListDeviceConfigVersionsResponse",
    "ListDeviceRegistriesRequest",
    "ListDeviceRegistriesResponse",
    "ListDevicesRequest",
    "ListDevicesResponse",
    "ListDeviceStatesRequest",
    "ListDeviceStatesResponse",
    "ModifyCloudToDeviceConfigRequest",
    "SendCommandToDeviceRequest",
    "SendCommandToDeviceResponse",
    "UnbindDeviceFromGatewayRequest",
    "UnbindDeviceFromGatewayResponse",
    "UpdateDeviceRegistryRequest",
    "UpdateDeviceRequest",
    "Device",
    "DeviceConfig",
    "DeviceCredential",
    "DeviceRegistry",
    "DeviceState",
    "EventNotificationConfig",
    "GatewayConfig",
    "HttpConfig",
    "MqttConfig",
    "PublicKeyCertificate",
    "PublicKeyCredential",
    "RegistryCredential",
    "StateNotificationConfig",
    "X509CertificateDetails",
    "GatewayAuthMethod",
    "GatewayType",
    "HttpState",
    "LogLevel",
    "MqttState",
    "PublicKeyCertificateFormat",
    "PublicKeyFormat",
)
