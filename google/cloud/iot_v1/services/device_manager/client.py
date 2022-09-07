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
from collections import OrderedDict
import os
import re
from typing import Dict, Mapping, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.cloud.iot_v1.services.device_manager import pagers
from google.cloud.iot_v1.types import device_manager
from google.cloud.iot_v1.types import resources
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from .transports.base import DeviceManagerTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import DeviceManagerGrpcTransport
from .transports.grpc_asyncio import DeviceManagerGrpcAsyncIOTransport


class DeviceManagerClientMeta(type):
    """Metaclass for the DeviceManager client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[DeviceManagerTransport]]
    _transport_registry["grpc"] = DeviceManagerGrpcTransport
    _transport_registry["grpc_asyncio"] = DeviceManagerGrpcAsyncIOTransport

    def get_transport_class(
        cls,
        label: str = None,
    ) -> Type[DeviceManagerTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class DeviceManagerClient(metaclass=DeviceManagerClientMeta):
    """Internet of Things (IoT) service. Securely connect and manage
    IoT devices.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "cloudiot.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DeviceManagerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DeviceManagerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DeviceManagerTransport:
        """Returns the transport used by the client instance.

        Returns:
            DeviceManagerTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def device_path(
        project: str,
        location: str,
        registry: str,
        device: str,
    ) -> str:
        """Returns a fully-qualified device string."""
        return "projects/{project}/locations/{location}/registries/{registry}/devices/{device}".format(
            project=project,
            location=location,
            registry=registry,
            device=device,
        )

    @staticmethod
    def parse_device_path(path: str) -> Dict[str, str]:
        """Parses a device path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/registries/(?P<registry>.+?)/devices/(?P<device>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def registry_path(
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

    @staticmethod
    def parse_registry_path(path: str) -> Dict[str, str]:
        """Parses a registry path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/registries/(?P<registry>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, DeviceManagerTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the device manager client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, DeviceManagerTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, DeviceManagerTransport):
            # transport is a DeviceManagerTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=client_options.api_audience,
            )

    def create_device_registry(
        self,
        request: Union[device_manager.CreateDeviceRegistryRequest, dict] = None,
        *,
        parent: str = None,
        device_registry: resources.DeviceRegistry = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DeviceRegistry:
        r"""Creates a device registry that contains devices.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_create_device_registry():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.CreateDeviceRegistryRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_device_registry(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.CreateDeviceRegistryRequest, dict]):
                The request object. Request for `CreateDeviceRegistry`.
            parent (str):
                Required. The project and cloud region where this device
                registry must be created. For example,
                ``projects/example-project/locations/us-central1``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            device_registry (google.cloud.iot_v1.types.DeviceRegistry):
                Required. The device registry. The field ``name`` must
                be empty. The server will generate that field from the
                device registry ``id`` provided and the ``parent``
                field.

                This corresponds to the ``device_registry`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.types.DeviceRegistry:
                A container for a group of devices.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, device_registry])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.CreateDeviceRegistryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.CreateDeviceRegistryRequest):
            request = device_manager.CreateDeviceRegistryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if device_registry is not None:
                request.device_registry = device_registry

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_device_registry]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_device_registry(
        self,
        request: Union[device_manager.GetDeviceRegistryRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DeviceRegistry:
        r"""Gets a device registry configuration.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_get_device_registry():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.GetDeviceRegistryRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_device_registry(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.GetDeviceRegistryRequest, dict]):
                The request object. Request for `GetDeviceRegistry`.
            name (str):
                Required. The name of the device registry. For example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.types.DeviceRegistry:
                A container for a group of devices.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.GetDeviceRegistryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.GetDeviceRegistryRequest):
            request = device_manager.GetDeviceRegistryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_device_registry]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_device_registry(
        self,
        request: Union[device_manager.UpdateDeviceRegistryRequest, dict] = None,
        *,
        device_registry: resources.DeviceRegistry = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DeviceRegistry:
        r"""Updates a device registry configuration.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_update_device_registry():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.UpdateDeviceRegistryRequest(
                )

                # Make the request
                response = client.update_device_registry(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.UpdateDeviceRegistryRequest, dict]):
                The request object. Request for `UpdateDeviceRegistry`.
            device_registry (google.cloud.iot_v1.types.DeviceRegistry):
                Required. The new values for the device registry. The
                ``id`` field must be empty, and the ``name`` field must
                indicate the path of the resource. For example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.

                This corresponds to the ``device_registry`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Only updates the ``device_registry`` fields
                indicated by this mask. The field mask must not be
                empty, and it must not contain fields that are immutable
                or only set by the server. Mutable top-level fields:
                ``event_notification_config``, ``http_config``,
                ``mqtt_config``, and ``state_notification_config``.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.types.DeviceRegistry:
                A container for a group of devices.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([device_registry, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.UpdateDeviceRegistryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.UpdateDeviceRegistryRequest):
            request = device_manager.UpdateDeviceRegistryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if device_registry is not None:
                request.device_registry = device_registry
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_device_registry]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("device_registry.name", request.device_registry.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_device_registry(
        self,
        request: Union[device_manager.DeleteDeviceRegistryRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a device registry configuration.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_delete_device_registry():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.DeleteDeviceRegistryRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_device_registry(request=request)

        Args:
            request (Union[google.cloud.iot_v1.types.DeleteDeviceRegistryRequest, dict]):
                The request object. Request for `DeleteDeviceRegistry`.
            name (str):
                Required. The name of the device registry. For example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.DeleteDeviceRegistryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.DeleteDeviceRegistryRequest):
            request = device_manager.DeleteDeviceRegistryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_device_registry]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def list_device_registries(
        self,
        request: Union[device_manager.ListDeviceRegistriesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDeviceRegistriesPager:
        r"""Lists device registries.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_list_device_registries():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.ListDeviceRegistriesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_device_registries(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.ListDeviceRegistriesRequest, dict]):
                The request object. Request for `ListDeviceRegistries`.
            parent (str):
                Required. The project and cloud region path. For
                example,
                ``projects/example-project/locations/us-central1``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.services.device_manager.pagers.ListDeviceRegistriesPager:
                Response for ListDeviceRegistries.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.ListDeviceRegistriesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.ListDeviceRegistriesRequest):
            request = device_manager.ListDeviceRegistriesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_device_registries]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDeviceRegistriesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_device(
        self,
        request: Union[device_manager.CreateDeviceRequest, dict] = None,
        *,
        parent: str = None,
        device: resources.Device = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Device:
        r"""Creates a device in a device registry.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_create_device():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.CreateDeviceRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_device(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.CreateDeviceRequest, dict]):
                The request object. Request for `CreateDevice`.
            parent (str):
                Required. The name of the device registry where this
                device should be created. For example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            device (google.cloud.iot_v1.types.Device):
                Required. The device registration details. The field
                ``name`` must be empty. The server generates ``name``
                from the device registry ``id`` and the ``parent``
                field.

                This corresponds to the ``device`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.types.Device:
                The device resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, device])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.CreateDeviceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.CreateDeviceRequest):
            request = device_manager.CreateDeviceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if device is not None:
                request.device = device

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_device]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_device(
        self,
        request: Union[device_manager.GetDeviceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Device:
        r"""Gets details about a device.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_get_device():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.GetDeviceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_device(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.GetDeviceRequest, dict]):
                The request object. Request for `GetDevice`.
            name (str):
                Required. The name of the device. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
                or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.types.Device:
                The device resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.GetDeviceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.GetDeviceRequest):
            request = device_manager.GetDeviceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_device]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_device(
        self,
        request: Union[device_manager.UpdateDeviceRequest, dict] = None,
        *,
        device: resources.Device = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Device:
        r"""Updates a device.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_update_device():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.UpdateDeviceRequest(
                )

                # Make the request
                response = client.update_device(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.UpdateDeviceRequest, dict]):
                The request object. Request for `UpdateDevice`.
            device (google.cloud.iot_v1.types.Device):
                Required. The new values for the device. The ``id`` and
                ``num_id`` fields must be empty, and the field ``name``
                must specify the name path. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``\ or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.

                This corresponds to the ``device`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Only updates the ``device`` fields indicated
                by this mask. The field mask must not be empty, and it
                must not contain fields that are immutable or only set
                by the server. Mutable top-level fields:
                ``credentials``, ``blocked``, and ``metadata``

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.types.Device:
                The device resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([device, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.UpdateDeviceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.UpdateDeviceRequest):
            request = device_manager.UpdateDeviceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if device is not None:
                request.device = device
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_device]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("device.name", request.device.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_device(
        self,
        request: Union[device_manager.DeleteDeviceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a device.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_delete_device():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.DeleteDeviceRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_device(request=request)

        Args:
            request (Union[google.cloud.iot_v1.types.DeleteDeviceRequest, dict]):
                The request object. Request for `DeleteDevice`.
            name (str):
                Required. The name of the device. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
                or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.DeleteDeviceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.DeleteDeviceRequest):
            request = device_manager.DeleteDeviceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_device]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def list_devices(
        self,
        request: Union[device_manager.ListDevicesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDevicesPager:
        r"""List devices in a device registry.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_list_devices():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.ListDevicesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_devices(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.ListDevicesRequest, dict]):
                The request object. Request for `ListDevices`.
            parent (str):
                Required. The device registry path. Required. For
                example,
                ``projects/my-project/locations/us-central1/registries/my-registry``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.services.device_manager.pagers.ListDevicesPager:
                Response for ListDevices.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.ListDevicesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.ListDevicesRequest):
            request = device_manager.ListDevicesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_devices]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDevicesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def modify_cloud_to_device_config(
        self,
        request: Union[device_manager.ModifyCloudToDeviceConfigRequest, dict] = None,
        *,
        name: str = None,
        binary_data: bytes = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DeviceConfig:
        r"""Modifies the configuration for the device, which is
        eventually sent from the Cloud IoT Core servers. Returns
        the modified configuration version and its metadata.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_modify_cloud_to_device_config():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.ModifyCloudToDeviceConfigRequest(
                    name="name_value",
                    binary_data=b'binary_data_blob',
                )

                # Make the request
                response = client.modify_cloud_to_device_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.ModifyCloudToDeviceConfigRequest, dict]):
                The request object. Request for
                `ModifyCloudToDeviceConfig`.
            name (str):
                Required. The name of the device. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
                or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            binary_data (bytes):
                Required. The configuration data for
                the device.

                This corresponds to the ``binary_data`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.types.DeviceConfig:
                The device configuration. Eventually
                delivered to devices.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, binary_data])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.ModifyCloudToDeviceConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.ModifyCloudToDeviceConfigRequest):
            request = device_manager.ModifyCloudToDeviceConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if binary_data is not None:
                request.binary_data = binary_data

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.modify_cloud_to_device_config
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_device_config_versions(
        self,
        request: Union[device_manager.ListDeviceConfigVersionsRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> device_manager.ListDeviceConfigVersionsResponse:
        r"""Lists the last few versions of the device
        configuration in descending order (i.e.: newest first).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_list_device_config_versions():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.ListDeviceConfigVersionsRequest(
                    name="name_value",
                )

                # Make the request
                response = client.list_device_config_versions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.ListDeviceConfigVersionsRequest, dict]):
                The request object. Request for
                `ListDeviceConfigVersions`.
            name (str):
                Required. The name of the device. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
                or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.types.ListDeviceConfigVersionsResponse:
                Response for ListDeviceConfigVersions.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.ListDeviceConfigVersionsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.ListDeviceConfigVersionsRequest):
            request = device_manager.ListDeviceConfigVersionsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_device_config_versions
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_device_states(
        self,
        request: Union[device_manager.ListDeviceStatesRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> device_manager.ListDeviceStatesResponse:
        r"""Lists the last few versions of the device state in
        descending order (i.e.: newest first).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_list_device_states():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.ListDeviceStatesRequest(
                    name="name_value",
                )

                # Make the request
                response = client.list_device_states(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.ListDeviceStatesRequest, dict]):
                The request object. Request for `ListDeviceStates`.
            name (str):
                Required. The name of the device. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
                or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.types.ListDeviceStatesResponse:
                Response for ListDeviceStates.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.ListDeviceStatesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.ListDeviceStatesRequest):
            request = device_manager.ListDeviceStatesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_device_states]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_iam_policy(
        self,
        request: Union[iam_policy_pb2.SetIamPolicyRequest, dict] = None,
        *,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the access control policy on the specified
        resource. Replaces any existing policy.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_set_iam_policy():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.SetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = client.set_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.SetIamPolicyRequest, dict]):
                The request object. Request message for `SetIamPolicy`
                method.
            resource (str):
                REQUIRED: The resource for which the
                policy is being specified. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": [ "user:eve@example.com" ],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ], "etag": "BwWWja0YfJA=", "version": 3

                      }

                   **YAML example:**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z') etag:
                      BwWWja0YfJA= version: 3

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.SetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_iam_policy(
        self,
        request: Union[iam_policy_pb2.GetIamPolicyRequest, dict] = None,
        *,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the access control policy for a resource.
        Returns an empty policy if the resource exists and does
        not have a policy set.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_get_iam_policy():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.GetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = client.get_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.GetIamPolicyRequest, dict]):
                The request object. Request message for `GetIamPolicy`
                method.
            resource (str):
                REQUIRED: The resource for which the
                policy is being requested. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": [ "user:eve@example.com" ],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ], "etag": "BwWWja0YfJA=", "version": 3

                      }

                   **YAML example:**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z') etag:
                      BwWWja0YfJA= version: 3

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.GetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def test_iam_permissions(
        self,
        request: Union[iam_policy_pb2.TestIamPermissionsRequest, dict] = None,
        *,
        resource: str = None,
        permissions: Sequence[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Returns permissions that a caller has on the specified resource.
        If the resource does not exist, this will return an empty set of
        permissions, not a NOT_FOUND error.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_test_iam_permissions():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.TestIamPermissionsRequest(
                    resource="resource_value",
                    permissions=['permissions_value1', 'permissions_value2'],
                )

                # Make the request
                response = client.test_iam_permissions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest, dict]):
                The request object. Request message for
                `TestIamPermissions` method.
            resource (str):
                REQUIRED: The resource for which the
                policy detail is being requested. See
                the operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            permissions (Sequence[str]):
                The set of permissions to check for the ``resource``.
                Permissions with wildcards (such as '*' or 'storage.*')
                are not allowed. For more information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.

                This corresponds to the ``permissions`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for TestIamPermissions method.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource, permissions])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.TestIamPermissionsRequest()
            if resource is not None:
                request.resource = resource
            if permissions:
                request.permissions.extend(permissions)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.test_iam_permissions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def send_command_to_device(
        self,
        request: Union[device_manager.SendCommandToDeviceRequest, dict] = None,
        *,
        name: str = None,
        binary_data: bytes = None,
        subfolder: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> device_manager.SendCommandToDeviceResponse:
        r"""Sends a command to the specified device. In order for a device
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

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_send_command_to_device():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.SendCommandToDeviceRequest(
                    name="name_value",
                    binary_data=b'binary_data_blob',
                )

                # Make the request
                response = client.send_command_to_device(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.SendCommandToDeviceRequest, dict]):
                The request object. Request for `SendCommandToDevice`.
            name (str):
                Required. The name of the device. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
                or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            binary_data (bytes):
                Required. The command data to send to
                the device.

                This corresponds to the ``binary_data`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            subfolder (str):
                Optional subfolder for the command.
                If empty, the command will be delivered
                to the /devices/{device-id}/commands
                topic, otherwise it will be delivered to
                the
                /devices/{device-id}/commands/{subfolder}
                topic. Multi-level subfolders are
                allowed. This field must not have more
                than 256 characters, and must not
                contain any MQTT wildcards ("+" or "#")
                or null characters.

                This corresponds to the ``subfolder`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.types.SendCommandToDeviceResponse:
                Response for SendCommandToDevice.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, binary_data, subfolder])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.SendCommandToDeviceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.SendCommandToDeviceRequest):
            request = device_manager.SendCommandToDeviceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if binary_data is not None:
                request.binary_data = binary_data
            if subfolder is not None:
                request.subfolder = subfolder

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.send_command_to_device]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def bind_device_to_gateway(
        self,
        request: Union[device_manager.BindDeviceToGatewayRequest, dict] = None,
        *,
        parent: str = None,
        gateway_id: str = None,
        device_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> device_manager.BindDeviceToGatewayResponse:
        r"""Associates the device with the gateway.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_bind_device_to_gateway():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.BindDeviceToGatewayRequest(
                    parent="parent_value",
                    gateway_id="gateway_id_value",
                    device_id="device_id_value",
                )

                # Make the request
                response = client.bind_device_to_gateway(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.BindDeviceToGatewayRequest, dict]):
                The request object. Request for `BindDeviceToGateway`.
            parent (str):
                Required. The name of the registry. For example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            gateway_id (str):
                Required. The value of ``gateway_id`` can be either the
                device numeric ID or the user-defined device identifier.

                This corresponds to the ``gateway_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            device_id (str):
                Required. The device to associate with the specified
                gateway. The value of ``device_id`` can be either the
                device numeric ID or the user-defined device identifier.

                This corresponds to the ``device_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.types.BindDeviceToGatewayResponse:
                Response for BindDeviceToGateway.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, gateway_id, device_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.BindDeviceToGatewayRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.BindDeviceToGatewayRequest):
            request = device_manager.BindDeviceToGatewayRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if gateway_id is not None:
                request.gateway_id = gateway_id
            if device_id is not None:
                request.device_id = device_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.bind_device_to_gateway]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def unbind_device_from_gateway(
        self,
        request: Union[device_manager.UnbindDeviceFromGatewayRequest, dict] = None,
        *,
        parent: str = None,
        gateway_id: str = None,
        device_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> device_manager.UnbindDeviceFromGatewayResponse:
        r"""Deletes the association between the device and the
        gateway.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import iot_v1

            def sample_unbind_device_from_gateway():
                # Create a client
                client = iot_v1.DeviceManagerClient()

                # Initialize request argument(s)
                request = iot_v1.UnbindDeviceFromGatewayRequest(
                    parent="parent_value",
                    gateway_id="gateway_id_value",
                    device_id="device_id_value",
                )

                # Make the request
                response = client.unbind_device_from_gateway(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.iot_v1.types.UnbindDeviceFromGatewayRequest, dict]):
                The request object. Request for
                `UnbindDeviceFromGateway`.
            parent (str):
                Required. The name of the registry. For example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            gateway_id (str):
                Required. The value of ``gateway_id`` can be either the
                device numeric ID or the user-defined device identifier.

                This corresponds to the ``gateway_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            device_id (str):
                Required. The device to disassociate from the specified
                gateway. The value of ``device_id`` can be either the
                device numeric ID or the user-defined device identifier.

                This corresponds to the ``device_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.iot_v1.types.UnbindDeviceFromGatewayResponse:
                Response for UnbindDeviceFromGateway.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, gateway_id, device_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a device_manager.UnbindDeviceFromGatewayRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, device_manager.UnbindDeviceFromGatewayRequest):
            request = device_manager.UnbindDeviceFromGatewayRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if gateway_id is not None:
                request.gateway_id = gateway_id
            if device_id is not None:
                request.device_id = device_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.unbind_device_from_gateway
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-iot",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DeviceManagerClient",)
