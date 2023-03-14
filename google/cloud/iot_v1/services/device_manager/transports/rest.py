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

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.iot_v1.types import device_manager, resources

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import DeviceManagerTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class DeviceManagerRestInterceptor:
    """Interceptor for DeviceManager.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DeviceManagerRestTransport.

    .. code-block:: python
        class MyCustomDeviceManagerInterceptor(DeviceManagerRestInterceptor):
            def pre_bind_device_to_gateway(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_bind_device_to_gateway(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_device(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_device(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_device_registry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_device_registry(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_device(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_device_registry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_device(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_device(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_device_registry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_device_registry(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_device_config_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_device_config_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_device_registries(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_device_registries(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_devices(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_devices(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_device_states(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_device_states(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_modify_cloud_to_device_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_modify_cloud_to_device_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_send_command_to_device(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_send_command_to_device(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_test_iam_permissions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_test_iam_permissions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_unbind_device_from_gateway(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_unbind_device_from_gateway(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_device(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_device(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_device_registry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_device_registry(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DeviceManagerRestTransport(interceptor=MyCustomDeviceManagerInterceptor())
        client = DeviceManagerClient(transport=transport)


    """

    def pre_bind_device_to_gateway(
        self,
        request: device_manager.BindDeviceToGatewayRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[device_manager.BindDeviceToGatewayRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for bind_device_to_gateway

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_bind_device_to_gateway(
        self, response: device_manager.BindDeviceToGatewayResponse
    ) -> device_manager.BindDeviceToGatewayResponse:
        """Post-rpc interceptor for bind_device_to_gateway

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_device(
        self,
        request: device_manager.CreateDeviceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[device_manager.CreateDeviceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_device

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_create_device(self, response: resources.Device) -> resources.Device:
        """Post-rpc interceptor for create_device

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_device_registry(
        self,
        request: device_manager.CreateDeviceRegistryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[device_manager.CreateDeviceRegistryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_device_registry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_create_device_registry(
        self, response: resources.DeviceRegistry
    ) -> resources.DeviceRegistry:
        """Post-rpc interceptor for create_device_registry

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_device(
        self,
        request: device_manager.DeleteDeviceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[device_manager.DeleteDeviceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_device

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def pre_delete_device_registry(
        self,
        request: device_manager.DeleteDeviceRegistryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[device_manager.DeleteDeviceRegistryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_device_registry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def pre_get_device(
        self,
        request: device_manager.GetDeviceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[device_manager.GetDeviceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_device

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_get_device(self, response: resources.Device) -> resources.Device:
        """Post-rpc interceptor for get_device

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_device_registry(
        self,
        request: device_manager.GetDeviceRegistryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[device_manager.GetDeviceRegistryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_device_registry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_get_device_registry(
        self, response: resources.DeviceRegistry
    ) -> resources.DeviceRegistry:
        """Post-rpc interceptor for get_device_registry

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_device_config_versions(
        self,
        request: device_manager.ListDeviceConfigVersionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        device_manager.ListDeviceConfigVersionsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_device_config_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_list_device_config_versions(
        self, response: device_manager.ListDeviceConfigVersionsResponse
    ) -> device_manager.ListDeviceConfigVersionsResponse:
        """Post-rpc interceptor for list_device_config_versions

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_device_registries(
        self,
        request: device_manager.ListDeviceRegistriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[device_manager.ListDeviceRegistriesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_device_registries

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_list_device_registries(
        self, response: device_manager.ListDeviceRegistriesResponse
    ) -> device_manager.ListDeviceRegistriesResponse:
        """Post-rpc interceptor for list_device_registries

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_devices(
        self,
        request: device_manager.ListDevicesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[device_manager.ListDevicesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_devices

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_list_devices(
        self, response: device_manager.ListDevicesResponse
    ) -> device_manager.ListDevicesResponse:
        """Post-rpc interceptor for list_devices

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_device_states(
        self,
        request: device_manager.ListDeviceStatesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[device_manager.ListDeviceStatesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_device_states

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_list_device_states(
        self, response: device_manager.ListDeviceStatesResponse
    ) -> device_manager.ListDeviceStatesResponse:
        """Post-rpc interceptor for list_device_states

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_modify_cloud_to_device_config(
        self,
        request: device_manager.ModifyCloudToDeviceConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        device_manager.ModifyCloudToDeviceConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for modify_cloud_to_device_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_modify_cloud_to_device_config(
        self, response: resources.DeviceConfig
    ) -> resources.DeviceConfig:
        """Post-rpc interceptor for modify_cloud_to_device_config

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_send_command_to_device(
        self,
        request: device_manager.SendCommandToDeviceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[device_manager.SendCommandToDeviceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for send_command_to_device

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_send_command_to_device(
        self, response: device_manager.SendCommandToDeviceResponse
    ) -> device_manager.SendCommandToDeviceResponse:
        """Post-rpc interceptor for send_command_to_device

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_unbind_device_from_gateway(
        self,
        request: device_manager.UnbindDeviceFromGatewayRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        device_manager.UnbindDeviceFromGatewayRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for unbind_device_from_gateway

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_unbind_device_from_gateway(
        self, response: device_manager.UnbindDeviceFromGatewayResponse
    ) -> device_manager.UnbindDeviceFromGatewayResponse:
        """Post-rpc interceptor for unbind_device_from_gateway

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_device(
        self,
        request: device_manager.UpdateDeviceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[device_manager.UpdateDeviceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_device

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_update_device(self, response: resources.Device) -> resources.Device:
        """Post-rpc interceptor for update_device

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_device_registry(
        self,
        request: device_manager.UpdateDeviceRegistryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[device_manager.UpdateDeviceRegistryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_device_registry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DeviceManager server.
        """
        return request, metadata

    def post_update_device_registry(
        self, response: resources.DeviceRegistry
    ) -> resources.DeviceRegistry:
        """Post-rpc interceptor for update_device_registry

        Override in a subclass to manipulate the response
        after it is returned by the DeviceManager server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DeviceManagerRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DeviceManagerRestInterceptor


class DeviceManagerRestTransport(DeviceManagerTransport):
    """REST backend transport for DeviceManager.

    Internet of Things (IoT) service. Securely connect and manage
    IoT devices.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "cloudiot.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DeviceManagerRestInterceptor] = None,
        api_audience: Optional[str] = None,
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

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or DeviceManagerRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _BindDeviceToGateway(DeviceManagerRestStub):
        def __hash__(self):
            return hash("BindDeviceToGateway")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.BindDeviceToGatewayRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> device_manager.BindDeviceToGatewayResponse:
            r"""Call the bind device to gateway method over HTTP.

            Args:
                request (~.device_manager.BindDeviceToGatewayRequest):
                    The request object. Request for ``BindDeviceToGateway``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.device_manager.BindDeviceToGatewayResponse:
                    Response for ``BindDeviceToGateway``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/registries/*}:bindDeviceToGateway",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/registries/*/groups/*}:bindDeviceToGateway",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_bind_device_to_gateway(
                request, metadata
            )
            pb_request = device_manager.BindDeviceToGatewayRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = device_manager.BindDeviceToGatewayResponse()
            pb_resp = device_manager.BindDeviceToGatewayResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_bind_device_to_gateway(resp)
            return resp

    class _CreateDevice(DeviceManagerRestStub):
        def __hash__(self):
            return hash("CreateDevice")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.CreateDeviceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Device:
            r"""Call the create device method over HTTP.

            Args:
                request (~.device_manager.CreateDeviceRequest):
                    The request object. Request for ``CreateDevice``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Device:
                    The device resource.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/registries/*}/devices",
                    "body": "device",
                },
            ]
            request, metadata = self._interceptor.pre_create_device(request, metadata)
            pb_request = device_manager.CreateDeviceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Device()
            pb_resp = resources.Device.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_device(resp)
            return resp

    class _CreateDeviceRegistry(DeviceManagerRestStub):
        def __hash__(self):
            return hash("CreateDeviceRegistry")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.CreateDeviceRegistryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DeviceRegistry:
            r"""Call the create device registry method over HTTP.

            Args:
                request (~.device_manager.CreateDeviceRegistryRequest):
                    The request object. Request for ``CreateDeviceRegistry``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.DeviceRegistry:
                    A container for a group of devices.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/registries",
                    "body": "device_registry",
                },
            ]
            request, metadata = self._interceptor.pre_create_device_registry(
                request, metadata
            )
            pb_request = device_manager.CreateDeviceRegistryRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.DeviceRegistry()
            pb_resp = resources.DeviceRegistry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_device_registry(resp)
            return resp

    class _DeleteDevice(DeviceManagerRestStub):
        def __hash__(self):
            return hash("DeleteDevice")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.DeleteDeviceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete device method over HTTP.

            Args:
                request (~.device_manager.DeleteDeviceRequest):
                    The request object. Request for ``DeleteDevice``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/registries/*/devices/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_device(request, metadata)
            pb_request = device_manager.DeleteDeviceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteDeviceRegistry(DeviceManagerRestStub):
        def __hash__(self):
            return hash("DeleteDeviceRegistry")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.DeleteDeviceRegistryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete device registry method over HTTP.

            Args:
                request (~.device_manager.DeleteDeviceRegistryRequest):
                    The request object. Request for ``DeleteDeviceRegistry``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/registries/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_device_registry(
                request, metadata
            )
            pb_request = device_manager.DeleteDeviceRegistryRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetDevice(DeviceManagerRestStub):
        def __hash__(self):
            return hash("GetDevice")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.GetDeviceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Device:
            r"""Call the get device method over HTTP.

            Args:
                request (~.device_manager.GetDeviceRequest):
                    The request object. Request for ``GetDevice``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Device:
                    The device resource.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/registries/*/devices/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/registries/*/groups/*/devices/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_device(request, metadata)
            pb_request = device_manager.GetDeviceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Device()
            pb_resp = resources.Device.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_device(resp)
            return resp

    class _GetDeviceRegistry(DeviceManagerRestStub):
        def __hash__(self):
            return hash("GetDeviceRegistry")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.GetDeviceRegistryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DeviceRegistry:
            r"""Call the get device registry method over HTTP.

            Args:
                request (~.device_manager.GetDeviceRegistryRequest):
                    The request object. Request for ``GetDeviceRegistry``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.DeviceRegistry:
                    A container for a group of devices.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/registries/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_device_registry(
                request, metadata
            )
            pb_request = device_manager.GetDeviceRegistryRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.DeviceRegistry()
            pb_resp = resources.DeviceRegistry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_device_registry(resp)
            return resp

    class _GetIamPolicy(DeviceManagerRestStub):
        def __hash__(self):
            return hash("GetIamPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.GetIamPolicyRequest):
                    The request object. Request message for ``GetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": [
                            "user:eve@example.com"
                          ],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ],
                      "etag": "BwWWja0YfJA=",
                      "version": 3
                    }

                **YAML example:**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                    etag: BwWWja0YfJA=
                    version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/registries/*}:getIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/registries/*/groups/*}:getIamPolicy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            pb_request = request
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    class _ListDeviceConfigVersions(DeviceManagerRestStub):
        def __hash__(self):
            return hash("ListDeviceConfigVersions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.ListDeviceConfigVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> device_manager.ListDeviceConfigVersionsResponse:
            r"""Call the list device config
            versions method over HTTP.

                Args:
                    request (~.device_manager.ListDeviceConfigVersionsRequest):
                        The request object. Request for ``ListDeviceConfigVersions``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.device_manager.ListDeviceConfigVersionsResponse:
                        Response for ``ListDeviceConfigVersions``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/registries/*/devices/*}/configVersions",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/registries/*/groups/*/devices/*}/configVersions",
                },
            ]
            request, metadata = self._interceptor.pre_list_device_config_versions(
                request, metadata
            )
            pb_request = device_manager.ListDeviceConfigVersionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = device_manager.ListDeviceConfigVersionsResponse()
            pb_resp = device_manager.ListDeviceConfigVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_device_config_versions(resp)
            return resp

    class _ListDeviceRegistries(DeviceManagerRestStub):
        def __hash__(self):
            return hash("ListDeviceRegistries")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.ListDeviceRegistriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> device_manager.ListDeviceRegistriesResponse:
            r"""Call the list device registries method over HTTP.

            Args:
                request (~.device_manager.ListDeviceRegistriesRequest):
                    The request object. Request for ``ListDeviceRegistries``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.device_manager.ListDeviceRegistriesResponse:
                    Response for ``ListDeviceRegistries``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/registries",
                },
            ]
            request, metadata = self._interceptor.pre_list_device_registries(
                request, metadata
            )
            pb_request = device_manager.ListDeviceRegistriesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = device_manager.ListDeviceRegistriesResponse()
            pb_resp = device_manager.ListDeviceRegistriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_device_registries(resp)
            return resp

    class _ListDevices(DeviceManagerRestStub):
        def __hash__(self):
            return hash("ListDevices")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.ListDevicesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> device_manager.ListDevicesResponse:
            r"""Call the list devices method over HTTP.

            Args:
                request (~.device_manager.ListDevicesRequest):
                    The request object. Request for ``ListDevices``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.device_manager.ListDevicesResponse:
                    Response for ``ListDevices``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/registries/*}/devices",
                },
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/registries/*/groups/*}/devices",
                },
            ]
            request, metadata = self._interceptor.pre_list_devices(request, metadata)
            pb_request = device_manager.ListDevicesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = device_manager.ListDevicesResponse()
            pb_resp = device_manager.ListDevicesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_devices(resp)
            return resp

    class _ListDeviceStates(DeviceManagerRestStub):
        def __hash__(self):
            return hash("ListDeviceStates")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.ListDeviceStatesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> device_manager.ListDeviceStatesResponse:
            r"""Call the list device states method over HTTP.

            Args:
                request (~.device_manager.ListDeviceStatesRequest):
                    The request object. Request for ``ListDeviceStates``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.device_manager.ListDeviceStatesResponse:
                    Response for ``ListDeviceStates``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/registries/*/devices/*}/states",
                },
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/registries/*/groups/*/devices/*}/states",
                },
            ]
            request, metadata = self._interceptor.pre_list_device_states(
                request, metadata
            )
            pb_request = device_manager.ListDeviceStatesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = device_manager.ListDeviceStatesResponse()
            pb_resp = device_manager.ListDeviceStatesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_device_states(resp)
            return resp

    class _ModifyCloudToDeviceConfig(DeviceManagerRestStub):
        def __hash__(self):
            return hash("ModifyCloudToDeviceConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.ModifyCloudToDeviceConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DeviceConfig:
            r"""Call the modify cloud to device
            config method over HTTP.

                Args:
                    request (~.device_manager.ModifyCloudToDeviceConfigRequest):
                        The request object. Request for ``ModifyCloudToDeviceConfig``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.DeviceConfig:
                        The device configuration. Eventually
                    delivered to devices.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/registries/*/devices/*}:modifyCloudToDeviceConfig",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/registries/*/groups/*/devices/*}:modifyCloudToDeviceConfig",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_modify_cloud_to_device_config(
                request, metadata
            )
            pb_request = device_manager.ModifyCloudToDeviceConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.DeviceConfig()
            pb_resp = resources.DeviceConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_modify_cloud_to_device_config(resp)
            return resp

    class _SendCommandToDevice(DeviceManagerRestStub):
        def __hash__(self):
            return hash("SendCommandToDevice")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.SendCommandToDeviceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> device_manager.SendCommandToDeviceResponse:
            r"""Call the send command to device method over HTTP.

            Args:
                request (~.device_manager.SendCommandToDeviceRequest):
                    The request object. Request for ``SendCommandToDevice``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.device_manager.SendCommandToDeviceResponse:
                    Response for ``SendCommandToDevice``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/registries/*/devices/*}:sendCommandToDevice",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/registries/*/groups/*/devices/*}:sendCommandToDevice",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_send_command_to_device(
                request, metadata
            )
            pb_request = device_manager.SendCommandToDeviceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = device_manager.SendCommandToDeviceResponse()
            pb_resp = device_manager.SendCommandToDeviceResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_send_command_to_device(resp)
            return resp

    class _SetIamPolicy(DeviceManagerRestStub):
        def __hash__(self):
            return hash("SetIamPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.SetIamPolicyRequest):
                    The request object. Request message for ``SetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": [
                            "user:eve@example.com"
                          ],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ],
                      "etag": "BwWWja0YfJA=",
                      "version": 3
                    }

                **YAML example:**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                    etag: BwWWja0YfJA=
                    version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/registries/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/registries/*/groups/*}:setIamPolicy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            pb_request = request
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    class _TestIamPermissions(DeviceManagerRestStub):
        def __hash__(self):
            return hash("TestIamPermissions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (~.iam_policy_pb2.TestIamPermissionsRequest):
                    The request object. Request message for ``TestIamPermissions`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.iam_policy_pb2.TestIamPermissionsResponse:
                    Response message for ``TestIamPermissions`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/registries/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/registries/*/groups/*}:testIamPermissions",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            pb_request = request
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    class _UnbindDeviceFromGateway(DeviceManagerRestStub):
        def __hash__(self):
            return hash("UnbindDeviceFromGateway")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.UnbindDeviceFromGatewayRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> device_manager.UnbindDeviceFromGatewayResponse:
            r"""Call the unbind device from
            gateway method over HTTP.

                Args:
                    request (~.device_manager.UnbindDeviceFromGatewayRequest):
                        The request object. Request for ``UnbindDeviceFromGateway``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.device_manager.UnbindDeviceFromGatewayResponse:
                        Response for ``UnbindDeviceFromGateway``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/registries/*}:unbindDeviceFromGateway",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/registries/*/groups/*}:unbindDeviceFromGateway",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_unbind_device_from_gateway(
                request, metadata
            )
            pb_request = device_manager.UnbindDeviceFromGatewayRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = device_manager.UnbindDeviceFromGatewayResponse()
            pb_resp = device_manager.UnbindDeviceFromGatewayResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_unbind_device_from_gateway(resp)
            return resp

    class _UpdateDevice(DeviceManagerRestStub):
        def __hash__(self):
            return hash("UpdateDevice")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.UpdateDeviceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Device:
            r"""Call the update device method over HTTP.

            Args:
                request (~.device_manager.UpdateDeviceRequest):
                    The request object. Request for ``UpdateDevice``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Device:
                    The device resource.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{device.name=projects/*/locations/*/registries/*/devices/*}",
                    "body": "device",
                },
                {
                    "method": "patch",
                    "uri": "/v1/{device.name=projects/*/locations/*/registries/*/groups/*/devices/*}",
                    "body": "device",
                },
            ]
            request, metadata = self._interceptor.pre_update_device(request, metadata)
            pb_request = device_manager.UpdateDeviceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Device()
            pb_resp = resources.Device.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_device(resp)
            return resp

    class _UpdateDeviceRegistry(DeviceManagerRestStub):
        def __hash__(self):
            return hash("UpdateDeviceRegistry")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: device_manager.UpdateDeviceRegistryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DeviceRegistry:
            r"""Call the update device registry method over HTTP.

            Args:
                request (~.device_manager.UpdateDeviceRegistryRequest):
                    The request object. Request for ``UpdateDeviceRegistry``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.DeviceRegistry:
                    A container for a group of devices.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{device_registry.name=projects/*/locations/*/registries/*}",
                    "body": "device_registry",
                },
            ]
            request, metadata = self._interceptor.pre_update_device_registry(
                request, metadata
            )
            pb_request = device_manager.UpdateDeviceRegistryRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.DeviceRegistry()
            pb_resp = resources.DeviceRegistry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_device_registry(resp)
            return resp

    @property
    def bind_device_to_gateway(
        self,
    ) -> Callable[
        [device_manager.BindDeviceToGatewayRequest],
        device_manager.BindDeviceToGatewayResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BindDeviceToGateway(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_device(
        self,
    ) -> Callable[[device_manager.CreateDeviceRequest], resources.Device]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDevice(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_device_registry(
        self,
    ) -> Callable[
        [device_manager.CreateDeviceRegistryRequest], resources.DeviceRegistry
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDeviceRegistry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_device(
        self,
    ) -> Callable[[device_manager.DeleteDeviceRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDevice(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_device_registry(
        self,
    ) -> Callable[[device_manager.DeleteDeviceRegistryRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDeviceRegistry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_device(
        self,
    ) -> Callable[[device_manager.GetDeviceRequest], resources.Device]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDevice(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_device_registry(
        self,
    ) -> Callable[[device_manager.GetDeviceRegistryRequest], resources.DeviceRegistry]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDeviceRegistry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_device_config_versions(
        self,
    ) -> Callable[
        [device_manager.ListDeviceConfigVersionsRequest],
        device_manager.ListDeviceConfigVersionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDeviceConfigVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_device_registries(
        self,
    ) -> Callable[
        [device_manager.ListDeviceRegistriesRequest],
        device_manager.ListDeviceRegistriesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDeviceRegistries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_devices(
        self,
    ) -> Callable[
        [device_manager.ListDevicesRequest], device_manager.ListDevicesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDevices(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_device_states(
        self,
    ) -> Callable[
        [device_manager.ListDeviceStatesRequest],
        device_manager.ListDeviceStatesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDeviceStates(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def modify_cloud_to_device_config(
        self,
    ) -> Callable[
        [device_manager.ModifyCloudToDeviceConfigRequest], resources.DeviceConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ModifyCloudToDeviceConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def send_command_to_device(
        self,
    ) -> Callable[
        [device_manager.SendCommandToDeviceRequest],
        device_manager.SendCommandToDeviceResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SendCommandToDevice(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        iam_policy_pb2.TestIamPermissionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def unbind_device_from_gateway(
        self,
    ) -> Callable[
        [device_manager.UnbindDeviceFromGatewayRequest],
        device_manager.UnbindDeviceFromGatewayResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UnbindDeviceFromGateway(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_device(
        self,
    ) -> Callable[[device_manager.UpdateDeviceRequest], resources.Device]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDevice(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_device_registry(
        self,
    ) -> Callable[
        [device_manager.UpdateDeviceRegistryRequest], resources.DeviceRegistry
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDeviceRegistry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("DeviceManagerRestTransport",)
