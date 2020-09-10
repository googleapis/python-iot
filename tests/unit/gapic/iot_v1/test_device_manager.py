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

import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.iot_v1.services.device_manager import DeviceManagerAsyncClient
from google.cloud.iot_v1.services.device_manager import DeviceManagerClient
from google.cloud.iot_v1.services.device_manager import pagers
from google.cloud.iot_v1.services.device_manager import transports
from google.cloud.iot_v1.types import device_manager
from google.cloud.iot_v1.types import resources
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import options_pb2 as options  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.oauth2 import service_account
from google.protobuf import any_pb2 as any  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore
from google.type import expr_pb2 as expr  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert DeviceManagerClient._get_default_mtls_endpoint(None) is None
    assert (
        DeviceManagerClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DeviceManagerClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DeviceManagerClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DeviceManagerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DeviceManagerClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [DeviceManagerClient, DeviceManagerAsyncClient]
)
def test_device_manager_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "cloudiot.googleapis.com:443"


def test_device_manager_client_get_transport_class():
    transport = DeviceManagerClient.get_transport_class()
    assert transport == transports.DeviceManagerGrpcTransport

    transport = DeviceManagerClient.get_transport_class("grpc")
    assert transport == transports.DeviceManagerGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DeviceManagerClient, transports.DeviceManagerGrpcTransport, "grpc"),
        (
            DeviceManagerAsyncClient,
            transports.DeviceManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    DeviceManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DeviceManagerClient),
)
@mock.patch.object(
    DeviceManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DeviceManagerAsyncClient),
)
def test_device_manager_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DeviceManagerClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DeviceManagerClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=client_cert_source_callback,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and default_client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_MTLS_ENDPOINT,
                    scopes=None,
                    api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", but client_cert_source and default_client_cert_source are None.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DeviceManagerClient, transports.DeviceManagerGrpcTransport, "grpc"),
        (
            DeviceManagerAsyncClient,
            transports.DeviceManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_device_manager_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DeviceManagerClient, transports.DeviceManagerGrpcTransport, "grpc"),
        (
            DeviceManagerAsyncClient,
            transports.DeviceManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_device_manager_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_device_manager_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.iot_v1.services.device_manager.transports.DeviceManagerGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DeviceManagerClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_create_device_registry(
    transport: str = "grpc", request_type=device_manager.CreateDeviceRegistryRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry(
            id="id_value", name="name_value", log_level=resources.LogLevel.NONE,
        )

        response = client.create_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.CreateDeviceRegistryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceRegistry)

    assert response.id == "id_value"

    assert response.name == "name_value"

    assert response.log_level == resources.LogLevel.NONE


def test_create_device_registry_from_dict():
    test_create_device_registry(request_type=dict)


@pytest.mark.asyncio
async def test_create_device_registry_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.CreateDeviceRegistryRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceRegistry(
                id="id_value", name="name_value", log_level=resources.LogLevel.NONE,
            )
        )

        response = await client.create_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceRegistry)

    assert response.id == "id_value"

    assert response.name == "name_value"

    assert response.log_level == resources.LogLevel.NONE


def test_create_device_registry_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.CreateDeviceRegistryRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_device_registry), "__call__"
    ) as call:
        call.return_value = resources.DeviceRegistry()

        client.create_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_device_registry_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.CreateDeviceRegistryRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_device_registry), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceRegistry()
        )

        await client.create_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_device_registry_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_device_registry(
            parent="parent_value",
            device_registry=resources.DeviceRegistry(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].device_registry == resources.DeviceRegistry(id="id_value")


def test_create_device_registry_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_device_registry(
            device_manager.CreateDeviceRegistryRequest(),
            parent="parent_value",
            device_registry=resources.DeviceRegistry(id="id_value"),
        )


@pytest.mark.asyncio
async def test_create_device_registry_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceRegistry()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_device_registry(
            parent="parent_value",
            device_registry=resources.DeviceRegistry(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].device_registry == resources.DeviceRegistry(id="id_value")


@pytest.mark.asyncio
async def test_create_device_registry_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_device_registry(
            device_manager.CreateDeviceRegistryRequest(),
            parent="parent_value",
            device_registry=resources.DeviceRegistry(id="id_value"),
        )


def test_get_device_registry(
    transport: str = "grpc", request_type=device_manager.GetDeviceRegistryRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry(
            id="id_value", name="name_value", log_level=resources.LogLevel.NONE,
        )

        response = client.get_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.GetDeviceRegistryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceRegistry)

    assert response.id == "id_value"

    assert response.name == "name_value"

    assert response.log_level == resources.LogLevel.NONE


def test_get_device_registry_from_dict():
    test_get_device_registry(request_type=dict)


@pytest.mark.asyncio
async def test_get_device_registry_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.GetDeviceRegistryRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceRegistry(
                id="id_value", name="name_value", log_level=resources.LogLevel.NONE,
            )
        )

        response = await client.get_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceRegistry)

    assert response.id == "id_value"

    assert response.name == "name_value"

    assert response.log_level == resources.LogLevel.NONE


