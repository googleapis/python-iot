# -*- coding: utf-8 -*-
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
from google.cloud.iot import gapic_version as package_version

__version__ = package_version.__version__


from .services.device_manager import DeviceManagerAsyncClient, DeviceManagerClient
from .types.device_manager import (
    BindDeviceToGatewayRequest,
    BindDeviceToGatewayResponse,
    CreateDeviceRegistryRequest,
    CreateDeviceRequest,
    DeleteDeviceRegistryRequest,
    DeleteDeviceRequest,
    GatewayListOptions,
    GetDeviceRegistryRequest,
    GetDeviceRequest,
    ListDeviceConfigVersionsRequest,
    ListDeviceConfigVersionsResponse,
    ListDeviceRegistriesRequest,
    ListDeviceRegistriesResponse,
    ListDevicesRequest,
    ListDevicesResponse,
    ListDeviceStatesRequest,
    ListDeviceStatesResponse,
    ModifyCloudToDeviceConfigRequest,
    SendCommandToDeviceRequest,
    SendCommandToDeviceResponse,
    UnbindDeviceFromGatewayRequest,
    UnbindDeviceFromGatewayResponse,
    UpdateDeviceRegistryRequest,
    UpdateDeviceRequest,
)
from .types.resources import (
    Device,
    DeviceConfig,
    DeviceCredential,
    DeviceRegistry,
    DeviceState,
    EventNotificationConfig,
    GatewayAuthMethod,
    GatewayConfig,
    GatewayType,
    HttpConfig,
    HttpState,
    LogLevel,
    MqttConfig,
    MqttState,
    PublicKeyCertificate,
    PublicKeyCertificateFormat,
    PublicKeyCredential,
    PublicKeyFormat,
    RegistryCredential,
    StateNotificationConfig,
    X509CertificateDetails,
)

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
