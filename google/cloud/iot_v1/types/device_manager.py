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
import proto  # type: ignore

from google.cloud.iot_v1.types import resources
from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.iot.v1",
    manifest={
        "CreateDeviceRegistryRequest",
        "GetDeviceRegistryRequest",
        "DeleteDeviceRegistryRequest",
        "UpdateDeviceRegistryRequest",
        "ListDeviceRegistriesRequest",
        "ListDeviceRegistriesResponse",
        "CreateDeviceRequest",
        "GetDeviceRequest",
        "UpdateDeviceRequest",
        "DeleteDeviceRequest",
        "ListDevicesRequest",
        "GatewayListOptions",
        "ListDevicesResponse",
        "ModifyCloudToDeviceConfigRequest",
        "ListDeviceConfigVersionsRequest",
        "ListDeviceConfigVersionsResponse",
        "ListDeviceStatesRequest",
        "ListDeviceStatesResponse",
        "SendCommandToDeviceRequest",
        "SendCommandToDeviceResponse",
        "BindDeviceToGatewayRequest",
        "BindDeviceToGatewayResponse",
        "UnbindDeviceFromGatewayRequest",
        "UnbindDeviceFromGatewayResponse",
    },
)


class CreateDeviceRegistryRequest(proto.Message):
    r"""Request for ``CreateDeviceRegistry``.
    Attributes:
        parent (str):
            Required. The project and cloud region where this device
            registry must be created. For example,
            ``projects/example-project/locations/us-central1``.
        device_registry (google.cloud.iot_v1.types.DeviceRegistry):
            Required. The device registry. The field ``name`` must be
            empty. The server will generate that field from the device
            registry ``id`` provided and the ``parent`` field.
    """

    parent = proto.Field(proto.STRING, number=1,)
    device_registry = proto.Field(
        proto.MESSAGE, number=2, message=resources.DeviceRegistry,
    )


class GetDeviceRegistryRequest(proto.Message):
    r"""Request for ``GetDeviceRegistry``.
    Attributes:
        name (str):
            Required. The name of the device registry. For example,
            ``projects/example-project/locations/us-central1/registries/my-registry``.
    """

    name = proto.Field(proto.STRING, number=1,)


class DeleteDeviceRegistryRequest(proto.Message):
    r"""Request for ``DeleteDeviceRegistry``.
    Attributes:
        name (str):
            Required. The name of the device registry. For example,
            ``projects/example-project/locations/us-central1/registries/my-registry``.
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateDeviceRegistryRequest(proto.Message):
    r"""Request for ``UpdateDeviceRegistry``.
    Attributes:
        device_registry (google.cloud.iot_v1.types.DeviceRegistry):
            Required. The new values for the device registry. The ``id``
            field must be empty, and the ``name`` field must indicate
            the path of the resource. For example,
            ``projects/example-project/locations/us-central1/registries/my-registry``.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Only updates the ``device_registry`` fields
            indicated by this mask. The field mask must not be empty,
            and it must not contain fields that are immutable or only
            set by the server. Mutable top-level fields:
            ``event_notification_config``, ``http_config``,
            ``mqtt_config``, and ``state_notification_config``.
    """

    device_registry = proto.Field(
        proto.MESSAGE, number=1, message=resources.DeviceRegistry,
    )
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class ListDeviceRegistriesRequest(proto.Message):
    r"""Request for ``ListDeviceRegistries``.
    Attributes:
        parent (str):
            Required. The project and cloud region path. For example,
            ``projects/example-project/locations/us-central1``.
        page_size (int):
            The maximum number of registries to return in the response.
            If this value is zero, the service will select a default
            size. A call may return fewer objects than requested. A
            non-empty ``next_page_token`` in the response indicates that
            more data is available.
        page_token (str):
            The value returned by the last
            ``ListDeviceRegistriesResponse``; indicates that this is a
            continuation of a prior ``ListDeviceRegistries`` call and
            the system should return the next page of data.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListDeviceRegistriesResponse(proto.Message):
    r"""Response for ``ListDeviceRegistries``.
    Attributes:
        device_registries (Sequence[google.cloud.iot_v1.types.DeviceRegistry]):
            The registries that matched the query.
        next_page_token (str):
            If not empty, indicates that there may be more registries
            that match the request; this value should be passed in a new
            ``ListDeviceRegistriesRequest``.
    """

    @property
    def raw_page(self):
        return self

    device_registries = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.DeviceRegistry,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class CreateDeviceRequest(proto.Message):
    r"""Request for ``CreateDevice``.
    Attributes:
        parent (str):
            Required. The name of the device registry where this device
            should be created. For example,
            ``projects/example-project/locations/us-central1/registries/my-registry``.
        device (google.cloud.iot_v1.types.Device):
            Required. The device registration details. The field
            ``name`` must be empty. The server generates ``name`` from
            the device registry ``id`` and the ``parent`` field.
    """

    parent = proto.Field(proto.STRING, number=1,)
    device = proto.Field(proto.MESSAGE, number=2, message=resources.Device,)