def test_get_device_registry_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.GetDeviceRegistryRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_device_registry), "__call__"
    ) as call:
        call.return_value = resources.DeviceRegistry()

        client.get_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_device_registry_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.GetDeviceRegistryRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_device_registry), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceRegistry()
        )

        await client.get_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_device_registry_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_device_registry(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_device_registry_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_device_registry(
            device_manager.GetDeviceRegistryRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_device_registry_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceRegistry()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_device_registry(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_device_registry_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_device_registry(
            device_manager.GetDeviceRegistryRequest(), name="name_value",
        )


def test_update_device_registry(
    transport: str = "grpc", request_type=device_manager.UpdateDeviceRegistryRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry(
            id="id_value", name="name_value", log_level=resources.LogLevel.NONE,
        )

        response = client.update_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.UpdateDeviceRegistryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceRegistry)

    assert response.id == "id_value"

    assert response.name == "name_value"

    assert response.log_level == resources.LogLevel.NONE


def test_update_device_registry_from_dict():
    test_update_device_registry(request_type=dict)


@pytest.mark.asyncio
async def test_update_device_registry_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.UpdateDeviceRegistryRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceRegistry(
                id="id_value", name="name_value", log_level=resources.LogLevel.NONE,
            )
        )

        response = await client.update_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceRegistry)

    assert response.id == "id_value"

    assert response.name == "name_value"

    assert response.log_level == resources.LogLevel.NONE


def test_update_device_registry_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.UpdateDeviceRegistryRequest()
    request.device_registry.name = "device_registry.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_device_registry), "__call__"
    ) as call:
        call.return_value = resources.DeviceRegistry()

        client.update_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "device_registry.name=device_registry.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_device_registry_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.UpdateDeviceRegistryRequest()
    request.device_registry.name = "device_registry.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_device_registry), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceRegistry()
        )

        await client.update_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "device_registry.name=device_registry.name/value",
    ) in kw["metadata"]


def test_update_device_registry_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_device_registry(
            device_registry=resources.DeviceRegistry(id="id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].device_registry == resources.DeviceRegistry(id="id_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_device_registry_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_device_registry(
            device_manager.UpdateDeviceRegistryRequest(),
            device_registry=resources.DeviceRegistry(id="id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_device_registry_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceRegistry()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_device_registry(
            device_registry=resources.DeviceRegistry(id="id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].device_registry == resources.DeviceRegistry(id="id_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_device_registry_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_device_registry(
            device_manager.UpdateDeviceRegistryRequest(),
            device_registry=resources.DeviceRegistry(id="id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_device_registry(
    transport: str = "grpc", request_type=device_manager.DeleteDeviceRegistryRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.DeleteDeviceRegistryRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_device_registry_from_dict():
    test_delete_device_registry(request_type=dict)


@pytest.mark.asyncio
async def test_delete_device_registry_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.DeleteDeviceRegistryRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_device_registry_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.DeleteDeviceRegistryRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_device_registry), "__call__"
    ) as call:
        call.return_value = None

        client.delete_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_device_registry_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.DeleteDeviceRegistryRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_device_registry), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_device_registry_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_device_registry(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_device_registry_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_device_registry(
            device_manager.DeleteDeviceRegistryRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_device_registry_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_device_registry(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_device_registry_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_device_registry(
            device_manager.DeleteDeviceRegistryRequest(), name="name_value",
        )


def test_list_device_registries(
    transport: str = "grpc", request_type=device_manager.ListDeviceRegistriesRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_device_registries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceRegistriesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_device_registries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.ListDeviceRegistriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeviceRegistriesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_device_registries_from_dict():
    test_list_device_registries(request_type=dict)


@pytest.mark.asyncio
async def test_list_device_registries_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.ListDeviceRegistriesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_device_registries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceRegistriesResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_device_registries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeviceRegistriesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_device_registries_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDeviceRegistriesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_device_registries), "__call__"
    ) as call:
        call.return_value = device_manager.ListDeviceRegistriesResponse()

        client.list_device_registries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_device_registries_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDeviceRegistriesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_device_registries), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceRegistriesResponse()
        )

        await client.list_device_registries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_device_registries_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_device_registries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceRegistriesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_device_registries(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_device_registries_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_device_registries(
            device_manager.ListDeviceRegistriesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_device_registries_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_device_registries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceRegistriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceRegistriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_device_registries(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_device_registries_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_device_registries(
            device_manager.ListDeviceRegistriesRequest(), parent="parent_value",
        )


def test_list_device_registries_pager():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_device_registries), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                ],
                next_page_token="abc",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[], next_page_token="def",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[resources.DeviceRegistry(),], next_page_token="ghi",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_device_registries(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.DeviceRegistry) for i in results)


def test_list_device_registries_pages():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_device_registries), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                ],
                next_page_token="abc",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[], next_page_token="def",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[resources.DeviceRegistry(),], next_page_token="ghi",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_device_registries(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_device_registries_async_pager():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_device_registries),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                ],
                next_page_token="abc",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[], next_page_token="def",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[resources.DeviceRegistry(),], next_page_token="ghi",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_device_registries(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.DeviceRegistry) for i in responses)


