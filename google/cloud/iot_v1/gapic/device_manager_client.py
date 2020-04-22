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

"""Accesses the google.cloud.iot.v1 DeviceManager API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.iot_v1.gapic import device_manager_client_config
from google.cloud.iot_v1.gapic import enums
from google.cloud.iot_v1.gapic.transports import device_manager_grpc_transport
from google.cloud.iot_v1.proto import device_manager_pb2
from google.cloud.iot_v1.proto import device_manager_pb2_grpc
from google.cloud.iot_v1.proto import resources_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import options_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-iot").version


class DeviceManagerClient(object):
    """Internet of Things (IoT) service. Securely connect and manage IoT devices."""

    SERVICE_ADDRESS = "cloudiot.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.iot.v1.DeviceManager"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
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

    @classmethod
    def device_path(cls, project, location, registry, device):
        """Return a fully-qualified device string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/registries/{registry}/devices/{device}",
            project=project,
            location=location,
            registry=registry,
            device=device,
        )

    @classmethod
    def location_path(cls, project, location):
        """Return a fully-qualified location string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}",
            project=project,
            location=location,
        )

    @classmethod
    def registry_path(cls, project, location, registry):
        """Return a fully-qualified registry string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/registries/{registry}",
            project=project,
            location=location,
            registry=registry,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.DeviceManagerGrpcTransport,
                    Callable[[~.Credentials, type], ~.DeviceManagerGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = device_manager_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=device_manager_grpc_transport.DeviceManagerGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = device_manager_grpc_transport.DeviceManagerGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def create_device_registry(
        self,
        parent,
        device_registry,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a device registry that contains devices.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `device_registry`:
            >>> device_registry = {}
            >>>
            >>> response = client.create_device_registry(parent, device_registry)

        Args:
            parent (str): [Output only] The last time a telemetry event was received.
                Timestamps are periodically collected and written to storage; they may
                be stale by a few minutes.
            device_registry (Union[dict, ~google.cloud.iot_v1.types.DeviceRegistry]): If not empty, indicates that there may be more registries that match
                the request; this value should be passed in a new
                ``ListDeviceRegistriesRequest``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.DeviceRegistry`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.DeviceRegistry` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_device_registry" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_device_registry"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_device_registry,
                default_retry=self._method_configs["CreateDeviceRegistry"].retry,
                default_timeout=self._method_configs["CreateDeviceRegistry"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.CreateDeviceRegistryRequest(
            parent=parent, device_registry=device_registry
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_device_registry"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_device_registry(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a device registry configuration.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> response = client.get_device_registry(name)

        Args:
            name (str): Request for ``CreateDevice``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.DeviceRegistry` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_device_registry" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_device_registry"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_device_registry,
                default_retry=self._method_configs["GetDeviceRegistry"].retry,
                default_timeout=self._method_configs["GetDeviceRegistry"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.GetDeviceRegistryRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_device_registry"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_device_registry(
        self,
        device_registry,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a device registry configuration.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> # TODO: Initialize `device_registry`:
            >>> device_registry = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_device_registry(device_registry, update_mask)

        Args:
            device_registry (Union[dict, ~google.cloud.iot_v1.types.DeviceRegistry]): Protocol Buffers - Google's data interchange format Copyright 2008
                Google Inc. All rights reserved.
                https://developers.google.com/protocol-buffers/

                Redistribution and use in source and binary forms, with or without
                modification, are permitted provided that the following conditions are
                met:

                ::

                    * Redistributions of source code must retain the above copyright

                notice, this list of conditions and the following disclaimer. \*
                Redistributions in binary form must reproduce the above copyright
                notice, this list of conditions and the following disclaimer in the
                documentation and/or other materials provided with the distribution. \*
                Neither the name of Google Inc. nor the names of its contributors may be
                used to endorse or promote products derived from this software without
                specific prior written permission.

                THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
                IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
                TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
                PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
                OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
                EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
                PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
                PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
                LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
                NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
                SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.DeviceRegistry`
            update_mask (Union[dict, ~google.cloud.iot_v1.types.FieldMask]): Whether the message is an automatically generated map entry type for
                the maps field.

                For maps fields: map<KeyType, ValueType> map_field = 1; The parsed
                descriptor looks like: message MapFieldEntry { option map_entry = true;
                optional KeyType key = 1; optional ValueType value = 2; } repeated
                MapFieldEntry map_field = 1;

                Implementations may choose not to generate the map_entry=true message,
                but use a native map in the target language to hold the keys and values.
                The reflection APIs in such implementations still need to work as if the
                field is a repeated message field.

                NOTE: Do not set the option in .proto files. Always use the maps syntax
                instead. The option should only be implicitly set by the proto compiler
                parser.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.DeviceRegistry` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_device_registry" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_device_registry"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_device_registry,
                default_retry=self._method_configs["UpdateDeviceRegistry"].retry,
                default_timeout=self._method_configs["UpdateDeviceRegistry"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.UpdateDeviceRegistryRequest(
            device_registry=device_registry, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("device_registry.name", device_registry.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_device_registry"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_device_registry(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a device registry configuration.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> client.delete_device_registry(name)

        Args:
            name (str): Required. The name of the device registry where this device should
                be created. For example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_device_registry" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_device_registry"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_device_registry,
                default_retry=self._method_configs["DeleteDeviceRegistry"].retry,
                default_timeout=self._method_configs["DeleteDeviceRegistry"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.DeleteDeviceRegistryRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_device_registry"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_device_registries(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists device registries.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_device_registries(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_device_registries(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Defines an Identity and Access Management (IAM) policy. It is used
                to specify access control policies for Cloud Platform resources.

                A ``Policy`` is a collection of ``bindings``. A ``binding`` binds one or
                more ``members`` to a single ``role``. Members can be user accounts,
                service accounts, Google groups, and domains (such as G Suite). A
                ``role`` is a named list of permissions (defined by IAM or configured by
                users). A ``binding`` can optionally specify a ``condition``, which is a
                logic expression that further constrains the role binding based on
                attributes about the request and/or target resource.

                **JSON Example**

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
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }

                **YAML Example**

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

                For a description of IAM and its features, see the `IAM developer's
                guide <https://cloud.google.com/iam/docs>`__.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.iot_v1.types.DeviceRegistry` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_device_registries" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_device_registries"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_device_registries,
                default_retry=self._method_configs["ListDeviceRegistries"].retry,
                default_timeout=self._method_configs["ListDeviceRegistries"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.ListDeviceRegistriesRequest(
            parent=parent, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_device_registries"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="device_registries",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_device(
        self,
        parent,
        device,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a device in a device registry.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> parent = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> # TODO: Initialize `device`:
            >>> device = {}
            >>>
            >>> response = client.create_device(parent, device)

        Args:
            parent (str): The resource path name. For example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.
            device (Union[dict, ~google.cloud.iot_v1.types.Device]): Identifies which part of the FileDescriptorProto was defined at this
                location.

                Each element is a field number or an index. They form a path from the
                root FileDescriptorProto to the place where the definition. For example,
                this path: [ 4, 3, 2, 7, 1 ] refers to: file.message_type(3) // 4, 3
                .field(7) // 2, 7 .name() // 1 This is because
                FileDescriptorProto.message_type has field number 4: repeated
                DescriptorProto message_type = 4; and DescriptorProto.field has field
                number 2: repeated FieldDescriptorProto field = 2; and
                FieldDescriptorProto.name has field number 1: optional string name = 1;

                Thus, the above path gives the location of a field name. If we removed
                the last element: [ 4, 3, 2, 7 ] this path refers to the whole field
                declaration (from the beginning of the label to the terminating
                semicolon).

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.Device`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.Device` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_device" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_device"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_device,
                default_retry=self._method_configs["CreateDevice"].retry,
                default_timeout=self._method_configs["CreateDevice"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.CreateDeviceRequest(parent=parent, device=device)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_device"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_device(
        self,
        name,
        field_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets details about a device.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.device_path('[PROJECT]', '[LOCATION]', '[REGISTRY]', '[DEVICE]')
            >>>
            >>> response = client.get_device(name)

        Args:
            name (str): The fields of the ``Device`` resource to be returned in the
                response. If the field mask is unset or empty, all fields are returned.
            field_mask (Union[dict, ~google.cloud.iot_v1.types.FieldMask]): Request for ``UpdateDevice``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.Device` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_device" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_device"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_device,
                default_retry=self._method_configs["GetDevice"].retry,
                default_timeout=self._method_configs["GetDevice"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.GetDeviceRequest(name=name, field_mask=field_mask)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_device"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_device(
        self,
        device,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a device.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> # TODO: Initialize `device`:
            >>> device = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_device(device, update_mask)

        Args:
            device (Union[dict, ~google.cloud.iot_v1.types.Device]): Protocol Buffers - Google's data interchange format Copyright 2008
                Google Inc. All rights reserved.
                https://developers.google.com/protocol-buffers/

                Redistribution and use in source and binary forms, with or without
                modification, are permitted provided that the following conditions are
                met:

                ::

                    * Redistributions of source code must retain the above copyright

                notice, this list of conditions and the following disclaimer. \*
                Redistributions in binary form must reproduce the above copyright
                notice, this list of conditions and the following disclaimer in the
                documentation and/or other materials provided with the distribution. \*
                Neither the name of Google Inc. nor the names of its contributors may be
                used to endorse or promote products derived from this software without
                specific prior written permission.

                THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
                IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
                TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
                PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
                OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
                EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
                PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
                PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
                LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
                NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
                SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.Device`
            update_mask (Union[dict, ~google.cloud.iot_v1.types.FieldMask]): If this SourceCodeInfo represents a complete declaration, these are
                any comments appearing before and after the declaration which appear to
                be attached to the declaration.

                A series of line comments appearing on consecutive lines, with no other
                tokens appearing on those lines, will be treated as a single comment.

                leading_detached_comments will keep paragraphs of comments that appear
                before (but not connected to) the current element. Each paragraph,
                separated by empty lines, will be one comment element in the repeated
                field.

                Only the comment content is provided; comment markers (e.g. //) are
                stripped out. For block comments, leading whitespace and an asterisk
                will be stripped from the beginning of each line other than the first.
                Newlines are included in the output.

                Examples:

                optional int32 foo = 1; // Comment attached to foo. // Comment attached
                to bar. optional int32 bar = 2;

                optional string baz = 3; // Comment attached to baz. // Another line
                attached to baz.

                // Comment attached to qux. // // Another line attached to qux. optional
                double qux = 4;

                // Detached comment for corge. This is not leading or trailing comments
                // to qux or corge because there are blank lines separating it from //
                both.

                // Detached comment for corge paragraph 2.

                optional string corge = 5; /\* Block comment attached \* to corge.
                Leading asterisks \* will be removed. */ /* Block comment attached to \*
                grault. \*/ optional int32 grault = 6;

                // ignored detached comments.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.Device` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_device" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_device"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_device,
                default_retry=self._method_configs["UpdateDevice"].retry,
                default_timeout=self._method_configs["UpdateDevice"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.UpdateDeviceRequest(
            device=device, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("device.name", device.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_device"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_device(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a device.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.device_path('[PROJECT]', '[LOCATION]', '[REGISTRY]', '[DEVICE]')
            >>>
            >>> client.delete_device(name)

        Args:
            name (str): Request for ``DeleteDevice``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_device" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_device"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_device,
                default_retry=self._method_configs["DeleteDevice"].retry,
                default_timeout=self._method_configs["DeleteDevice"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.DeleteDeviceRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_device"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_devices(
        self,
        parent,
        device_num_ids=None,
        device_ids=None,
        field_mask=None,
        gateway_list_options=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        List devices in a device registry.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> parent = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_devices(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_devices(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): ``Any`` contains an arbitrary serialized protocol buffer message
                along with a URL that describes the type of the serialized message.

                Protobuf library provides support to pack/unpack Any values in the form
                of utility functions or additional generated methods of the Any type.

                Example 1: Pack and unpack a message in C++.

                ::

                    Foo foo = ...;
                    Any any;
                    any.PackFrom(foo);
                    ...
                    if (any.UnpackTo(&foo)) {
                      ...
                    }

                Example 2: Pack and unpack a message in Java.

                ::

                    Foo foo = ...;
                    Any any = Any.pack(foo);
                    ...
                    if (any.is(Foo.class)) {
                      foo = any.unpack(Foo.class);
                    }

                Example 3: Pack and unpack a message in Python.

                ::

                    foo = Foo(...)
                    any = Any()
                    any.Pack(foo)
                    ...
                    if any.Is(Foo.DESCRIPTOR):
                      any.Unpack(foo)
                      ...

                Example 4: Pack and unpack a message in Go

                ::

                     foo := &pb.Foo{...}
                     any, err := ptypes.MarshalAny(foo)
                     ...
                     foo := &pb.Foo{}
                     if err := ptypes.UnmarshalAny(any, foo); err != nil {
                       ...
                     }

                The pack methods provided by protobuf library will by default use
                'type.googleapis.com/full.type.name' as the type URL and the unpack
                methods only use the fully qualified type name after the last '/' in the
                type URL, for example "foo.bar.com/x/y.z" will yield type name "y.z".

                # JSON

                The JSON representation of an ``Any`` value uses the regular
                representation of the deserialized, embedded message, with an additional
                field ``@type`` which contains the type URL. Example:

                ::

                    package google.profile;
                    message Person {
                      string first_name = 1;
                      string last_name = 2;
                    }

                    {
                      "@type": "type.googleapis.com/google.profile.Person",
                      "firstName": <string>,
                      "lastName": <string>
                    }

                If the embedded message type is well-known and has a custom JSON
                representation, that representation will be embedded adding a field
                ``value`` which holds the custom JSON in addition to the ``@type``
                field. Example (for message ``google.protobuf.Duration``):

                ::

                    {
                      "@type": "type.googleapis.com/google.protobuf.Duration",
                      "value": "1.212s"
                    }
            device_num_ids (list[long]): A list of device numeric IDs. If empty, this field is ignored. Maximum
                IDs: 10,000.
            device_ids (list[str]): A URL/resource name that uniquely identifies the type of the
                serialized protocol buffer message. This string must contain at least
                one "/" character. The last segment of the URL's path must represent the
                fully qualified name of the type (as in
                ``path/google.protobuf.Duration``). The name should be in a canonical
                form (e.g., leading "." is not accepted).

                In practice, teams usually precompile into the binary all types that
                they expect it to use in the context of Any. However, for URLs which use
                the scheme ``http``, ``https``, or no scheme, one can optionally set up
                a type server that maps type URLs to message definitions as follows:

                -  If no scheme is provided, ``https`` is assumed.
                -  An HTTP GET on the URL must yield a ``google.protobuf.Type`` value in
                   binary format, or produce an error.
                -  Applications are allowed to cache lookup results based on the URL, or
                   have them precompiled into a binary to avoid any lookup. Therefore,
                   binary compatibility needs to be preserved on changes to types. (Use
                   versioned type names to manage breaking changes.)

                Note: this functionality is not currently available in the official
                protobuf release, and it is not used for type URLs beginning with
                type.googleapis.com.

                Schemes other than ``http``, ``https`` (or the empty scheme) might be
                used with implementation specific semantics.
            field_mask (Union[dict, ~google.cloud.iot_v1.types.FieldMask]): Request for ``ListDevices``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.FieldMask`
            gateway_list_options (Union[dict, ~google.cloud.iot_v1.types.GatewayListOptions]): Options related to gateways.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.GatewayListOptions`
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.iot_v1.types.Device` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_devices" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_devices"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_devices,
                default_retry=self._method_configs["ListDevices"].retry,
                default_timeout=self._method_configs["ListDevices"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.ListDevicesRequest(
            parent=parent,
            device_num_ids=device_num_ids,
            device_ids=device_ids,
            field_mask=field_mask,
            gateway_list_options=gateway_list_options,
            page_size=page_size,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_devices"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="devices",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def modify_cloud_to_device_config(
        self,
        name,
        binary_data,
        version_to_update=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Modifies the configuration for the device, which is eventually sent from
        the Cloud IoT Core servers. Returns the modified configuration version and
        its metadata.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.device_path('[PROJECT]', '[LOCATION]', '[REGISTRY]', '[DEVICE]')
            >>>
            >>> # TODO: Initialize `binary_data`:
            >>> binary_data = b''
            >>>
            >>> response = client.modify_cloud_to_device_config(name, binary_data)

        Args:
            name (str): The fields of the ``Device`` resource to be returned in the
                response. The fields ``id`` and ``num_id`` are always returned, along
                with any other fields specified.
            binary_data (bytes): Required. The configuration data for the device.
            version_to_update (long): The version number to update. If this value is zero, it will not check the
                version number of the server and will always update the current version;
                otherwise, this update will fail if the version number found on the server
                does not match this version number. This is used to support multiple
                simultaneous updates without losing data.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.DeviceConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "modify_cloud_to_device_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "modify_cloud_to_device_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.modify_cloud_to_device_config,
                default_retry=self._method_configs["ModifyCloudToDeviceConfig"].retry,
                default_timeout=self._method_configs[
                    "ModifyCloudToDeviceConfig"
                ].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.ModifyCloudToDeviceConfigRequest(
            name=name, binary_data=binary_data, version_to_update=version_to_update
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["modify_cloud_to_device_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_device_config_versions(
        self,
        name,
        num_versions=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the last few versions of the device configuration in descending
        order (i.e.: newest first).

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.device_path('[PROJECT]', '[LOCATION]', '[REGISTRY]', '[DEVICE]')
            >>>
            >>> response = client.list_device_config_versions(name)

        Args:
            name (str): Should this field be parsed lazily? Lazy applies only to
                message-type fields. It means that when the outer message is initially
                parsed, the inner message's contents will not be parsed but instead
                stored in encoded form. The inner message will actually be parsed when
                it is first accessed.

                This is only a hint. Implementations are free to choose whether to use
                eager or lazy parsing regardless of the value of this option. However,
                setting this option true suggests that the protocol author believes that
                using lazy parsing on this field is worth the additional bookkeeping
                overhead typically needed to implement it.

                This option does not affect the public interface of any generated code;
                all method signatures remain the same. Furthermore, thread-safety of the
                interface is not affected by this option; const methods remain safe to
                call from multiple threads concurrently, while non-const methods
                continue to require exclusive access.

                Note that implementations may choose not to check required fields within
                a lazy sub-message. That is, calling IsInitialized() on the outer
                message may return true even if the inner message has missing required
                fields. This is necessary because otherwise the inner message would have
                to be parsed in order to perform the check, defeating the purpose of
                lazy parsing. An implementation which chooses not to check required
                fields must be consistent about it. That is, for any particular
                sub-message, the implementation must either *always* check its required
                fields, or *never* check its required fields, regardless of whether or
                not the message has been parsed.
            num_versions (int): The number of versions to list. Versions are listed in decreasing order of
                the version number. The maximum number of versions retained is 10. If this
                value is zero, it will return all the versions available.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.ListDeviceConfigVersionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_device_config_versions" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_device_config_versions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_device_config_versions,
                default_retry=self._method_configs["ListDeviceConfigVersions"].retry,
                default_timeout=self._method_configs[
                    "ListDeviceConfigVersions"
                ].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.ListDeviceConfigVersionsRequest(
            name=name, num_versions=num_versions
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["list_device_config_versions"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_device_states(
        self,
        name,
        num_states=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the last few versions of the device state in descending order (i.e.:
        newest first).

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.device_path('[PROJECT]', '[LOCATION]', '[REGISTRY]', '[DEVICE]')
            >>>
            >>> response = client.list_device_states(name)

        Args:
            name (str): A developer-facing error message, which should be in English. Any
                user-facing error message should be localized and sent in the
                ``google.rpc.Status.details`` field, or localized by the client.
            num_states (int): The number of states to list. States are listed in descending order of
                update time. The maximum number of states retained is 10. If this
                value is zero, it will return all the states available.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.ListDeviceStatesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_device_states" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_device_states"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_device_states,
                default_retry=self._method_configs["ListDeviceStates"].retry,
                default_timeout=self._method_configs["ListDeviceStates"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.ListDeviceStatesRequest(
            name=name, num_states=num_states
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["list_device_states"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_iam_policy(
        self,
        resource,
        policy,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the access control policy on the specified resource. Replaces any
        existing policy.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                See the operation documentation for the appropriate value for this field.
            policy (Union[dict, ~google.cloud.iot_v1.types.Policy]): Optional. The relative resource name pattern associated with this
                resource type. The DNS prefix of the full resource name shouldn't be
                specified here.

                The path pattern must follow the syntax, which aligns with HTTP binding
                syntax:

                ::

                    Template = Segment { "/" Segment } ;
                    Segment = LITERAL | Variable ;
                    Variable = "{" LITERAL "}" ;

                Examples:

                ::

                    - "projects/{project}/topics/{topic}"
                    - "projects/{project}/knowledgeBases/{knowledge_base}"

                The components in braces correspond to the IDs for each resource in the
                hierarchy. It is expected that, if multiple patterns are provided, the
                same component name (e.g. "project") refers to IDs of the same type of
                resource.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_iam_policy,
                default_retry=self._method_configs["SetIamPolicy"].retry,
                default_timeout=self._method_configs["SetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.SetIamPolicyRequest(resource=resource, policy=policy)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_iam_policy(
        self,
        resource,
        options_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the access control policy for a resource.
        Returns an empty policy if the resource exists and does not have a policy
        set.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                See the operation documentation for the appropriate value for this field.
            options_ (Union[dict, ~google.cloud.iot_v1.types.GetPolicyOptions]): Protocol Buffers - Google's data interchange format Copyright 2008
                Google Inc. All rights reserved.
                https://developers.google.com/protocol-buffers/

                Redistribution and use in source and binary forms, with or without
                modification, are permitted provided that the following conditions are
                met:

                ::

                    * Redistributions of source code must retain the above copyright

                notice, this list of conditions and the following disclaimer. \*
                Redistributions in binary form must reproduce the above copyright
                notice, this list of conditions and the following disclaimer in the
                documentation and/or other materials provided with the distribution. \*
                Neither the name of Google Inc. nor the names of its contributors may be
                used to endorse or promote products derived from this software without
                specific prior written permission.

                THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
                IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
                TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
                PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
                OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
                EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
                PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
                PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
                LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
                NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
                SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.GetPolicyOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_iam_policy,
                default_retry=self._method_configs["GetIamPolicy"].retry,
                default_timeout=self._method_configs["GetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.GetIamPolicyRequest(
            resource=resource, options=options_
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def test_iam_permissions(
        self,
        resource,
        permissions,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        ``etag`` is used for optimistic concurrency control as a way to help
        prevent simultaneous updates of a policy from overwriting each other. It
        is strongly suggested that systems make use of the ``etag`` in the
        read-modify-write cycle to perform policy updates in order to avoid race
        conditions: An ``etag`` is returned in the response to ``getIamPolicy``,
        and systems are expected to put that etag in the request to
        ``setIamPolicy`` to ensure that their change will be applied to the same
        version of the policy.

        If no ``etag`` is provided in the call to ``setIamPolicy``, then the
        existing policy is overwritten. Due to blind-set semantics of an
        etag-less policy, 'setIamPolicy' will not fail even if the incoming
        policy version does not meet the requirements for modifying the stored
        policy.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> # TODO: Initialize `permissions`:
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                See the operation documentation for the appropriate value for this field.
            permissions (list[str]): Optional. The historical or future-looking state of the resource
                pattern.

                Example:

                ::

                    // The InspectTemplate message originally only supported resource
                    // names with organization, and project was added later.
                    message InspectTemplate {
                      option (google.api.resource) = {
                        type: "dlp.googleapis.com/InspectTemplate"
                        pattern:
                        "organizations/{organization}/inspectTemplates/{inspect_template}"
                        pattern: "projects/{project}/inspectTemplates/{inspect_template}"
                        history: ORIGINALLY_SINGLE_PATTERN
                      };
                    }
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.TestIamPermissionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "test_iam_permissions" not in self._inner_api_calls:
            self._inner_api_calls[
                "test_iam_permissions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.test_iam_permissions,
                default_retry=self._method_configs["TestIamPermissions"].retry,
                default_timeout=self._method_configs["TestIamPermissions"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["test_iam_permissions"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def send_command_to_device(
        self,
        name,
        binary_data,
        subfolder=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        [Output only] The last time a state event was received. Timestamps
        are periodically collected and written to storage; they may be stale by
        a few minutes.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.device_path('[PROJECT]', '[LOCATION]', '[REGISTRY]', '[DEVICE]')
            >>>
            >>> # TODO: Initialize `binary_data`:
            >>> binary_data = b''
            >>>
            >>> response = client.send_command_to_device(name, binary_data)

        Args:
            name (str): Required. The device to disassociate from the specified gateway. The
                value of ``device_id`` can be either the device numeric ID or the
                user-defined device identifier.
            binary_data (bytes): Required. The command data to send to the device.
            subfolder (str): Optional subfolder for the command. If empty, the command will be delivered
                to the /devices/{device-id}/commands topic, otherwise it will be delivered
                to the /devices/{device-id}/commands/{subfolder} topic. Multi-level
                subfolders are allowed. This field must not have more than 256 characters,
                and must not contain any MQTT wildcards ("+" or "#") or null characters.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.SendCommandToDeviceResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "send_command_to_device" not in self._inner_api_calls:
            self._inner_api_calls[
                "send_command_to_device"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.send_command_to_device,
                default_retry=self._method_configs["SendCommandToDevice"].retry,
                default_timeout=self._method_configs["SendCommandToDevice"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.SendCommandToDeviceRequest(
            name=name, binary_data=binary_data, subfolder=subfolder
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["send_command_to_device"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def bind_device_to_gateway(
        self,
        parent,
        gateway_id,
        device_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Associates the device with the gateway.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> parent = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> # TODO: Initialize `gateway_id`:
            >>> gateway_id = ''
            >>>
            >>> # TODO: Initialize `device_id`:
            >>> device_id = ''
            >>>
            >>> response = client.bind_device_to_gateway(parent, gateway_id, device_id)

        Args:
            parent (str): If set, only devices associated with the specified gateway are
                returned. The gateway ID can be numeric (``num_id``) or the user-defined
                string (``id``). For example, if ``123`` is specified, only devices
                bound to the gateway with ``num_id`` 123 are returned.
            gateway_id (str): Required. The device registry. The field ``name`` must be empty. The
                server will generate that field from the device registry ``id`` provided
                and the ``parent`` field.
            device_id (str): Each of the definitions above may have "options" attached. These are
                just annotations which may cause code to be generated slightly
                differently or may contain hints for code that manipulates protocol
                messages.

                Clients may define custom options as extensions of the \*Options
                messages. These extensions may not yet be known at parsing time, so the
                parser cannot store the values in them. Instead it stores them in a
                field in the \*Options message called uninterpreted_option. This field
                must have the same name across all \*Options messages. We then use this
                field to populate the extensions when we build a descriptor, at which
                point all protos have been parsed and so all extensions are known.

                Extension numbers for custom options may be chosen as follows:

                -  For options which will only be used within a single application or
                   organization, or for experimental options, use field numbers 50000
                   through 99999. It is up to you to ensure that you do not use the same
                   number for multiple options.
                -  For options which will be published and used publicly by multiple
                   independent entities, e-mail
                   protobuf-global-extension-registry@google.com to reserve extension
                   numbers. Simply provide your project name (e.g. Objective-C plugin)
                   and your project website (if available) -- there's no need to explain
                   how you intend to use them. Usually you only need one extension
                   number. You can declare multiple options with only one extension
                   number by putting them in a sub-message. See the Custom Options
                   section of the docs for examples:
                   https://developers.google.com/protocol-buffers/docs/proto#options If
                   this turns out to be popular, a web service will be set up to
                   automatically assign option numbers.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.BindDeviceToGatewayResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "bind_device_to_gateway" not in self._inner_api_calls:
            self._inner_api_calls[
                "bind_device_to_gateway"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.bind_device_to_gateway,
                default_retry=self._method_configs["BindDeviceToGateway"].retry,
                default_timeout=self._method_configs["BindDeviceToGateway"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.BindDeviceToGatewayRequest(
            parent=parent, gateway_id=gateway_id, device_id=device_id
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["bind_device_to_gateway"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def unbind_device_from_gateway(
        self,
        parent,
        gateway_id,
        device_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes the association between the device and the gateway.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> parent = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> # TODO: Initialize `gateway_id`:
            >>> gateway_id = ''
            >>>
            >>> # TODO: Initialize `device_id`:
            >>> device_id = ''
            >>>
            >>> response = client.unbind_device_from_gateway(parent, gateway_id, device_id)

        Args:
            parent (str): Response for ``ListDevices``.
            gateway_id (str): If set, all the classes from the .proto file are wrapped in a single
                outer class with the given name. This applies to both Proto1 (equivalent
                to the old "--one_java_file" option) and Proto2 (where a .proto always
                translates to a single class, but you may want to explicitly choose the
                class name).
            device_id (str): A single identity that is exempted from "data access" audit logging
                for the ``service`` specified above. Follows the same format of
                Binding.members.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.UnbindDeviceFromGatewayResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "unbind_device_from_gateway" not in self._inner_api_calls:
            self._inner_api_calls[
                "unbind_device_from_gateway"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.unbind_device_from_gateway,
                default_retry=self._method_configs["UnbindDeviceFromGateway"].retry,
                default_timeout=self._method_configs["UnbindDeviceFromGateway"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.UnbindDeviceFromGatewayRequest(
            parent=parent, gateway_id=gateway_id, device_id=device_id
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["unbind_device_from_gateway"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
