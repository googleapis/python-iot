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
import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1  # type: ignore
from google.api_core import grpc_helpers_async  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
import packaging.version

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.iot_v1.types import device_manager
from google.cloud.iot_v1.types import resources
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from .base import DeviceManagerTransport, DEFAULT_CLIENT_INFO
from .grpc import DeviceManagerGrpcTransport


class DeviceManagerGrpcAsyncIOTransport(DeviceManagerTransport):
    """gRPC AsyncIO backend transport for DeviceManager.

    Internet of Things (IoT) service. Securely connect and manage
    IoT devices.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "cloudiot.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "cloudiot.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def create_device_registry(
        self,
    ) -> Callable[
        [device_manager.CreateDeviceRegistryRequest],
        Awaitable[resources.DeviceRegistry],
    ]:
        r"""Return a callable for the create device registry method over gRPC.

        Creates a device registry that contains devices.

        Returns:
            Callable[[~.CreateDeviceRegistryRequest],
                    Awaitable[~.DeviceRegistry]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_device_registry" not in self._stubs:
            self._stubs["create_device_registry"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/CreateDeviceRegistry",
                request_serializer=device_manager.CreateDeviceRegistryRequest.serialize,
                response_deserializer=resources.DeviceRegistry.deserialize,
            )
        return self._stubs["create_device_registry"]

    @property
    def get_device_registry(
        self,
    ) -> Callable[
        [device_manager.GetDeviceRegistryRequest], Awaitable[resources.DeviceRegistry]
    ]:
        r"""Return a callable for the get device registry method over gRPC.

        Gets a device registry configuration.

        Returns:
            Callable[[~.GetDeviceRegistryRequest],
                    Awaitable[~.DeviceRegistry]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_device_registry" not in self._stubs:
            self._stubs["get_device_registry"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/GetDeviceRegistry",
                request_serializer=device_manager.GetDeviceRegistryRequest.serialize,
                response_deserializer=resources.DeviceRegistry.deserialize,
            )
        return self._stubs["get_device_registry"]

    @property
    def update_device_registry(
        self,
    ) -> Callable[
        [device_manager.UpdateDeviceRegistryRequest],
        Awaitable[resources.DeviceRegistry],
    ]:
        r"""Return a callable for the update device registry method over gRPC.

        Updates a device registry configuration.

        Returns:
            Callable[[~.UpdateDeviceRegistryRequest],
                    Awaitable[~.DeviceRegistry]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_device_registry" not in self._stubs:
            self._stubs["update_device_registry"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/UpdateDeviceRegistry",
                request_serializer=device_manager.UpdateDeviceRegistryRequest.serialize,
                response_deserializer=resources.DeviceRegistry.deserialize,
            )
        return self._stubs["update_device_registry"]

    @property
    def delete_device_registry(
        self,
    ) -> Callable[
        [device_manager.DeleteDeviceRegistryRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete device registry method over gRPC.

        Deletes a device registry configuration.

        Returns:
            Callable[[~.DeleteDeviceRegistryRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_device_registry" not in self._stubs:
            self._stubs["delete_device_registry"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/DeleteDeviceRegistry",
                request_serializer=device_manager.DeleteDeviceRegistryRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_device_registry"]

    @property
    def list_device_registries(
        self,
    ) -> Callable[
        [device_manager.ListDeviceRegistriesRequest],
        Awaitable[device_manager.ListDeviceRegistriesResponse],
    ]:
        r"""Return a callable for the list device registries method over gRPC.

        Lists device registries.

        Returns:
            Callable[[~.ListDeviceRegistriesRequest],
                    Awaitable[~.ListDeviceRegistriesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_device_registries" not in self._stubs:
            self._stubs["list_device_registries"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/ListDeviceRegistries",
                request_serializer=device_manager.ListDeviceRegistriesRequest.serialize,
                response_deserializer=device_manager.ListDeviceRegistriesResponse.deserialize,
            )
        return self._stubs["list_device_registries"]

    @property
    def create_device(
        self,
    ) -> Callable[[device_manager.CreateDeviceRequest], Awaitable[resources.Device]]:
        r"""Return a callable for the create device method over gRPC.

        Creates a device in a device registry.

        Returns:
            Callable[[~.CreateDeviceRequest],
                    Awaitable[~.Device]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_device" not in self._stubs:
            self._stubs["create_device"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/CreateDevice",
                request_serializer=device_manager.CreateDeviceRequest.serialize,
                response_deserializer=resources.Device.deserialize,
            )
        return self._stubs["create_device"]

    @property
    def get_device(
        self,
    ) -> Callable[[device_manager.GetDeviceRequest], Awaitable[resources.Device]]:
        r"""Return a callable for the get device method over gRPC.

        Gets details about a device.

        Returns:
            Callable[[~.GetDeviceRequest],
                    Awaitable[~.Device]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_device" not in self._stubs:
            self._stubs["get_device"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/GetDevice",
                request_serializer=device_manager.GetDeviceRequest.serialize,
                response_deserializer=resources.Device.deserialize,
            )
        return self._stubs["get_device"]

    @property
    def update_device(
        self,
    ) -> Callable[[device_manager.UpdateDeviceRequest], Awaitable[resources.Device]]:
        r"""Return a callable for the update device method over gRPC.

        Updates a device.

        Returns:
            Callable[[~.UpdateDeviceRequest],
                    Awaitable[~.Device]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_device" not in self._stubs:
            self._stubs["update_device"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/UpdateDevice",
                request_serializer=device_manager.UpdateDeviceRequest.serialize,
                response_deserializer=resources.Device.deserialize,
            )
        return self._stubs["update_device"]

    @property
    def delete_device(
        self,
    ) -> Callable[[device_manager.DeleteDeviceRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete device method over gRPC.

        Deletes a device.

        Returns:
            Callable[[~.DeleteDeviceRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_device" not in self._stubs:
            self._stubs["delete_device"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/DeleteDevice",
                request_serializer=device_manager.DeleteDeviceRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_device"]

    @property
    def list_devices(
        self,
    ) -> Callable[
        [device_manager.ListDevicesRequest],
        Awaitable[device_manager.ListDevicesResponse],
    ]:
        r"""Return a callable for the list devices method over gRPC.

        List devices in a device registry.

        Returns:
            Callable[[~.ListDevicesRequest],
                    Awaitable[~.ListDevicesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_devices" not in self._stubs:
            self._stubs["list_devices"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/ListDevices",
                request_serializer=device_manager.ListDevicesRequest.serialize,
                response_deserializer=device_manager.ListDevicesResponse.deserialize,
            )
        return self._stubs["list_devices"]

    @property
    def modify_cloud_to_device_config(
        self,
    ) -> Callable[
        [device_manager.ModifyCloudToDeviceConfigRequest],
        Awaitable[resources.DeviceConfig],
    ]:
        r"""Return a callable for the modify cloud to device config method over gRPC.

        Modifies the configuration for the device, which is
        eventually sent from the Cloud IoT Core servers. Returns
        the modified configuration version and its metadata.

        Returns:
            Callable[[~.ModifyCloudToDeviceConfigRequest],
                    Awaitable[~.DeviceConfig]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "modify_cloud_to_device_config" not in self._stubs:
            self._stubs[
                "modify_cloud_to_device_config"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/ModifyCloudToDeviceConfig",
                request_serializer=device_manager.ModifyCloudToDeviceConfigRequest.serialize,
                response_deserializer=resources.DeviceConfig.deserialize,
            )
        return self._stubs["modify_cloud_to_device_config"]

    @property
    def list_device_config_versions(
        self,
    ) -> Callable[
        [device_manager.ListDeviceConfigVersionsRequest],
        Awaitable[device_manager.ListDeviceConfigVersionsResponse],
    ]:
        r"""Return a callable for the list device config versions method over gRPC.

        Lists the last few versions of the device
        configuration in descending order (i.e.: newest first).

        Returns:
            Callable[[~.ListDeviceConfigVersionsRequest],
                    Awaitable[~.ListDeviceConfigVersionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_device_config_versions" not in self._stubs:
            self._stubs["list_device_config_versions"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/ListDeviceConfigVersions",
                request_serializer=device_manager.ListDeviceConfigVersionsRequest.serialize,
                response_deserializer=device_manager.ListDeviceConfigVersionsResponse.deserialize,
            )
        return self._stubs["list_device_config_versions"]

    @property
    def list_device_states(
        self,
    ) -> Callable[
        [device_manager.ListDeviceStatesRequest],
        Awaitable[device_manager.ListDeviceStatesResponse],
    ]:
        r"""Return a callable for the list device states method over gRPC.

        Lists the last few versions of the device state in
        descending order (i.e.: newest first).

        Returns:
            Callable[[~.ListDeviceStatesRequest],
                    Awaitable[~.ListDeviceStatesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_device_states" not in self._stubs:
            self._stubs["list_device_states"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/ListDeviceStates",
                request_serializer=device_manager.ListDeviceStatesRequest.serialize,
                response_deserializer=device_manager.ListDeviceStatesResponse.deserialize,
            )
        return self._stubs["list_device_states"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the set iam policy method over gRPC.

        Sets the access control policy on the specified
        resource. Replaces any existing policy.

        Returns:
            Callable[[~.SetIamPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_iam_policy" not in self._stubs:
            self._stubs["set_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/SetIamPolicy",
                request_serializer=iam_policy_pb2.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the get iam policy method over gRPC.

        Gets the access control policy for a resource.
        Returns an empty policy if the resource exists and does
        not have a policy set.

        Returns:
            Callable[[~.GetIamPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_iam_policy" not in self._stubs:
            self._stubs["get_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/GetIamPolicy",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.

        Returns permissions that a caller has on the specified resource.
        If the resource does not exist, this will return an empty set of
        permissions, not a NOT_FOUND error.

        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    Awaitable[~.TestIamPermissionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "test_iam_permissions" not in self._stubs:
            self._stubs["test_iam_permissions"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/TestIamPermissions",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]

    @property
    def send_command_to_device(
        self,
    ) -> Callable[
        [device_manager.SendCommandToDeviceRequest],
        Awaitable[device_manager.SendCommandToDeviceResponse],
    ]:
        r"""Return a callable for the send command to device method over gRPC.

        Sends a command to the specified device. In order for a device
        to be able to receive commands, it must:

        1) be connected to Cloud IoT Core using the MQTT protocol, and
        2) be subscribed to the group of MQTT topics specified by
           /devices/{device-id}/commands/#. This subscription will
           receive commands at the top-level topic
           /devices/{device-id}/commands as well as commands for
           subfolders, like /devices/{device-id}/commands/subfolder.
           Note that subscribing to specific subfolders is not
           supported. If the command could not be delivered to the
           device, this method will return an error; in particular, if
           the device is not subscribed, this method will return
           FAILED_PRECONDITION. Otherwise, this method will return OK.
           If the subscription is QoS 1, at least once delivery will be
           guaranteed; for QoS 0, no acknowledgment will be expected
           from the device.

        Returns:
            Callable[[~.SendCommandToDeviceRequest],
                    Awaitable[~.SendCommandToDeviceResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "send_command_to_device" not in self._stubs:
            self._stubs["send_command_to_device"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/SendCommandToDevice",
                request_serializer=device_manager.SendCommandToDeviceRequest.serialize,
                response_deserializer=device_manager.SendCommandToDeviceResponse.deserialize,
            )
        return self._stubs["send_command_to_device"]

    @property
    def bind_device_to_gateway(
        self,
    ) -> Callable[
        [device_manager.BindDeviceToGatewayRequest],
        Awaitable[device_manager.BindDeviceToGatewayResponse],
    ]:
        r"""Return a callable for the bind device to gateway method over gRPC.

        Associates the device with the gateway.

        Returns:
            Callable[[~.BindDeviceToGatewayRequest],
                    Awaitable[~.BindDeviceToGatewayResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "bind_device_to_gateway" not in self._stubs:
            self._stubs["bind_device_to_gateway"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/BindDeviceToGateway",
                request_serializer=device_manager.BindDeviceToGatewayRequest.serialize,
                response_deserializer=device_manager.BindDeviceToGatewayResponse.deserialize,
            )
        return self._stubs["bind_device_to_gateway"]

    @property
    def unbind_device_from_gateway(
        self,
    ) -> Callable[
        [device_manager.UnbindDeviceFromGatewayRequest],
        Awaitable[device_manager.UnbindDeviceFromGatewayResponse],
    ]:
        r"""Return a callable for the unbind device from gateway method over gRPC.

        Deletes the association between the device and the
        gateway.

        Returns:
            Callable[[~.UnbindDeviceFromGatewayRequest],
                    Awaitable[~.UnbindDeviceFromGatewayResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "unbind_device_from_gateway" not in self._stubs:
            self._stubs["unbind_device_from_gateway"] = self.grpc_channel.unary_unary(
                "/google.cloud.iot.v1.DeviceManager/UnbindDeviceFromGateway",
                request_serializer=device_manager.UnbindDeviceFromGatewayRequest.serialize,
                response_deserializer=device_manager.UnbindDeviceFromGatewayResponse.deserialize,
            )
        return self._stubs["unbind_device_from_gateway"]


__all__ = ("DeviceManagerGrpcAsyncIOTransport",)