class GetDeviceRequest(proto.Message):
    r"""Request for ``GetDevice``.
    Attributes:
        name (str):
            Required. The name of the device. For example,
            ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
            or
            ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.
        field_mask (google.protobuf.field_mask_pb2.FieldMask):
            The fields of the ``Device`` resource to be returned in the
            response. If the field mask is unset or empty, all fields
            are returned. Fields have to be provided in snake_case
            format, for example: ``last_heartbeat_time``.
    """

    name = proto.Field(proto.STRING, number=1,)
    field_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,)


class UpdateDeviceRequest(proto.Message):
    r"""Request for ``UpdateDevice``.
    Attributes:
        device (google.cloud.iot_v1.types.Device):
            Required. The new values for the device. The ``id`` and
            ``num_id`` fields must be empty, and the field ``name`` must
            specify the name path. For example,
            ``projects/p0/locations/us-central1/registries/registry0/devices/device0``\ or
            ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Only updates the ``device`` fields indicated by
            this mask. The field mask must not be empty, and it must not
            contain fields that are immutable or only set by the server.
            Mutable top-level fields: ``credentials``, ``blocked``, and
            ``metadata``
    """

    device = proto.Field(proto.MESSAGE, number=2, message=resources.Device,)
    update_mask = proto.Field(
        proto.MESSAGE, number=3, message=field_mask_pb2.FieldMask,
    )


class DeleteDeviceRequest(proto.Message):
    r"""Request for ``DeleteDevice``.
    Attributes:
        name (str):
            Required. The name of the device. For example,
            ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
            or
            ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.
    """

    name = proto.Field(proto.STRING, number=1,)


class ListDevicesRequest(proto.Message):
    r"""Request for ``ListDevices``.
    Attributes:
        parent (str):
            Required. The device registry path. Required. For example,
            ``projects/my-project/locations/us-central1/registries/my-registry``.
        device_num_ids (Sequence[int]):
            A list of device numeric IDs. If empty, this
            field is ignored. Maximum IDs: 10,000.
        device_ids (Sequence[str]):
            A list of device string IDs. For example,
            ``['device0', 'device12']``. If empty, this field is
            ignored. Maximum IDs: 10,000
        field_mask (google.protobuf.field_mask_pb2.FieldMask):
            The fields of the ``Device`` resource to be returned in the
            response. The fields ``id`` and ``num_id`` are always
            returned, along with any other fields specified in
            snake_case format, for example: ``last_heartbeat_time``.
        gateway_list_options (google.cloud.iot_v1.types.GatewayListOptions):
            Options related to gateways.
        page_size (int):
            The maximum number of devices to return in the response. If
            this value is zero, the service will select a default size.
            A call may return fewer objects than requested. A non-empty
            ``next_page_token`` in the response indicates that more data
            is available.
        page_token (str):
            The value returned by the last ``ListDevicesResponse``;
            indicates that this is a continuation of a prior
            ``ListDevices`` call and the system should return the next
            page of data.
    """

    parent = proto.Field(proto.STRING, number=1,)
    device_num_ids = proto.RepeatedField(proto.UINT64, number=2,)
    device_ids = proto.RepeatedField(proto.STRING, number=3,)
    field_mask = proto.Field(proto.MESSAGE, number=4, message=field_mask_pb2.FieldMask,)
    gateway_list_options = proto.Field(
        proto.MESSAGE, number=6, message="GatewayListOptions",
    )
    page_size = proto.Field(proto.INT32, number=100,)
    page_token = proto.Field(proto.STRING, number=101,)