@pytest.mark.asyncio
async def test_list_device_registries_async_pages():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_device_registries),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                ],
                next_page_token="abc",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[], next_page_token="def",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[resources.DeviceRegistry(),], next_page_token="ghi",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_device_registries(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_device(
    transport: str = "grpc", request_type=device_manager.CreateDeviceRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device(
            id="id_value",
            name="name_value",
            num_id=636,
            blocked=True,
            log_level=resources.LogLevel.NONE,
        )

        response = client.create_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.CreateDeviceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Device)

    assert response.id == "id_value"

    assert response.name == "name_value"

    assert response.num_id == 636

    assert response.blocked is True

    assert response.log_level == resources.LogLevel.NONE


def test_create_device_from_dict():
    test_create_device(request_type=dict)


@pytest.mark.asyncio
async def test_create_device_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.CreateDeviceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_device), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Device(
                id="id_value",
                name="name_value",
                num_id=636,
                blocked=True,
                log_level=resources.LogLevel.NONE,
            )
        )

        response = await client.create_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Device)

    assert response.id == "id_value"

    assert response.name == "name_value"

    assert response.num_id == 636

    assert response.blocked is True

    assert response.log_level == resources.LogLevel.NONE


def test_create_device_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.CreateDeviceRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_device), "__call__") as call:
        call.return_value = resources.Device()

        client.create_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_device_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.CreateDeviceRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_device), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Device())

        await client.create_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_device_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_device(
            parent="parent_value", device=resources.Device(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].device == resources.Device(id="id_value")


def test_create_device_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_device(
            device_manager.CreateDeviceRequest(),
            parent="parent_value",
            device=resources.Device(id="id_value"),
        )


@pytest.mark.asyncio
async def test_create_device_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_device), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Device())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_device(
            parent="parent_value", device=resources.Device(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].device == resources.Device(id="id_value")


@pytest.mark.asyncio
async def test_create_device_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_device(
            device_manager.CreateDeviceRequest(),
            parent="parent_value",
            device=resources.Device(id="id_value"),
        )


def test_get_device(
    transport: str = "grpc", request_type=device_manager.GetDeviceRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device(
            id="id_value",
            name="name_value",
            num_id=636,
            blocked=True,
            log_level=resources.LogLevel.NONE,
        )

        response = client.get_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.GetDeviceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Device)

    assert response.id == "id_value"

    assert response.name == "name_value"

    assert response.num_id == 636

    assert response.blocked is True

    assert response.log_level == resources.LogLevel.NONE


def test_get_device_from_dict():
    test_get_device(request_type=dict)


@pytest.mark.asyncio
async def test_get_device_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.GetDeviceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_device), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Device(
                id="id_value",
                name="name_value",
                num_id=636,
                blocked=True,
                log_level=resources.LogLevel.NONE,
            )
        )

        response = await client.get_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Device)

    assert response.id == "id_value"

    assert response.name == "name_value"

    assert response.num_id == 636

    assert response.blocked is True

    assert response.log_level == resources.LogLevel.NONE


