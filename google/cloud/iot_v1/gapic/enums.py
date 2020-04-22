# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrappers for protocol buffer enum types."""

import enum


class GatewayAuthMethod(enum.IntEnum):
    """
    The gateway authorization/authentication method. This setting determines how
    Cloud IoT Core authorizes/authenticate devices to access the gateway.

    Attributes:
      GATEWAY_AUTH_METHOD_UNSPECIFIED (int): No authentication/authorization method specified. No devices are allowed to
      access the gateway.
      ASSOCIATION_ONLY (int): The device is authenticated through the gateway association only. Device
      credentials are ignored even if provided.
      DEVICE_AUTH_TOKEN_ONLY (int): The device is authenticated through its own credentials. Gateway
      association is not checked.
      ASSOCIATION_AND_DEVICE_AUTH_TOKEN (int): The device is authenticated through both device credentials and gateway
      association. The device must be bound to the gateway and must provide its
      own credentials.
    """

    GATEWAY_AUTH_METHOD_UNSPECIFIED = 0
    ASSOCIATION_ONLY = 1
    DEVICE_AUTH_TOKEN_ONLY = 2
    ASSOCIATION_AND_DEVICE_AUTH_TOKEN = 3


class GatewayType(enum.IntEnum):
    """
    Gateway type.

    Attributes:
      GATEWAY_TYPE_UNSPECIFIED (int): If unspecified, the device is considered a non-gateway device.
      GATEWAY (int): The device is a gateway.
      NON_GATEWAY (int): The device is not a gateway.
    """

    GATEWAY_TYPE_UNSPECIFIED = 0
    GATEWAY = 1
    NON_GATEWAY = 2


class HttpState(enum.IntEnum):
    """
    Indicates whether DeviceService (HTTP) is enabled or disabled for the
    registry. See the field description for details.

    Attributes:
      HTTP_STATE_UNSPECIFIED (int): No HTTP state specified. If not specified, DeviceService will be
      enabled by default.
      HTTP_ENABLED (int): Enables DeviceService (HTTP) service for the registry.
      HTTP_DISABLED (int): Disables DeviceService (HTTP) service for the registry.
    """

    HTTP_STATE_UNSPECIFIED = 0
    HTTP_ENABLED = 1
    HTTP_DISABLED = 2


class LogLevel(enum.IntEnum):
    """
    Required. The name of the registry. For example,
    ``projects/example-project/locations/us-central1/registries/my-registry``.

    Attributes:
      LOG_LEVEL_UNSPECIFIED (int): No logging specified. If not specified, logging will be disabled.
      NONE (int): Disables logging.
      ERROR (int): Error events will be logged.
      INFO (int): Informational events will be logged, such as connections and
      disconnections.
      DEBUG (int): All events will be logged.
    """

    LOG_LEVEL_UNSPECIFIED = 0
    NONE = 10
    ERROR = 20
    INFO = 30
    DEBUG = 40


class MqttState(enum.IntEnum):
    """
    Indicates whether an MQTT connection is enabled or disabled. See the field
    description for details.

    Attributes:
      MQTT_STATE_UNSPECIFIED (int): No MQTT state specified. If not specified, MQTT will be enabled by default.
      MQTT_ENABLED (int): Enables a MQTT connection.
      MQTT_DISABLED (int): Disables a MQTT connection.
    """

    MQTT_STATE_UNSPECIFIED = 0
    MQTT_ENABLED = 1
    MQTT_DISABLED = 2


class PublicKeyCertificateFormat(enum.IntEnum):
    """
    The supported formats for the public key.

    Attributes:
      UNSPECIFIED_PUBLIC_KEY_CERTIFICATE_FORMAT (int): The format has not been specified. This is an invalid default value and
      must not be used.
      X509_CERTIFICATE_PEM (int): Required. The name of the device registry. For example,
      ``projects/example-project/locations/us-central1/registries/my-registry``.
    """

    UNSPECIFIED_PUBLIC_KEY_CERTIFICATE_FORMAT = 0
    X509_CERTIFICATE_PEM = 1


class PublicKeyFormat(enum.IntEnum):
    """
    The supported formats for the public key.

    Attributes:
      UNSPECIFIED_PUBLIC_KEY_FORMAT (int): The format has not been specified. This is an invalid default value and
      must not be used.
      RSA_PEM (int): Required. The value of ``gateway_id`` can be either the device
      numeric ID or the user-defined device identifier.
      RSA_X509_PEM (int): Response message for ``TestIamPermissions`` method.
      ES256_PEM (int): A subset of ``TestPermissionsRequest.permissions`` that the caller
      is allowed.
      ES256_X509_PEM (int): Request for ``DeleteDeviceRegistry``.
    """

    UNSPECIFIED_PUBLIC_KEY_FORMAT = 0
    RSA_PEM = 3
    RSA_X509_PEM = 1
    ES256_PEM = 2
    ES256_X509_PEM = 4