class GatewayListOptions(proto.Message):
    r"""Options for limiting the list based on gateway type and
    associations.

    Attributes:
        gateway_type (google.cloud.iot_v1.types.GatewayType):
            If ``GATEWAY`` is specified, only gateways are returned. If
            ``NON_GATEWAY`` is specified, only non-gateway devices are
            returned. If ``GATEWAY_TYPE_UNSPECIFIED`` is specified, all
            devices are returned.
        associations_gateway_id (str):
            If set, only devices associated with the specified gateway
            are returned. The gateway ID can be numeric (``num_id``) or
            the user-defined string (``id``). For example, if ``123`` is
            specified, only devices bound to the gateway with ``num_id``
            123 are returned.
        associations_device_id (str):
            If set, returns only the gateways with which the specified
            device is associated. The device ID can be numeric
            (``num_id``) or the user-defined string (``id``). For
            example, if ``456`` is specified, returns only the gateways
            to which the device with ``num_id`` 456 is bound.
    """

    gateway_type = proto.Field(
        proto.ENUM, number=1, oneof="filter", enum=resources.GatewayType,
    )
    associations_gateway_id = proto.Field(proto.STRING, number=2, oneof="filter",)
    associations_device_id = proto.Field(proto.STRING, number=3, oneof="filter",)


class ListDevicesResponse(proto.Message):
    r"""Response for ``ListDevices``.
    Attributes:
        devices (Sequence[google.cloud.iot_v1.types.Device]):
            The devices that match the request.
        next_page_token (str):
            If not empty, indicates that there may be more devices that
            match the request; this value should be passed in a new
            ``ListDevicesRequest``.
    """

    @property
    def raw_page(self):
        return self

    devices = proto.RepeatedField(proto.MESSAGE, number=1, message=resources.Device,)
    next_page_token = proto.Field(proto.STRING, number=2,)


class ModifyCloudToDeviceConfigRequest(proto.Message):
    r"""Request for ``ModifyCloudToDeviceConfig``.
    Attributes:
        name (str):
            Required. The name of the device. For example,
            ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
            or
            ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.
        version_to_update (int):
            The version number to update. If this value
            is zero, it will not check the version number of
            the server and will always update the current
            version; otherwise, this update will fail if the
            version number found on the server does not
            match this version number. This is used to
            support multiple simultaneous updates without
            losing data.
        binary_data (bytes):
            Required. The configuration data for the
            device.
    """

    name = proto.Field(proto.STRING, number=1,)
    version_to_update = proto.Field(proto.INT64, number=2,)
    binary_data = proto.Field(proto.BYTES, number=3,)


class ListDeviceConfigVersionsRequest(proto.Message):
    r"""Request for ``ListDeviceConfigVersions``.
    Attributes:
        name (str):
            Required. The name of the device. For example,
            ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
            or
            ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.
        num_versions (int):
            The number of versions to list. Versions are
            listed in decreasing order of the version
            number. The maximum number of versions retained
            is 10. If this value is zero, it will return all
            the versions available.
    """

    name = proto.Field(proto.STRING, number=1,)
    num_versions = proto.Field(proto.INT32, number=2,)