def test_get_device_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.GetDeviceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_device), "__call__") as call:
        call.return_value = resources.Device()

        client.get_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_device_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.GetDeviceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_device), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Device())

        await client.get_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_device_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_device(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_device_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_device(
            device_manager.GetDeviceRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_device_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_device), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Device())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_device(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_device_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_device(
            device_manager.GetDeviceRequest(), name="name_value",
        )


def test_update_device(
    transport: str = "grpc", request_type=device_manager.UpdateDeviceRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device(
            id="id_value",
            name="name_value",
            num_id=636,
            blocked=True,
            log_level=resources.LogLevel.NONE,
        )

        response = client.update_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.UpdateDeviceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Device)

    assert response.id == "id_value"

    assert response.name == "name_value"

    assert response.num_id == 636

    assert response.blocked is True

    assert response.log_level == resources.LogLevel.NONE


def test_update_device_from_dict():
    test_update_device(request_type=dict)


@pytest.mark.asyncio
async def test_update_device_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.UpdateDeviceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_device), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Device(
                id="id_value",
                name="name_value",
                num_id=636,
                blocked=True,
                log_level=resources.LogLevel.NONE,
            )
        )

        response = await client.update_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Device)

    assert response.id == "id_value"

    assert response.name == "name_value"

    assert response.num_id == 636

    assert response.blocked is True

    assert response.log_level == resources.LogLevel.NONE


def test_update_device_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.UpdateDeviceRequest()
    request.device.name = "device.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_device), "__call__") as call:
        call.return_value = resources.Device()

        client.update_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "device.name=device.name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_device_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.UpdateDeviceRequest()
    request.device.name = "device.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_device), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Device())

        await client.update_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "device.name=device.name/value",) in kw["metadata"]


