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

from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore


import grpc  # type: ignore

from google.cloud.iot_v1.types import device_manager
from google.cloud.iot_v1.types import resources
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import DeviceManagerTransport, DEFAULT_CLIENT_INFO


class DeviceManagerGrpcTransport(DeviceManagerTransport):
    """gRPC backend transport for DeviceManager.

    Internet of Things (IoT) service. Securely connect and manage
    IoT devices.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "cloudiot.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )

        self._stubs = {}  # type: Dict[str, Callable]

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
            client_info=client_info,
        )

    @classmethod
    def create_channel(
        cls,
        host: str = "cloudiot.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials,
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def create_device_registry(
        self,
    ) -> Callable[
        [device_manager.CreateDeviceRegistryRequest], resources.DeviceRegistry
    ]:
        r"""Return a callable for the create device registry method over gRPC.

        Creates a device registry that contains devices.

        Returns:
            Callable[[~.CreateDeviceRegistryRequest],
                    ~.DeviceRegistry]:
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
    ) -> Callable[[device_manager.GetDeviceRegistryRequest], resources.DeviceRegistry]:
        r"""Return a callable for the get device registry method over gRPC.

        Gets a device registry configuration.

        Returns:
            Callable[[~.GetDeviceRegistryRequest],
                    ~.DeviceRegistry]:
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
        [device_manager.UpdateDeviceRegistryRequest], resources.DeviceRegistry
    ]:
        r"""Return a callable for the update device registry method over gRPC.

        Updates a device registry configuration.

        Returns:
            Callable[[~.UpdateDeviceRegistryRequest],
                    ~.DeviceRegistry]:
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
    ) -> Callable[[device_manager.DeleteDeviceRegistryRequest], empty.Empty]:
        r"""Return a callable for the delete device registry method over gRPC.

        Deletes a device registry configuration.

        Returns:
            Callable[[~.DeleteDeviceRegistryRequest],
                    ~.Empty]:
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
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_device_registry"]

    @property
    def list_device_registries(
        self,
    ) -> Callable[
        [device_manager.ListDeviceRegistriesRequest],
        device_manager.ListDeviceRegistriesResponse,
    ]:
        r"""Return a callable for the list device registries method over gRPC.

        Lists device registries.

        Returns:
            Callable[[~.ListDeviceRegistriesRequest],
                    ~.ListDeviceRegistriesResponse]:
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
    ) -> Callable[[device_manager.CreateDeviceRequest], resources.Device]:
        r"""Return a callable for the create device method over gRPC.

        Creates a device in a device registry.

        Returns:
            Callable[[~.CreateDeviceRequest],
                    ~.Device]:
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
    ) -> Callable[[device_manager.GetDeviceRequest], resources.Device]:
        r"""Return a callable for the get device method over gRPC.

        Gets details about a device.

        Returns:
            Callable[[~.GetDeviceRequest],
                    ~.Device]:
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
    ) -> Callable[[device_manager.UpdateDeviceRequest], resources.Device]:
        r"""Return a callable for the update device method over gRPC.

        Updates a device.

        Returns:
            Callable[[~.UpdateDeviceRequest],
                    ~.Device]:
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
    ) -> Callable[[device_manager.DeleteDeviceRequest], empty.Empty]:
        r"""Return a callable for the delete device method over gRPC.

        Deletes a device.

        Returns:
            Callable[[~.DeleteDeviceRequest],
                    ~.Empty]:
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
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_device"]

    @property
    def list_devices(
        self,
    ) -> Callable[
        [device_manager.ListDevicesRequest], device_manager.ListDevicesResponse
    ]:
        r"""Return a callable for the list devices method over gRPC.

        List devices in a device registry.

        Returns:
            Callable[[~.ListDevicesRequest],
                    ~.ListDevicesResponse]:
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
        [device_manager.ModifyCloudToDeviceConfigRequest], resources.DeviceConfig
    ]:
        r"""Return a callable for the modify cloud to device config method over gRPC.

        Modifies the configuration for the device, which is
        eventually sent from the Cloud IoT Core servers. Returns
        the modified configuration version and its metadata.

        Returns:
            Callable[[~.ModifyCloudToDeviceConfigRequest],
                    ~.DeviceConfig]:
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
        device_manager.ListDeviceConfigVersionsResponse,
    ]:
        r"""Return a callable for the list device config versions method over gRPC.

        Lists the last few versions of the device
        configuration in descending order (i.e.: newest first).

        Returns:
            Callable[[~.ListDeviceConfigVersionsRequest],
                    ~.ListDeviceConfigVersionsResponse]:
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
        device_manager.ListDeviceStatesResponse,
    ]:
        r"""Return a callable for the list device states method over gRPC.

        Lists the last few versions of the device state in
        descending order (i.e.: newest first).

        Returns:
            Callable[[~.ListDeviceStatesRequest],
                    ~.ListDeviceStatesResponse]:
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
    ) -> Callable[[iam_policy.SetIamPolicyRequest], policy.Policy]:
        r"""Return a callable for the set iam policy method over gRPC.

        Sets the access control policy on the specified
        resource. Replaces any existing policy.

        Returns:
            Callable[[~.SetIamPolicyRequest],
                    ~.Policy]:
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
                request_serializer=iam_policy.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy.GetIamPolicyRequest], policy.Policy]:
        r"""Return a callable for the get iam policy method over gRPC.

        Gets the access control policy for a resource.
        Returns an empty policy if the resource exists and does
        not have a policy set.

        Returns:
            Callable[[~.GetIamPolicyRequest],
                    ~.Policy]:
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
                request_serializer=iam_policy.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy.TestIamPermissionsRequest], iam_policy.TestIamPermissionsResponse
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.

        Returns permissions that a caller has on the specified resource.
        If the resource does not exist, this will return an empty set of
        permissions, not a NOT_FOUND error.

        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    ~.TestIamPermissionsResponse]:
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
                request_serializer=iam_policy.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]

    @property
    def send_command_to_device(
        self,
    ) -> Callable[
        [device_manager.SendCommandToDeviceRequest],
        device_manager.SendCommandToDeviceResponse,
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
                    ~.SendCommandToDeviceResponse]:
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
        device_manager.BindDeviceToGatewayResponse,
    ]:
        r"""Return a callable for the bind device to gateway method over gRPC.

        Associates the device with the gateway.

        Returns:
            Callable[[~.BindDeviceToGatewayRequest],
                    ~.BindDeviceToGatewayResponse]:
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
        device_manager.UnbindDeviceFromGatewayResponse,
    ]:
        r"""Return a callable for the unbind device from gateway method over gRPC.

        Deletes the association between the device and the
        gateway.

        Returns:
            Callable[[~.UnbindDeviceFromGatewayRequest],
                    ~.UnbindDeviceFromGatewayResponse]:
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


__all__ = ("DeviceManagerGrpcTransport",)