class ListDeviceConfigVersionsResponse(proto.Message):
    r"""Response for ``ListDeviceConfigVersions``.
    Attributes:
        device_configs (Sequence[google.cloud.iot_v1.types.DeviceConfig]):
            The device configuration for the last few
            versions. Versions are listed in decreasing
            order, starting from the most recent one.
    """

    device_configs = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.DeviceConfig,
    )


class ListDeviceStatesRequest(proto.Message):
    r"""Request for ``ListDeviceStates``.
    Attributes:
        name (str):
            Required. The name of the device. For example,
            ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
            or
            ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.
        num_states (int):
            The number of states to list. States are
            listed in descending order of update time. The
            maximum number of states retained is 10. If this
            value is zero, it will return all the states
            available.
    """

    name = proto.Field(proto.STRING, number=1,)
    num_states = proto.Field(proto.INT32, number=2,)


class ListDeviceStatesResponse(proto.Message):
    r"""Response for ``ListDeviceStates``.
    Attributes:
        device_states (Sequence[google.cloud.iot_v1.types.DeviceState]):
            The last few device states. States are listed
            in descending order of server update time,
            starting from the most recent one.
    """

    device_states = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.DeviceState,
    )


class SendCommandToDeviceRequest(proto.Message):
    r"""Request for ``SendCommandToDevice``.
    Attributes:
        name (str):
            Required. The name of the device. For example,
            ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
            or
            ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.
        binary_data (bytes):
            Required. The command data to send to the
            device.
        subfolder (str):
            Optional subfolder for the command. If empty,
            the command will be delivered to the
            /devices/{device-id}/commands topic, otherwise
            it will be delivered to the /devices/{device-
            id}/commands/{subfolder} topic. Multi-level
            subfolders are allowed. This field must not have
            more than 256 characters, and must not contain
            any MQTT wildcards ("+" or "#") or null
            characters.
    """

    name = proto.Field(proto.STRING, number=1,)
    binary_data = proto.Field(proto.BYTES, number=2,)
    subfolder = proto.Field(proto.STRING, number=3,)


class SendCommandToDeviceResponse(proto.Message):
    r"""Response for ``SendCommandToDevice``.    """


class BindDeviceToGatewayRequest(proto.Message):
    r"""Request for ``BindDeviceToGateway``.
    Attributes:
        parent (str):
            Required. The name of the registry. For example,
            ``projects/example-project/locations/us-central1/registries/my-registry``.
        gateway_id (str):
            Required. The value of ``gateway_id`` can be either the
            device numeric ID or the user-defined device identifier.
        device_id (str):
            Required. The device to associate with the specified
            gateway. The value of ``device_id`` can be either the device
            numeric ID or the user-defined device identifier.
    """

    parent = proto.Field(proto.STRING, number=1,)
    gateway_id = proto.Field(proto.STRING, number=2,)
    device_id = proto.Field(proto.STRING, number=3,)


class BindDeviceToGatewayResponse(proto.Message):
    r"""Response for ``BindDeviceToGateway``.    """


class UnbindDeviceFromGatewayRequest(proto.Message):
    r"""Request for ``UnbindDeviceFromGateway``.
    Attributes:
        parent (str):
            Required. The name of the registry. For example,
            ``projects/example-project/locations/us-central1/registries/my-registry``.
        gateway_id (str):
            Required. The value of ``gateway_id`` can be either the
            device numeric ID or the user-defined device identifier.
        device_id (str):
            Required. The device to disassociate from the specified
            gateway. The value of ``device_id`` can be either the device
            numeric ID or the user-defined device identifier.
    """

    parent = proto.Field(proto.STRING, number=1,)
    gateway_id = proto.Field(proto.STRING, number=2,)
    device_id = proto.Field(proto.STRING, number=3,)


class UnbindDeviceFromGatewayResponse(proto.Message):
    r"""Response for ``UnbindDeviceFromGateway``.    """


__all__ = tuple(sorted(__protobuf__.manifest))