def test_update_device_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_device(
            device=resources.Device(id="id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].device == resources.Device(id="id_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_device_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_device(
            device_manager.UpdateDeviceRequest(),
            device=resources.Device(id="id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_device_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_device), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Device())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_device(
            device=resources.Device(id="id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].device == resources.Device(id="id_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_device_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_device(
            device_manager.UpdateDeviceRequest(),
            device=resources.Device(id="id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_device(
    transport: str = "grpc", request_type=device_manager.DeleteDeviceRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.DeleteDeviceRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_device_from_dict():
    test_delete_device(request_type=dict)


@pytest.mark.asyncio
async def test_delete_device_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.DeleteDeviceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_device), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_device_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.DeleteDeviceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_device), "__call__") as call:
        call.return_value = None

        client.delete_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_device_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.DeleteDeviceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_device), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_device_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_device(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_device_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_device(
            device_manager.DeleteDeviceRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_device_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_device), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_device(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_device_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_device(
            device_manager.DeleteDeviceRequest(), name="name_value",
        )


def test_list_devices(
    transport: str = "grpc", request_type=device_manager.ListDevicesRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_devices), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDevicesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_devices(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.ListDevicesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDevicesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_devices_from_dict():
    test_list_devices(request_type=dict)


@pytest.mark.asyncio
async def test_list_devices_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.ListDevicesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_devices), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDevicesResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_devices(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDevicesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_devices_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDevicesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_devices), "__call__") as call:
        call.return_value = device_manager.ListDevicesResponse()

        client.list_devices(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_devices_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDevicesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_devices), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDevicesResponse()
        )

        await client.list_devices(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_devices_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_devices), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDevicesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_devices(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_devices_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_devices(
            device_manager.ListDevicesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_devices_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_devices), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDevicesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDevicesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_devices(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_devices_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_devices(
            device_manager.ListDevicesRequest(), parent="parent_value",
        )


def test_list_devices_pager():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_devices), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            device_manager.ListDevicesResponse(
                devices=[resources.Device(), resources.Device(), resources.Device(),],
                next_page_token="abc",
            ),
            device_manager.ListDevicesResponse(devices=[], next_page_token="def",),
            device_manager.ListDevicesResponse(
                devices=[resources.Device(),], next_page_token="ghi",
            ),
            device_manager.ListDevicesResponse(
                devices=[resources.Device(), resources.Device(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_devices(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.Device) for i in results)


def test_list_devices_pages():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_devices), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            device_manager.ListDevicesResponse(
                devices=[resources.Device(), resources.Device(), resources.Device(),],
                next_page_token="abc",
            ),
            device_manager.ListDevicesResponse(devices=[], next_page_token="def",),
            device_manager.ListDevicesResponse(
                devices=[resources.Device(),], next_page_token="ghi",
            ),
            device_manager.ListDevicesResponse(
                devices=[resources.Device(), resources.Device(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_devices(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_devices_async_pager():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_devices),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            device_manager.ListDevicesResponse(
                devices=[resources.Device(), resources.Device(), resources.Device(),],
                next_page_token="abc",
            ),
            device_manager.ListDevicesResponse(devices=[], next_page_token="def",),
            device_manager.ListDevicesResponse(
                devices=[resources.Device(),], next_page_token="ghi",
            ),
            device_manager.ListDevicesResponse(
                devices=[resources.Device(), resources.Device(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_devices(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Device) for i in responses)


@pytest.mark.asyncio
async def test_list_devices_async_pages():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_devices),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            device_manager.ListDevicesResponse(
                devices=[resources.Device(), resources.Device(), resources.Device(),],
                next_page_token="abc",
            ),
            device_manager.ListDevicesResponse(devices=[], next_page_token="def",),
            device_manager.ListDevicesResponse(
                devices=[resources.Device(),], next_page_token="ghi",
            ),
            device_manager.ListDevicesResponse(
                devices=[resources.Device(), resources.Device(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_devices(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_modify_cloud_to_device_config(
    transport: str = "grpc",
    request_type=device_manager.ModifyCloudToDeviceConfigRequest,
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.modify_cloud_to_device_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceConfig(
            version=774, binary_data=b"binary_data_blob",
        )

        response = client.modify_cloud_to_device_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.ModifyCloudToDeviceConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceConfig)

    assert response.version == 774

    assert response.binary_data == b"binary_data_blob"


def test_modify_cloud_to_device_config_from_dict():
    test_modify_cloud_to_device_config(request_type=dict)


@pytest.mark.asyncio
async def test_modify_cloud_to_device_config_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.ModifyCloudToDeviceConfigRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.modify_cloud_to_device_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceConfig(version=774, binary_data=b"binary_data_blob",)
        )

        response = await client.modify_cloud_to_device_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceConfig)

    assert response.version == 774

    assert response.binary_data == b"binary_data_blob"


def test_modify_cloud_to_device_config_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ModifyCloudToDeviceConfigRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.modify_cloud_to_device_config), "__call__"
    ) as call:
        call.return_value = resources.DeviceConfig()

        client.modify_cloud_to_device_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_modify_cloud_to_device_config_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ModifyCloudToDeviceConfigRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.modify_cloud_to_device_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceConfig()
        )

        await client.modify_cloud_to_device_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_modify_cloud_to_device_config_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.modify_cloud_to_device_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceConfig()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.modify_cloud_to_device_config(
            name="name_value", binary_data=b"binary_data_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].binary_data == b"binary_data_blob"


def test_modify_cloud_to_device_config_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.modify_cloud_to_device_config(
            device_manager.ModifyCloudToDeviceConfigRequest(),
            name="name_value",
            binary_data=b"binary_data_blob",
        )


@pytest.mark.asyncio
async def test_modify_cloud_to_device_config_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.modify_cloud_to_device_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.modify_cloud_to_device_config(
            name="name_value", binary_data=b"binary_data_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].binary_data == b"binary_data_blob"


@pytest.mark.asyncio
async def test_modify_cloud_to_device_config_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.modify_cloud_to_device_config(
            device_manager.ModifyCloudToDeviceConfigRequest(),
            name="name_value",
            binary_data=b"binary_data_blob",
        )


def test_list_device_config_versions(
    transport: str = "grpc", request_type=device_manager.ListDeviceConfigVersionsRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_device_config_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceConfigVersionsResponse()

        response = client.list_device_config_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.ListDeviceConfigVersionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.ListDeviceConfigVersionsResponse)


def test_list_device_config_versions_from_dict():
    test_list_device_config_versions(request_type=dict)


@pytest.mark.asyncio
async def test_list_device_config_versions_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.ListDeviceConfigVersionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_device_config_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceConfigVersionsResponse()
        )

        response = await client.list_device_config_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.ListDeviceConfigVersionsResponse)


def test_list_device_config_versions_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDeviceConfigVersionsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_device_config_versions), "__call__"
    ) as call:
        call.return_value = device_manager.ListDeviceConfigVersionsResponse()

        client.list_device_config_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_device_config_versions_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDeviceConfigVersionsRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_device_config_versions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceConfigVersionsResponse()
        )

        await client.list_device_config_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_list_device_config_versions_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_device_config_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceConfigVersionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_device_config_versions(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_list_device_config_versions_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_device_config_versions(
            device_manager.ListDeviceConfigVersionsRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_list_device_config_versions_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_device_config_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceConfigVersionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceConfigVersionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_device_config_versions(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_list_device_config_versions_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_device_config_versions(
            device_manager.ListDeviceConfigVersionsRequest(), name="name_value",
        )


def test_list_device_states(
    transport: str = "grpc", request_type=device_manager.ListDeviceStatesRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_device_states), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceStatesResponse()

        response = client.list_device_states(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.ListDeviceStatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.ListDeviceStatesResponse)


def test_list_device_states_from_dict():
    test_list_device_states(request_type=dict)


@pytest.mark.asyncio
async def test_list_device_states_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.ListDeviceStatesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_device_states), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceStatesResponse()
        )

        response = await client.list_device_states(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.ListDeviceStatesResponse)


def test_list_device_states_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDeviceStatesRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_device_states), "__call__"
    ) as call:
        call.return_value = device_manager.ListDeviceStatesResponse()

        client.list_device_states(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_device_states_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDeviceStatesRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_device_states), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceStatesResponse()
        )

        await client.list_device_states(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_list_device_states_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_device_states), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceStatesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_device_states(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_list_device_states_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_device_states(
            device_manager.ListDeviceStatesRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_list_device_states_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_device_states), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceStatesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceStatesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_device_states(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_list_device_states_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_device_states(
            device_manager.ListDeviceStatesRequest(), name="name_value",
        )


def test_set_iam_policy(
    transport: str = "grpc", request_type=iam_policy.SetIamPolicyRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob",)

        response = client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == iam_policy.SetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_set_iam_policy_from_dict():
    test_set_iam_policy(request_type=dict)


@pytest.mark.asyncio
async def test_set_iam_policy_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.set_iam_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy.Policy(version=774, etag=b"etag_blob",)
        )

        response = await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_set_iam_policy_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        call.return_value = policy.Policy()

        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.set_iam_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())

        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_set_iam_policy_from_dict():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy.Policy(version=774),
            }
        )
        call.assert_called()


def test_set_iam_policy_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_iam_policy(resource="resource_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].resource == "resource_value"


def test_set_iam_policy_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_iam_policy(
            iam_policy.SetIamPolicyRequest(), resource="resource_value",
        )


@pytest.mark.asyncio
async def test_set_iam_policy_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.set_iam_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_iam_policy(resource="resource_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].resource == "resource_value"


@pytest.mark.asyncio
async def test_set_iam_policy_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_iam_policy(
            iam_policy.SetIamPolicyRequest(), resource="resource_value",
        )


def test_get_iam_policy(
    transport: str = "grpc", request_type=iam_policy.GetIamPolicyRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob",)

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == iam_policy.GetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_get_iam_policy_from_dict():
    test_get_iam_policy(request_type=dict)


@pytest.mark.asyncio
async def test_get_iam_policy_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_iam_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy.Policy(version=774, etag=b"etag_blob",)
        )

        response = await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_get_iam_policy_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        call.return_value = policy.Policy()

        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_iam_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())

        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_get_iam_policy_from_dict():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_get_iam_policy_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_iam_policy(resource="resource_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].resource == "resource_value"


def test_get_iam_policy_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_iam_policy(
            iam_policy.GetIamPolicyRequest(), resource="resource_value",
        )


@pytest.mark.asyncio
async def test_get_iam_policy_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_iam_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy.Policy())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_iam_policy(resource="resource_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].resource == "resource_value"


@pytest.mark.asyncio
async def test_get_iam_policy_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_iam_policy(
            iam_policy.GetIamPolicyRequest(), resource="resource_value",
        )


def test_test_iam_permissions(
    transport: str = "grpc", request_type=iam_policy.TestIamPermissionsRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == iam_policy.TestIamPermissionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_from_dict():
    test_test_iam_permissions(request_type=dict)


@pytest.mark.asyncio
async def test_test_iam_permissions_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy.TestIamPermissionsResponse(permissions=["permissions_value"],)
        )

        response = await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy.TestIamPermissionsResponse()

        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy.TestIamPermissionsResponse()
        )

        await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_test_iam_permissions_from_dict():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse()

        response = client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


def test_test_iam_permissions_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.test_iam_permissions(
            resource="resource_value", permissions=["permissions_value"],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].resource == "resource_value"

        assert args[0].permissions == ["permissions_value"]


def test_test_iam_permissions_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.test_iam_permissions(
            iam_policy.TestIamPermissionsRequest(),
            resource="resource_value",
            permissions=["permissions_value"],
        )


@pytest.mark.asyncio
async def test_test_iam_permissions_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy.TestIamPermissionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.test_iam_permissions(
            resource="resource_value", permissions=["permissions_value"],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].resource == "resource_value"

        assert args[0].permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.test_iam_permissions(
            iam_policy.TestIamPermissionsRequest(),
            resource="resource_value",
            permissions=["permissions_value"],
        )


def test_send_command_to_device(
    transport: str = "grpc", request_type=device_manager.SendCommandToDeviceRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.send_command_to_device), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.SendCommandToDeviceResponse()

        response = client.send_command_to_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.SendCommandToDeviceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.SendCommandToDeviceResponse)


def test_send_command_to_device_from_dict():
    test_send_command_to_device(request_type=dict)


@pytest.mark.asyncio
async def test_send_command_to_device_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.SendCommandToDeviceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.send_command_to_device), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.SendCommandToDeviceResponse()
        )

        response = await client.send_command_to_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.SendCommandToDeviceResponse)


def test_send_command_to_device_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.SendCommandToDeviceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.send_command_to_device), "__call__"
    ) as call:
        call.return_value = device_manager.SendCommandToDeviceResponse()

        client.send_command_to_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_send_command_to_device_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.SendCommandToDeviceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.send_command_to_device), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.SendCommandToDeviceResponse()
        )

        await client.send_command_to_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_send_command_to_device_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.send_command_to_device), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.SendCommandToDeviceResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.send_command_to_device(
            name="name_value",
            binary_data=b"binary_data_blob",
            subfolder="subfolder_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].binary_data == b"binary_data_blob"

        assert args[0].subfolder == "subfolder_value"


def test_send_command_to_device_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.send_command_to_device(
            device_manager.SendCommandToDeviceRequest(),
            name="name_value",
            binary_data=b"binary_data_blob",
            subfolder="subfolder_value",
        )


@pytest.mark.asyncio
async def test_send_command_to_device_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.send_command_to_device), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.SendCommandToDeviceResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.SendCommandToDeviceResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.send_command_to_device(
            name="name_value",
            binary_data=b"binary_data_blob",
            subfolder="subfolder_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].binary_data == b"binary_data_blob"

        assert args[0].subfolder == "subfolder_value"


@pytest.mark.asyncio
async def test_send_command_to_device_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.send_command_to_device(
            device_manager.SendCommandToDeviceRequest(),
            name="name_value",
            binary_data=b"binary_data_blob",
            subfolder="subfolder_value",
        )


def test_bind_device_to_gateway(
    transport: str = "grpc", request_type=device_manager.BindDeviceToGatewayRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.bind_device_to_gateway), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.BindDeviceToGatewayResponse()

        response = client.bind_device_to_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.BindDeviceToGatewayRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.BindDeviceToGatewayResponse)


def test_bind_device_to_gateway_from_dict():
    test_bind_device_to_gateway(request_type=dict)


@pytest.mark.asyncio
async def test_bind_device_to_gateway_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.BindDeviceToGatewayRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.bind_device_to_gateway), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.BindDeviceToGatewayResponse()
        )

        response = await client.bind_device_to_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.BindDeviceToGatewayResponse)


def test_bind_device_to_gateway_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.BindDeviceToGatewayRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.bind_device_to_gateway), "__call__"
    ) as call:
        call.return_value = device_manager.BindDeviceToGatewayResponse()

        client.bind_device_to_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_bind_device_to_gateway_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.BindDeviceToGatewayRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.bind_device_to_gateway), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.BindDeviceToGatewayResponse()
        )

        await client.bind_device_to_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_bind_device_to_gateway_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.bind_device_to_gateway), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.BindDeviceToGatewayResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.bind_device_to_gateway(
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].gateway_id == "gateway_id_value"

        assert args[0].device_id == "device_id_value"


def test_bind_device_to_gateway_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.bind_device_to_gateway(
            device_manager.BindDeviceToGatewayRequest(),
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )


@pytest.mark.asyncio
async def test_bind_device_to_gateway_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.bind_device_to_gateway), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.BindDeviceToGatewayResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.BindDeviceToGatewayResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.bind_device_to_gateway(
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].gateway_id == "gateway_id_value"

        assert args[0].device_id == "device_id_value"


@pytest.mark.asyncio
async def test_bind_device_to_gateway_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.bind_device_to_gateway(
            device_manager.BindDeviceToGatewayRequest(),
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )


def test_unbind_device_from_gateway(
    transport: str = "grpc", request_type=device_manager.UnbindDeviceFromGatewayRequest
):
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.unbind_device_from_gateway), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.UnbindDeviceFromGatewayResponse()

        response = client.unbind_device_from_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == device_manager.UnbindDeviceFromGatewayRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.UnbindDeviceFromGatewayResponse)


def test_unbind_device_from_gateway_from_dict():
    test_unbind_device_from_gateway(request_type=dict)


@pytest.mark.asyncio
async def test_unbind_device_from_gateway_async(transport: str = "grpc_asyncio"):
    client = DeviceManagerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = device_manager.UnbindDeviceFromGatewayRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.unbind_device_from_gateway), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.UnbindDeviceFromGatewayResponse()
        )

        response = await client.unbind_device_from_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.UnbindDeviceFromGatewayResponse)


def test_unbind_device_from_gateway_field_headers():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.UnbindDeviceFromGatewayRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.unbind_device_from_gateway), "__call__"
    ) as call:
        call.return_value = device_manager.UnbindDeviceFromGatewayResponse()

        client.unbind_device_from_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_unbind_device_from_gateway_field_headers_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.UnbindDeviceFromGatewayRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.unbind_device_from_gateway), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.UnbindDeviceFromGatewayResponse()
        )

        await client.unbind_device_from_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_unbind_device_from_gateway_flattened():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.unbind_device_from_gateway), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.UnbindDeviceFromGatewayResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.unbind_device_from_gateway(
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].gateway_id == "gateway_id_value"

        assert args[0].device_id == "device_id_value"


def test_unbind_device_from_gateway_flattened_error():
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.unbind_device_from_gateway(
            device_manager.UnbindDeviceFromGatewayRequest(),
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )


@pytest.mark.asyncio
async def test_unbind_device_from_gateway_flattened_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.unbind_device_from_gateway), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.UnbindDeviceFromGatewayResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.UnbindDeviceFromGatewayResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.unbind_device_from_gateway(
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].gateway_id == "gateway_id_value"

        assert args[0].device_id == "device_id_value"


@pytest.mark.asyncio
async def test_unbind_device_from_gateway_flattened_error_async():
    client = DeviceManagerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.unbind_device_from_gateway(
            device_manager.UnbindDeviceFromGatewayRequest(),
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DeviceManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DeviceManagerClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DeviceManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DeviceManagerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DeviceManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DeviceManagerClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DeviceManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = DeviceManagerClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DeviceManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DeviceManagerGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DeviceManagerClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.DeviceManagerGrpcTransport,)


def test_device_manager_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.DeviceManagerTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_device_manager_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.iot_v1.services.device_manager.transports.DeviceManagerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DeviceManagerTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_device_registry",
        "get_device_registry",
        "update_device_registry",
        "delete_device_registry",
        "list_device_registries",
        "create_device",
        "get_device",
        "update_device",
        "delete_device",
        "list_devices",
        "modify_cloud_to_device_config",
        "list_device_config_versions",
        "list_device_states",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
        "send_command_to_device",
        "bind_device_to_gateway",
        "unbind_device_from_gateway",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_device_manager_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.iot_v1.services.device_manager.transports.DeviceManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.DeviceManagerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudiot",
            ),
            quota_project_id="octopus",
        )


def test_device_manager_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        DeviceManagerClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudiot",
            ),
            quota_project_id=None,
        )


def test_device_manager_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.DeviceManagerGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudiot",
            ),
            quota_project_id="octopus",
        )


def test_device_manager_host_no_port():
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudiot.googleapis.com"
        ),
    )
    assert client._transport._host == "cloudiot.googleapis.com:443"


def test_device_manager_host_with_port():
    client = DeviceManagerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudiot.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "cloudiot.googleapis.com:8000"


def test_device_manager_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.DeviceManagerGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_device_manager_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.DeviceManagerGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_device_manager_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.DeviceManagerGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=(
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/cloudiot",
        ),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_device_manager_grpc_asyncio_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.DeviceManagerGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=(
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/cloudiot",
        ),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_device_manager_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.DeviceManagerGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudiot",
            ),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_device_manager_grpc_asyncio_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.DeviceManagerGrpcAsyncIOTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudiot",
            ),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_registry_path():
    project = "squid"
    location = "clam"
    registry = "whelk"

    expected = "projects/{project}/locations/{location}/registries/{registry}".format(
        project=project, location=location, registry=registry,
    )
    actual = DeviceManagerClient.registry_path(project, location, registry)
    assert expected == actual


def test_parse_registry_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "registry": "nudibranch",
    }
    path = DeviceManagerClient.registry_path(**expected)

    # Check that the path construction is reversible.
    actual = DeviceManagerClient.parse_registry_path(path)
    assert expected == actual


def test_device_path():
    project = "squid"
    location = "clam"
    registry = "whelk"
    device = "octopus"

    expected = "projects/{project}/locations/{location}/registries/{registry}/devices/{device}".format(
        project=project, location=location, registry=registry, device=device,
    )
    actual = DeviceManagerClient.device_path(project, location, registry, device)
    assert expected == actual


def test_parse_device_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "registry": "cuttlefish",
        "device": "mussel",
    }
    path = DeviceManagerClient.device_path(**expected)

    # Check that the path construction is reversible.
    actual = DeviceManagerClient.parse_device_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DeviceManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DeviceManagerClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DeviceManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DeviceManagerClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
