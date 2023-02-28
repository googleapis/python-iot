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
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import Iterable
import json
import math

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.iot_v1.services.device_manager import (
    DeviceManagerAsyncClient,
    DeviceManagerClient,
    pagers,
    transports,
)
from google.cloud.iot_v1.types import device_manager, resources


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
    "client_class,transport_name",
    [
        (DeviceManagerClient, "grpc"),
        (DeviceManagerAsyncClient, "grpc_asyncio"),
        (DeviceManagerClient, "rest"),
    ],
)
def test_device_manager_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "cloudiot.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudiot.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.DeviceManagerGrpcTransport, "grpc"),
        (transports.DeviceManagerGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.DeviceManagerRestTransport, "rest"),
    ],
)
def test_device_manager_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (DeviceManagerClient, "grpc"),
        (DeviceManagerAsyncClient, "grpc_asyncio"),
        (DeviceManagerClient, "rest"),
    ],
)
def test_device_manager_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "cloudiot.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudiot.googleapis.com"
        )


def test_device_manager_client_get_transport_class():
    transport = DeviceManagerClient.get_transport_class()
    available_transports = [
        transports.DeviceManagerGrpcTransport,
        transports.DeviceManagerRestTransport,
    ]
    assert transport in available_transports

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
        (DeviceManagerClient, transports.DeviceManagerRestTransport, "rest"),
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
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
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
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (DeviceManagerClient, transports.DeviceManagerGrpcTransport, "grpc", "true"),
        (
            DeviceManagerAsyncClient,
            transports.DeviceManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (DeviceManagerClient, transports.DeviceManagerGrpcTransport, "grpc", "false"),
        (
            DeviceManagerAsyncClient,
            transports.DeviceManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (DeviceManagerClient, transports.DeviceManagerRestTransport, "rest", "true"),
        (DeviceManagerClient, transports.DeviceManagerRestTransport, "rest", "false"),
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
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_device_manager_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class", [DeviceManagerClient, DeviceManagerAsyncClient]
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
def test_device_manager_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DeviceManagerClient, transports.DeviceManagerGrpcTransport, "grpc"),
        (
            DeviceManagerAsyncClient,
            transports.DeviceManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (DeviceManagerClient, transports.DeviceManagerRestTransport, "rest"),
    ],
)
def test_device_manager_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            DeviceManagerClient,
            transports.DeviceManagerGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            DeviceManagerAsyncClient,
            transports.DeviceManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (DeviceManagerClient, transports.DeviceManagerRestTransport, "rest", None),
    ],
)
def test_device_manager_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
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
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            DeviceManagerClient,
            transports.DeviceManagerGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            DeviceManagerAsyncClient,
            transports.DeviceManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_device_manager_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "cloudiot.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudiot",
            ),
            scopes=None,
            default_host="cloudiot.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.CreateDeviceRegistryRequest,
        dict,
    ],
)
def test_create_device_registry(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry(
            id="id_value",
            name="name_value",
            log_level=resources.LogLevel.NONE,
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


def test_create_device_registry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_device_registry), "__call__"
    ) as call:
        client.create_device_registry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.CreateDeviceRegistryRequest()


@pytest.mark.asyncio
async def test_create_device_registry_async(
    transport: str = "grpc_asyncio",
    request_type=device_manager.CreateDeviceRegistryRequest,
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceRegistry(
                id="id_value",
                name="name_value",
                log_level=resources.LogLevel.NONE,
            )
        )
        response = await client.create_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.CreateDeviceRegistryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceRegistry)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.log_level == resources.LogLevel.NONE


@pytest.mark.asyncio
async def test_create_device_registry_async_from_dict():
    await test_create_device_registry_async(request_type=dict)


def test_create_device_registry_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.CreateDeviceRegistryRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_device_registry), "__call__"
    ) as call:
        call.return_value = resources.DeviceRegistry()
        client.create_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_device_registry_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.CreateDeviceRegistryRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_device_registry), "__call__"
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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_device_registry_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_device_registry), "__call__"
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].device_registry
        mock_val = resources.DeviceRegistry(id="id_value")
        assert arg == mock_val


def test_create_device_registry_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

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
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_device_registry), "__call__"
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].device_registry
        mock_val = resources.DeviceRegistry(id="id_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_device_registry_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_device_registry(
            device_manager.CreateDeviceRegistryRequest(),
            parent="parent_value",
            device_registry=resources.DeviceRegistry(id="id_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.GetDeviceRegistryRequest,
        dict,
    ],
)
def test_get_device_registry(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry(
            id="id_value",
            name="name_value",
            log_level=resources.LogLevel.NONE,
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


def test_get_device_registry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_device_registry), "__call__"
    ) as call:
        client.get_device_registry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.GetDeviceRegistryRequest()


@pytest.mark.asyncio
async def test_get_device_registry_async(
    transport: str = "grpc_asyncio",
    request_type=device_manager.GetDeviceRegistryRequest,
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceRegistry(
                id="id_value",
                name="name_value",
                log_level=resources.LogLevel.NONE,
            )
        )
        response = await client.get_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.GetDeviceRegistryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceRegistry)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.log_level == resources.LogLevel.NONE


@pytest.mark.asyncio
async def test_get_device_registry_async_from_dict():
    await test_get_device_registry_async(request_type=dict)


def test_get_device_registry_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.GetDeviceRegistryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_device_registry), "__call__"
    ) as call:
        call.return_value = resources.DeviceRegistry()
        client.get_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_device_registry_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.GetDeviceRegistryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_device_registry), "__call__"
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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_device_registry_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_device_registry(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_device_registry_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_device_registry(
            device_manager.GetDeviceRegistryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_device_registry_flattened_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceRegistry()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_device_registry(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_device_registry_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_device_registry(
            device_manager.GetDeviceRegistryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.UpdateDeviceRegistryRequest,
        dict,
    ],
)
def test_update_device_registry(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry(
            id="id_value",
            name="name_value",
            log_level=resources.LogLevel.NONE,
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


def test_update_device_registry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_device_registry), "__call__"
    ) as call:
        client.update_device_registry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.UpdateDeviceRegistryRequest()


@pytest.mark.asyncio
async def test_update_device_registry_async(
    transport: str = "grpc_asyncio",
    request_type=device_manager.UpdateDeviceRegistryRequest,
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceRegistry(
                id="id_value",
                name="name_value",
                log_level=resources.LogLevel.NONE,
            )
        )
        response = await client.update_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.UpdateDeviceRegistryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceRegistry)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.log_level == resources.LogLevel.NONE


@pytest.mark.asyncio
async def test_update_device_registry_async_from_dict():
    await test_update_device_registry_async(request_type=dict)


def test_update_device_registry_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.UpdateDeviceRegistryRequest()

    request.device_registry.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_device_registry), "__call__"
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
        "device_registry.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_device_registry_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.UpdateDeviceRegistryRequest()

    request.device_registry.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_device_registry), "__call__"
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
        "device_registry.name=name_value",
    ) in kw["metadata"]


def test_update_device_registry_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceRegistry()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_device_registry(
            device_registry=resources.DeviceRegistry(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].device_registry
        mock_val = resources.DeviceRegistry(id="id_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_device_registry_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_device_registry(
            device_manager.UpdateDeviceRegistryRequest(),
            device_registry=resources.DeviceRegistry(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_device_registry_flattened_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_device_registry), "__call__"
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
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].device_registry
        mock_val = resources.DeviceRegistry(id="id_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_device_registry_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_device_registry(
            device_manager.UpdateDeviceRegistryRequest(),
            device_registry=resources.DeviceRegistry(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.DeleteDeviceRegistryRequest,
        dict,
    ],
)
def test_delete_device_registry(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_device_registry), "__call__"
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


def test_delete_device_registry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_device_registry), "__call__"
    ) as call:
        client.delete_device_registry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.DeleteDeviceRegistryRequest()


@pytest.mark.asyncio
async def test_delete_device_registry_async(
    transport: str = "grpc_asyncio",
    request_type=device_manager.DeleteDeviceRegistryRequest,
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.DeleteDeviceRegistryRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_device_registry_async_from_dict():
    await test_delete_device_registry_async(request_type=dict)


def test_delete_device_registry_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.DeleteDeviceRegistryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_device_registry), "__call__"
    ) as call:
        call.return_value = None
        client.delete_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_device_registry_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.DeleteDeviceRegistryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_device_registry), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_device_registry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_device_registry_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_device_registry(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_device_registry_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_device_registry(
            device_manager.DeleteDeviceRegistryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_device_registry_flattened_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_device_registry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_device_registry(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_device_registry_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_device_registry(
            device_manager.DeleteDeviceRegistryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.ListDeviceRegistriesRequest,
        dict,
    ],
)
def test_list_device_registries(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_registries), "__call__"
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


def test_list_device_registries_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_registries), "__call__"
    ) as call:
        client.list_device_registries()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.ListDeviceRegistriesRequest()


@pytest.mark.asyncio
async def test_list_device_registries_async(
    transport: str = "grpc_asyncio",
    request_type=device_manager.ListDeviceRegistriesRequest,
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_registries), "__call__"
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
        assert args[0] == device_manager.ListDeviceRegistriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeviceRegistriesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_device_registries_async_from_dict():
    await test_list_device_registries_async(request_type=dict)


def test_list_device_registries_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDeviceRegistriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_registries), "__call__"
    ) as call:
        call.return_value = device_manager.ListDeviceRegistriesResponse()
        client.list_device_registries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_device_registries_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDeviceRegistriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_registries), "__call__"
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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_device_registries_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_registries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceRegistriesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_device_registries(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_device_registries_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_device_registries(
            device_manager.ListDeviceRegistriesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_device_registries_flattened_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_registries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceRegistriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceRegistriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_device_registries(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_device_registries_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_device_registries(
            device_manager.ListDeviceRegistriesRequest(),
            parent="parent_value",
        )


def test_list_device_registries_pager(transport_name: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_registries), "__call__"
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
                device_registries=[],
                next_page_token="def",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                ],
                next_page_token="ghi",
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

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.DeviceRegistry) for i in results)


def test_list_device_registries_pages(transport_name: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_registries), "__call__"
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
                device_registries=[],
                next_page_token="def",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                ],
                next_page_token="ghi",
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
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_registries),
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
                device_registries=[],
                next_page_token="def",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                ],
                next_page_token="ghi",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_device_registries(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.DeviceRegistry) for i in responses)


@pytest.mark.asyncio
async def test_list_device_registries_async_pages():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_registries),
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
                device_registries=[],
                next_page_token="def",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                ],
                next_page_token="ghi",
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
        async for page_ in (
            await client.list_device_registries(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.CreateDeviceRequest,
        dict,
    ],
)
def test_create_device(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_device), "__call__") as call:
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


def test_create_device_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_device), "__call__") as call:
        client.create_device()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.CreateDeviceRequest()


@pytest.mark.asyncio
async def test_create_device_async(
    transport: str = "grpc_asyncio", request_type=device_manager.CreateDeviceRequest
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_device), "__call__") as call:
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
        assert args[0] == device_manager.CreateDeviceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Device)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.num_id == 636
    assert response.blocked is True
    assert response.log_level == resources.LogLevel.NONE


@pytest.mark.asyncio
async def test_create_device_async_from_dict():
    await test_create_device_async(request_type=dict)


def test_create_device_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.CreateDeviceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_device), "__call__") as call:
        call.return_value = resources.Device()
        client.create_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_device_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.CreateDeviceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_device), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Device())
        await client.create_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_device_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_device(
            parent="parent_value",
            device=resources.Device(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].device
        mock_val = resources.Device(id="id_value")
        assert arg == mock_val


def test_create_device_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

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
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Device())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_device(
            parent="parent_value",
            device=resources.Device(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].device
        mock_val = resources.Device(id="id_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_device_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_device(
            device_manager.CreateDeviceRequest(),
            parent="parent_value",
            device=resources.Device(id="id_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.GetDeviceRequest,
        dict,
    ],
)
def test_get_device(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_device), "__call__") as call:
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


def test_get_device_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_device), "__call__") as call:
        client.get_device()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.GetDeviceRequest()


@pytest.mark.asyncio
async def test_get_device_async(
    transport: str = "grpc_asyncio", request_type=device_manager.GetDeviceRequest
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_device), "__call__") as call:
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
        assert args[0] == device_manager.GetDeviceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Device)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.num_id == 636
    assert response.blocked is True
    assert response.log_level == resources.LogLevel.NONE


@pytest.mark.asyncio
async def test_get_device_async_from_dict():
    await test_get_device_async(request_type=dict)


def test_get_device_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.GetDeviceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_device), "__call__") as call:
        call.return_value = resources.Device()
        client.get_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_device_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.GetDeviceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_device), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Device())
        await client.get_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_device_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_device(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_device_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_device(
            device_manager.GetDeviceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_device_flattened_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Device())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_device(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_device_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_device(
            device_manager.GetDeviceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.UpdateDeviceRequest,
        dict,
    ],
)
def test_update_device(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_device), "__call__") as call:
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


def test_update_device_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_device), "__call__") as call:
        client.update_device()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.UpdateDeviceRequest()


@pytest.mark.asyncio
async def test_update_device_async(
    transport: str = "grpc_asyncio", request_type=device_manager.UpdateDeviceRequest
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_device), "__call__") as call:
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
        assert args[0] == device_manager.UpdateDeviceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Device)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.num_id == 636
    assert response.blocked is True
    assert response.log_level == resources.LogLevel.NONE


@pytest.mark.asyncio
async def test_update_device_async_from_dict():
    await test_update_device_async(request_type=dict)


def test_update_device_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.UpdateDeviceRequest()

    request.device.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_device), "__call__") as call:
        call.return_value = resources.Device()
        client.update_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "device.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_device_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.UpdateDeviceRequest()

    request.device.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_device), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Device())
        await client.update_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "device.name=name_value",
    ) in kw["metadata"]


def test_update_device_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_device(
            device=resources.Device(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].device
        mock_val = resources.Device(id="id_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_device_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_device(
            device_manager.UpdateDeviceRequest(),
            device=resources.Device(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_device_flattened_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Device()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Device())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_device(
            device=resources.Device(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].device
        mock_val = resources.Device(id="id_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_device_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_device(
            device_manager.UpdateDeviceRequest(),
            device=resources.Device(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.DeleteDeviceRequest,
        dict,
    ],
)
def test_delete_device(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.DeleteDeviceRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_device_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_device), "__call__") as call:
        client.delete_device()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.DeleteDeviceRequest()


@pytest.mark.asyncio
async def test_delete_device_async(
    transport: str = "grpc_asyncio", request_type=device_manager.DeleteDeviceRequest
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.DeleteDeviceRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_device_async_from_dict():
    await test_delete_device_async(request_type=dict)


def test_delete_device_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.DeleteDeviceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_device), "__call__") as call:
        call.return_value = None
        client.delete_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_device_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.DeleteDeviceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_device), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_device_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_device(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_device_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_device(
            device_manager.DeleteDeviceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_device_flattened_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_device), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_device(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_device_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_device(
            device_manager.DeleteDeviceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.ListDevicesRequest,
        dict,
    ],
)
def test_list_devices(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_devices), "__call__") as call:
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


def test_list_devices_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_devices), "__call__") as call:
        client.list_devices()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.ListDevicesRequest()


@pytest.mark.asyncio
async def test_list_devices_async(
    transport: str = "grpc_asyncio", request_type=device_manager.ListDevicesRequest
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_devices), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDevicesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_devices(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.ListDevicesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDevicesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_devices_async_from_dict():
    await test_list_devices_async(request_type=dict)


def test_list_devices_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDevicesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_devices), "__call__") as call:
        call.return_value = device_manager.ListDevicesResponse()
        client.list_devices(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_devices_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDevicesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_devices), "__call__") as call:
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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_devices_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_devices), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDevicesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_devices(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_devices_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_devices(
            device_manager.ListDevicesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_devices_flattened_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_devices), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDevicesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDevicesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_devices(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_devices_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_devices(
            device_manager.ListDevicesRequest(),
            parent="parent_value",
        )


def test_list_devices_pager(transport_name: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_devices), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                    resources.Device(),
                    resources.Device(),
                ],
                next_page_token="abc",
            ),
            device_manager.ListDevicesResponse(
                devices=[],
                next_page_token="def",
            ),
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                ],
                next_page_token="ghi",
            ),
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                    resources.Device(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_devices(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Device) for i in results)


def test_list_devices_pages(transport_name: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_devices), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                    resources.Device(),
                    resources.Device(),
                ],
                next_page_token="abc",
            ),
            device_manager.ListDevicesResponse(
                devices=[],
                next_page_token="def",
            ),
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                ],
                next_page_token="ghi",
            ),
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                    resources.Device(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_devices(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_devices_async_pager():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_devices), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                    resources.Device(),
                    resources.Device(),
                ],
                next_page_token="abc",
            ),
            device_manager.ListDevicesResponse(
                devices=[],
                next_page_token="def",
            ),
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                ],
                next_page_token="ghi",
            ),
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                    resources.Device(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_devices(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Device) for i in responses)


@pytest.mark.asyncio
async def test_list_devices_async_pages():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_devices), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                    resources.Device(),
                    resources.Device(),
                ],
                next_page_token="abc",
            ),
            device_manager.ListDevicesResponse(
                devices=[],
                next_page_token="def",
            ),
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                ],
                next_page_token="ghi",
            ),
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                    resources.Device(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_devices(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.ModifyCloudToDeviceConfigRequest,
        dict,
    ],
)
def test_modify_cloud_to_device_config(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_cloud_to_device_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceConfig(
            version=774,
            binary_data=b"binary_data_blob",
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


def test_modify_cloud_to_device_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_cloud_to_device_config), "__call__"
    ) as call:
        client.modify_cloud_to_device_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.ModifyCloudToDeviceConfigRequest()


@pytest.mark.asyncio
async def test_modify_cloud_to_device_config_async(
    transport: str = "grpc_asyncio",
    request_type=device_manager.ModifyCloudToDeviceConfigRequest,
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_cloud_to_device_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceConfig(
                version=774,
                binary_data=b"binary_data_blob",
            )
        )
        response = await client.modify_cloud_to_device_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.ModifyCloudToDeviceConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceConfig)
    assert response.version == 774
    assert response.binary_data == b"binary_data_blob"


@pytest.mark.asyncio
async def test_modify_cloud_to_device_config_async_from_dict():
    await test_modify_cloud_to_device_config_async(request_type=dict)


def test_modify_cloud_to_device_config_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ModifyCloudToDeviceConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_cloud_to_device_config), "__call__"
    ) as call:
        call.return_value = resources.DeviceConfig()
        client.modify_cloud_to_device_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_modify_cloud_to_device_config_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ModifyCloudToDeviceConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_cloud_to_device_config), "__call__"
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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_modify_cloud_to_device_config_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_cloud_to_device_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.modify_cloud_to_device_config(
            name="name_value",
            binary_data=b"binary_data_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].binary_data
        mock_val = b"binary_data_blob"
        assert arg == mock_val


def test_modify_cloud_to_device_config_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

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
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_cloud_to_device_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.DeviceConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.DeviceConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.modify_cloud_to_device_config(
            name="name_value",
            binary_data=b"binary_data_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].binary_data
        mock_val = b"binary_data_blob"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_modify_cloud_to_device_config_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.modify_cloud_to_device_config(
            device_manager.ModifyCloudToDeviceConfigRequest(),
            name="name_value",
            binary_data=b"binary_data_blob",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.ListDeviceConfigVersionsRequest,
        dict,
    ],
)
def test_list_device_config_versions(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_config_versions), "__call__"
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


def test_list_device_config_versions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_config_versions), "__call__"
    ) as call:
        client.list_device_config_versions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.ListDeviceConfigVersionsRequest()


@pytest.mark.asyncio
async def test_list_device_config_versions_async(
    transport: str = "grpc_asyncio",
    request_type=device_manager.ListDeviceConfigVersionsRequest,
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_config_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceConfigVersionsResponse()
        )
        response = await client.list_device_config_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.ListDeviceConfigVersionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.ListDeviceConfigVersionsResponse)


@pytest.mark.asyncio
async def test_list_device_config_versions_async_from_dict():
    await test_list_device_config_versions_async(request_type=dict)


def test_list_device_config_versions_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDeviceConfigVersionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_config_versions), "__call__"
    ) as call:
        call.return_value = device_manager.ListDeviceConfigVersionsResponse()
        client.list_device_config_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_device_config_versions_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDeviceConfigVersionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_config_versions), "__call__"
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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_list_device_config_versions_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_config_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceConfigVersionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_device_config_versions(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_list_device_config_versions_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_device_config_versions(
            device_manager.ListDeviceConfigVersionsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_list_device_config_versions_flattened_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_config_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceConfigVersionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceConfigVersionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_device_config_versions(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_device_config_versions_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_device_config_versions(
            device_manager.ListDeviceConfigVersionsRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.ListDeviceStatesRequest,
        dict,
    ],
)
def test_list_device_states(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_states), "__call__"
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


def test_list_device_states_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_states), "__call__"
    ) as call:
        client.list_device_states()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.ListDeviceStatesRequest()


@pytest.mark.asyncio
async def test_list_device_states_async(
    transport: str = "grpc_asyncio", request_type=device_manager.ListDeviceStatesRequest
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_states), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceStatesResponse()
        )
        response = await client.list_device_states(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.ListDeviceStatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.ListDeviceStatesResponse)


@pytest.mark.asyncio
async def test_list_device_states_async_from_dict():
    await test_list_device_states_async(request_type=dict)


def test_list_device_states_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDeviceStatesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_states), "__call__"
    ) as call:
        call.return_value = device_manager.ListDeviceStatesResponse()
        client.list_device_states(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_device_states_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.ListDeviceStatesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_states), "__call__"
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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_list_device_states_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_states), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceStatesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_device_states(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_list_device_states_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_device_states(
            device_manager.ListDeviceStatesRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_list_device_states_flattened_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_device_states), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = device_manager.ListDeviceStatesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.ListDeviceStatesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_device_states(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_device_states_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_device_states(
            device_manager.ListDeviceStatesRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.SetIamPolicyRequest,
        dict,
    ],
)
def test_set_iam_policy(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )
        response = client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.SetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_set_iam_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        client.set_iam_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.SetIamPolicyRequest()


@pytest.mark.asyncio
async def test_set_iam_policy_async(
    transport: str = "grpc_asyncio", request_type=iam_policy_pb2.SetIamPolicyRequest
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )
        response = await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.SetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_set_iam_policy_async_from_dict():
    await test_set_iam_policy_async(request_type=dict)


def test_set_iam_policy_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()
        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())
        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


def test_set_iam_policy_from_dict_foreign():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()
        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
                "update_mask": field_mask_pb2.FieldMask(paths=["paths_value"]),
            }
        )
        call.assert_called()


def test_set_iam_policy_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_iam_policy(
            resource="resource_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource
        mock_val = "resource_value"
        assert arg == mock_val


def test_set_iam_policy_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_iam_policy(
            iam_policy_pb2.SetIamPolicyRequest(),
            resource="resource_value",
        )


@pytest.mark.asyncio
async def test_set_iam_policy_flattened_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_iam_policy(
            resource="resource_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource
        mock_val = "resource_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_iam_policy_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_iam_policy(
            iam_policy_pb2.SetIamPolicyRequest(),
            resource="resource_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )
        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.GetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_get_iam_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        client.get_iam_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.GetIamPolicyRequest()


@pytest.mark.asyncio
async def test_get_iam_policy_async(
    transport: str = "grpc_asyncio", request_type=iam_policy_pb2.GetIamPolicyRequest
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )
        response = await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.GetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_get_iam_policy_async_from_dict():
    await test_get_iam_policy_async(request_type=dict)


def test_get_iam_policy_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()
        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())
        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


def test_get_iam_policy_from_dict_foreign():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()
        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_get_iam_policy_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_iam_policy(
            resource="resource_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource
        mock_val = "resource_value"
        assert arg == mock_val


def test_get_iam_policy_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_iam_policy(
            iam_policy_pb2.GetIamPolicyRequest(),
            resource="resource_value",
        )


@pytest.mark.asyncio
async def test_get_iam_policy_flattened_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_iam_policy(
            resource="resource_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource
        mock_val = "resource_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_iam_policy_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_iam_policy(
            iam_policy_pb2.GetIamPolicyRequest(),
            resource="resource_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.TestIamPermissionsRequest,
        dict,
    ],
)
def test_test_iam_permissions(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )
        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.TestIamPermissionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        client.test_iam_permissions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.TestIamPermissionsRequest()


@pytest.mark.asyncio
async def test_test_iam_permissions_async(
    transport: str = "grpc_asyncio",
    request_type=iam_policy_pb2.TestIamPermissionsRequest,
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse(
                permissions=["permissions_value"],
            )
        )
        response = await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.TestIamPermissionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_async_from_dict():
    await test_test_iam_permissions_async(request_type=dict)


def test_test_iam_permissions_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()
        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )
        await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


def test_test_iam_permissions_from_dict_foreign():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()
        response = client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


def test_test_iam_permissions_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.test_iam_permissions(
            resource="resource_value",
            permissions=["permissions_value"],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource
        mock_val = "resource_value"
        assert arg == mock_val
        arg = args[0].permissions
        mock_val = ["permissions_value"]
        assert arg == mock_val


def test_test_iam_permissions_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.test_iam_permissions(
            iam_policy_pb2.TestIamPermissionsRequest(),
            resource="resource_value",
            permissions=["permissions_value"],
        )


@pytest.mark.asyncio
async def test_test_iam_permissions_flattened_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.test_iam_permissions(
            resource="resource_value",
            permissions=["permissions_value"],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource
        mock_val = "resource_value"
        assert arg == mock_val
        arg = args[0].permissions
        mock_val = ["permissions_value"]
        assert arg == mock_val


@pytest.mark.asyncio
async def test_test_iam_permissions_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.test_iam_permissions(
            iam_policy_pb2.TestIamPermissionsRequest(),
            resource="resource_value",
            permissions=["permissions_value"],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.SendCommandToDeviceRequest,
        dict,
    ],
)
def test_send_command_to_device(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_command_to_device), "__call__"
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


def test_send_command_to_device_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_command_to_device), "__call__"
    ) as call:
        client.send_command_to_device()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.SendCommandToDeviceRequest()


@pytest.mark.asyncio
async def test_send_command_to_device_async(
    transport: str = "grpc_asyncio",
    request_type=device_manager.SendCommandToDeviceRequest,
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_command_to_device), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.SendCommandToDeviceResponse()
        )
        response = await client.send_command_to_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.SendCommandToDeviceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.SendCommandToDeviceResponse)


@pytest.mark.asyncio
async def test_send_command_to_device_async_from_dict():
    await test_send_command_to_device_async(request_type=dict)


def test_send_command_to_device_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.SendCommandToDeviceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_command_to_device), "__call__"
    ) as call:
        call.return_value = device_manager.SendCommandToDeviceResponse()
        client.send_command_to_device(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_send_command_to_device_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.SendCommandToDeviceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_command_to_device), "__call__"
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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_send_command_to_device_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_command_to_device), "__call__"
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
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].binary_data
        mock_val = b"binary_data_blob"
        assert arg == mock_val
        arg = args[0].subfolder
        mock_val = "subfolder_value"
        assert arg == mock_val


def test_send_command_to_device_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

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
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_command_to_device), "__call__"
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
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].binary_data
        mock_val = b"binary_data_blob"
        assert arg == mock_val
        arg = args[0].subfolder
        mock_val = "subfolder_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_send_command_to_device_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.send_command_to_device(
            device_manager.SendCommandToDeviceRequest(),
            name="name_value",
            binary_data=b"binary_data_blob",
            subfolder="subfolder_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.BindDeviceToGatewayRequest,
        dict,
    ],
)
def test_bind_device_to_gateway(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bind_device_to_gateway), "__call__"
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


def test_bind_device_to_gateway_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bind_device_to_gateway), "__call__"
    ) as call:
        client.bind_device_to_gateway()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.BindDeviceToGatewayRequest()


@pytest.mark.asyncio
async def test_bind_device_to_gateway_async(
    transport: str = "grpc_asyncio",
    request_type=device_manager.BindDeviceToGatewayRequest,
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bind_device_to_gateway), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.BindDeviceToGatewayResponse()
        )
        response = await client.bind_device_to_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.BindDeviceToGatewayRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.BindDeviceToGatewayResponse)


@pytest.mark.asyncio
async def test_bind_device_to_gateway_async_from_dict():
    await test_bind_device_to_gateway_async(request_type=dict)


def test_bind_device_to_gateway_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.BindDeviceToGatewayRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bind_device_to_gateway), "__call__"
    ) as call:
        call.return_value = device_manager.BindDeviceToGatewayResponse()
        client.bind_device_to_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_bind_device_to_gateway_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.BindDeviceToGatewayRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bind_device_to_gateway), "__call__"
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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_bind_device_to_gateway_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bind_device_to_gateway), "__call__"
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].gateway_id
        mock_val = "gateway_id_value"
        assert arg == mock_val
        arg = args[0].device_id
        mock_val = "device_id_value"
        assert arg == mock_val


def test_bind_device_to_gateway_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

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
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bind_device_to_gateway), "__call__"
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].gateway_id
        mock_val = "gateway_id_value"
        assert arg == mock_val
        arg = args[0].device_id
        mock_val = "device_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_bind_device_to_gateway_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.bind_device_to_gateway(
            device_manager.BindDeviceToGatewayRequest(),
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.UnbindDeviceFromGatewayRequest,
        dict,
    ],
)
def test_unbind_device_from_gateway(request_type, transport: str = "grpc"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.unbind_device_from_gateway), "__call__"
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


def test_unbind_device_from_gateway_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.unbind_device_from_gateway), "__call__"
    ) as call:
        client.unbind_device_from_gateway()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.UnbindDeviceFromGatewayRequest()


@pytest.mark.asyncio
async def test_unbind_device_from_gateway_async(
    transport: str = "grpc_asyncio",
    request_type=device_manager.UnbindDeviceFromGatewayRequest,
):
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.unbind_device_from_gateway), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            device_manager.UnbindDeviceFromGatewayResponse()
        )
        response = await client.unbind_device_from_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == device_manager.UnbindDeviceFromGatewayRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.UnbindDeviceFromGatewayResponse)


@pytest.mark.asyncio
async def test_unbind_device_from_gateway_async_from_dict():
    await test_unbind_device_from_gateway_async(request_type=dict)


def test_unbind_device_from_gateway_field_headers():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.UnbindDeviceFromGatewayRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.unbind_device_from_gateway), "__call__"
    ) as call:
        call.return_value = device_manager.UnbindDeviceFromGatewayResponse()
        client.unbind_device_from_gateway(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_unbind_device_from_gateway_field_headers_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = device_manager.UnbindDeviceFromGatewayRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.unbind_device_from_gateway), "__call__"
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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_unbind_device_from_gateway_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.unbind_device_from_gateway), "__call__"
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].gateway_id
        mock_val = "gateway_id_value"
        assert arg == mock_val
        arg = args[0].device_id
        mock_val = "device_id_value"
        assert arg == mock_val


def test_unbind_device_from_gateway_flattened_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

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
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.unbind_device_from_gateway), "__call__"
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].gateway_id
        mock_val = "gateway_id_value"
        assert arg == mock_val
        arg = args[0].device_id
        mock_val = "device_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_unbind_device_from_gateway_flattened_error_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.unbind_device_from_gateway(
            device_manager.UnbindDeviceFromGatewayRequest(),
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.CreateDeviceRegistryRequest,
        dict,
    ],
)
def test_create_device_registry_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["device_registry"] = {
        "id": "id_value",
        "name": "name_value",
        "event_notification_configs": [
            {
                "subfolder_matches": "subfolder_matches_value",
                "pubsub_topic_name": "pubsub_topic_name_value",
            }
        ],
        "state_notification_config": {"pubsub_topic_name": "pubsub_topic_name_value"},
        "mqtt_config": {"mqtt_enabled_state": 1},
        "http_config": {"http_enabled_state": 1},
        "log_level": 10,
        "credentials": [
            {
                "public_key_certificate": {
                    "format": 1,
                    "certificate": "certificate_value",
                    "x509_details": {
                        "issuer": "issuer_value",
                        "subject": "subject_value",
                        "start_time": {"seconds": 751, "nanos": 543},
                        "expiry_time": {},
                        "signature_algorithm": "signature_algorithm_value",
                        "public_key_type": "public_key_type_value",
                    },
                }
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.DeviceRegistry(
            id="id_value",
            name="name_value",
            log_level=resources.LogLevel.NONE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.DeviceRegistry.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_device_registry(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceRegistry)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.log_level == resources.LogLevel.NONE


def test_create_device_registry_rest_required_fields(
    request_type=device_manager.CreateDeviceRegistryRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_device_registry._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_device_registry._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.DeviceRegistry()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = resources.DeviceRegistry.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_device_registry(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_device_registry_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_device_registry._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "deviceRegistry",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_device_registry_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_create_device_registry"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_create_device_registry"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.CreateDeviceRegistryRequest.pb(
            device_manager.CreateDeviceRegistryRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.DeviceRegistry.to_json(
            resources.DeviceRegistry()
        )

        request = device_manager.CreateDeviceRegistryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.DeviceRegistry()

        client.create_device_registry(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_device_registry_rest_bad_request(
    transport: str = "rest", request_type=device_manager.CreateDeviceRegistryRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["device_registry"] = {
        "id": "id_value",
        "name": "name_value",
        "event_notification_configs": [
            {
                "subfolder_matches": "subfolder_matches_value",
                "pubsub_topic_name": "pubsub_topic_name_value",
            }
        ],
        "state_notification_config": {"pubsub_topic_name": "pubsub_topic_name_value"},
        "mqtt_config": {"mqtt_enabled_state": 1},
        "http_config": {"http_enabled_state": 1},
        "log_level": 10,
        "credentials": [
            {
                "public_key_certificate": {
                    "format": 1,
                    "certificate": "certificate_value",
                    "x509_details": {
                        "issuer": "issuer_value",
                        "subject": "subject_value",
                        "start_time": {"seconds": 751, "nanos": 543},
                        "expiry_time": {},
                        "signature_algorithm": "signature_algorithm_value",
                        "public_key_type": "public_key_type_value",
                    },
                }
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_device_registry(request)


def test_create_device_registry_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.DeviceRegistry()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            device_registry=resources.DeviceRegistry(id="id_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.DeviceRegistry.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_device_registry(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/registries" % client.transport._host,
            args[1],
        )


def test_create_device_registry_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_device_registry(
            device_manager.CreateDeviceRegistryRequest(),
            parent="parent_value",
            device_registry=resources.DeviceRegistry(id="id_value"),
        )


def test_create_device_registry_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.GetDeviceRegistryRequest,
        dict,
    ],
)
def test_get_device_registry_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.DeviceRegistry(
            id="id_value",
            name="name_value",
            log_level=resources.LogLevel.NONE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.DeviceRegistry.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_device_registry(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceRegistry)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.log_level == resources.LogLevel.NONE


def test_get_device_registry_rest_required_fields(
    request_type=device_manager.GetDeviceRegistryRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_device_registry._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_device_registry._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.DeviceRegistry()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = resources.DeviceRegistry.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_device_registry(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_device_registry_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_device_registry._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_device_registry_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_get_device_registry"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_get_device_registry"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.GetDeviceRegistryRequest.pb(
            device_manager.GetDeviceRegistryRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.DeviceRegistry.to_json(
            resources.DeviceRegistry()
        )

        request = device_manager.GetDeviceRegistryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.DeviceRegistry()

        client.get_device_registry(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_device_registry_rest_bad_request(
    transport: str = "rest", request_type=device_manager.GetDeviceRegistryRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_device_registry(request)


def test_get_device_registry_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.DeviceRegistry()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/registries/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.DeviceRegistry.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_device_registry(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/registries/*}" % client.transport._host,
            args[1],
        )


def test_get_device_registry_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_device_registry(
            device_manager.GetDeviceRegistryRequest(),
            name="name_value",
        )


def test_get_device_registry_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.UpdateDeviceRegistryRequest,
        dict,
    ],
)
def test_update_device_registry_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "device_registry": {
            "name": "projects/sample1/locations/sample2/registries/sample3"
        }
    }
    request_init["device_registry"] = {
        "id": "id_value",
        "name": "projects/sample1/locations/sample2/registries/sample3",
        "event_notification_configs": [
            {
                "subfolder_matches": "subfolder_matches_value",
                "pubsub_topic_name": "pubsub_topic_name_value",
            }
        ],
        "state_notification_config": {"pubsub_topic_name": "pubsub_topic_name_value"},
        "mqtt_config": {"mqtt_enabled_state": 1},
        "http_config": {"http_enabled_state": 1},
        "log_level": 10,
        "credentials": [
            {
                "public_key_certificate": {
                    "format": 1,
                    "certificate": "certificate_value",
                    "x509_details": {
                        "issuer": "issuer_value",
                        "subject": "subject_value",
                        "start_time": {"seconds": 751, "nanos": 543},
                        "expiry_time": {},
                        "signature_algorithm": "signature_algorithm_value",
                        "public_key_type": "public_key_type_value",
                    },
                }
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.DeviceRegistry(
            id="id_value",
            name="name_value",
            log_level=resources.LogLevel.NONE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.DeviceRegistry.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_device_registry(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceRegistry)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.log_level == resources.LogLevel.NONE


def test_update_device_registry_rest_required_fields(
    request_type=device_manager.UpdateDeviceRegistryRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_device_registry._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_device_registry._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.DeviceRegistry()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = resources.DeviceRegistry.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_device_registry(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_device_registry_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_device_registry._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "deviceRegistry",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_device_registry_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_update_device_registry"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_update_device_registry"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.UpdateDeviceRegistryRequest.pb(
            device_manager.UpdateDeviceRegistryRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.DeviceRegistry.to_json(
            resources.DeviceRegistry()
        )

        request = device_manager.UpdateDeviceRegistryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.DeviceRegistry()

        client.update_device_registry(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_device_registry_rest_bad_request(
    transport: str = "rest", request_type=device_manager.UpdateDeviceRegistryRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "device_registry": {
            "name": "projects/sample1/locations/sample2/registries/sample3"
        }
    }
    request_init["device_registry"] = {
        "id": "id_value",
        "name": "projects/sample1/locations/sample2/registries/sample3",
        "event_notification_configs": [
            {
                "subfolder_matches": "subfolder_matches_value",
                "pubsub_topic_name": "pubsub_topic_name_value",
            }
        ],
        "state_notification_config": {"pubsub_topic_name": "pubsub_topic_name_value"},
        "mqtt_config": {"mqtt_enabled_state": 1},
        "http_config": {"http_enabled_state": 1},
        "log_level": 10,
        "credentials": [
            {
                "public_key_certificate": {
                    "format": 1,
                    "certificate": "certificate_value",
                    "x509_details": {
                        "issuer": "issuer_value",
                        "subject": "subject_value",
                        "start_time": {"seconds": 751, "nanos": 543},
                        "expiry_time": {},
                        "signature_algorithm": "signature_algorithm_value",
                        "public_key_type": "public_key_type_value",
                    },
                }
            }
        ],
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_device_registry(request)


def test_update_device_registry_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.DeviceRegistry()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "device_registry": {
                "name": "projects/sample1/locations/sample2/registries/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            device_registry=resources.DeviceRegistry(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.DeviceRegistry.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_device_registry(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{device_registry.name=projects/*/locations/*/registries/*}"
            % client.transport._host,
            args[1],
        )


def test_update_device_registry_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_device_registry(
            device_manager.UpdateDeviceRegistryRequest(),
            device_registry=resources.DeviceRegistry(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_device_registry_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.DeleteDeviceRegistryRequest,
        dict,
    ],
)
def test_delete_device_registry_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_device_registry(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_device_registry_rest_required_fields(
    request_type=device_manager.DeleteDeviceRegistryRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_device_registry._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_device_registry._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_device_registry(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_device_registry_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_device_registry._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_device_registry_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_delete_device_registry"
    ) as pre:
        pre.assert_not_called()
        pb_message = device_manager.DeleteDeviceRegistryRequest.pb(
            device_manager.DeleteDeviceRegistryRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = device_manager.DeleteDeviceRegistryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_device_registry(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_device_registry_rest_bad_request(
    transport: str = "rest", request_type=device_manager.DeleteDeviceRegistryRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_device_registry(request)


def test_delete_device_registry_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/registries/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_device_registry(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/registries/*}" % client.transport._host,
            args[1],
        )


def test_delete_device_registry_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_device_registry(
            device_manager.DeleteDeviceRegistryRequest(),
            name="name_value",
        )


def test_delete_device_registry_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.ListDeviceRegistriesRequest,
        dict,
    ],
)
def test_list_device_registries_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.ListDeviceRegistriesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.ListDeviceRegistriesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_device_registries(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeviceRegistriesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_device_registries_rest_required_fields(
    request_type=device_manager.ListDeviceRegistriesRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_device_registries._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_device_registries._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = device_manager.ListDeviceRegistriesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = device_manager.ListDeviceRegistriesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_device_registries(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_device_registries_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_device_registries._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_device_registries_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_list_device_registries"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_list_device_registries"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.ListDeviceRegistriesRequest.pb(
            device_manager.ListDeviceRegistriesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = device_manager.ListDeviceRegistriesResponse.to_json(
            device_manager.ListDeviceRegistriesResponse()
        )

        request = device_manager.ListDeviceRegistriesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = device_manager.ListDeviceRegistriesResponse()

        client.list_device_registries(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_device_registries_rest_bad_request(
    transport: str = "rest", request_type=device_manager.ListDeviceRegistriesRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_device_registries(request)


def test_list_device_registries_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.ListDeviceRegistriesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.ListDeviceRegistriesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_device_registries(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/registries" % client.transport._host,
            args[1],
        )


def test_list_device_registries_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_device_registries(
            device_manager.ListDeviceRegistriesRequest(),
            parent="parent_value",
        )


def test_list_device_registries_rest_pager(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                ],
                next_page_token="abc",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[],
                next_page_token="def",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                ],
                next_page_token="ghi",
            ),
            device_manager.ListDeviceRegistriesResponse(
                device_registries=[
                    resources.DeviceRegistry(),
                    resources.DeviceRegistry(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            device_manager.ListDeviceRegistriesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_device_registries(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.DeviceRegistry) for i in results)

        pages = list(client.list_device_registries(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.CreateDeviceRequest,
        dict,
    ],
)
def test_create_device_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/registries/sample3"}
    request_init["device"] = {
        "id": "id_value",
        "name": "name_value",
        "num_id": 636,
        "credentials": [
            {
                "public_key": {"format": 3, "key": "key_value"},
                "expiration_time": {"seconds": 751, "nanos": 543},
            }
        ],
        "last_heartbeat_time": {},
        "last_event_time": {},
        "last_state_time": {},
        "last_config_ack_time": {},
        "last_config_send_time": {},
        "blocked": True,
        "last_error_time": {},
        "last_error_status": {
            "code": 411,
            "message": "message_value",
            "details": [
                {
                    "type_url": "type.googleapis.com/google.protobuf.Duration",
                    "value": b"\x08\x0c\x10\xdb\x07",
                }
            ],
        },
        "config": {
            "version": 774,
            "cloud_update_time": {},
            "device_ack_time": {},
            "binary_data": b"binary_data_blob",
        },
        "state": {"update_time": {}, "binary_data": b"binary_data_blob"},
        "log_level": 10,
        "metadata": {},
        "gateway_config": {
            "gateway_type": 1,
            "gateway_auth_method": 1,
            "last_accessed_gateway_id": "last_accessed_gateway_id_value",
            "last_accessed_gateway_time": {},
        },
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.Device(
            id="id_value",
            name="name_value",
            num_id=636,
            blocked=True,
            log_level=resources.LogLevel.NONE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.Device.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_device(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Device)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.num_id == 636
    assert response.blocked is True
    assert response.log_level == resources.LogLevel.NONE


def test_create_device_rest_required_fields(
    request_type=device_manager.CreateDeviceRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_device._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_device._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.Device()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = resources.Device.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_device(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_device_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_device._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "device",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_device_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_create_device"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_create_device"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.CreateDeviceRequest.pb(
            device_manager.CreateDeviceRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.Device.to_json(resources.Device())

        request = device_manager.CreateDeviceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.Device()

        client.create_device(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_device_rest_bad_request(
    transport: str = "rest", request_type=device_manager.CreateDeviceRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/registries/sample3"}
    request_init["device"] = {
        "id": "id_value",
        "name": "name_value",
        "num_id": 636,
        "credentials": [
            {
                "public_key": {"format": 3, "key": "key_value"},
                "expiration_time": {"seconds": 751, "nanos": 543},
            }
        ],
        "last_heartbeat_time": {},
        "last_event_time": {},
        "last_state_time": {},
        "last_config_ack_time": {},
        "last_config_send_time": {},
        "blocked": True,
        "last_error_time": {},
        "last_error_status": {
            "code": 411,
            "message": "message_value",
            "details": [
                {
                    "type_url": "type.googleapis.com/google.protobuf.Duration",
                    "value": b"\x08\x0c\x10\xdb\x07",
                }
            ],
        },
        "config": {
            "version": 774,
            "cloud_update_time": {},
            "device_ack_time": {},
            "binary_data": b"binary_data_blob",
        },
        "state": {"update_time": {}, "binary_data": b"binary_data_blob"},
        "log_level": 10,
        "metadata": {},
        "gateway_config": {
            "gateway_type": 1,
            "gateway_auth_method": 1,
            "last_accessed_gateway_id": "last_accessed_gateway_id_value",
            "last_accessed_gateway_time": {},
        },
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_device(request)


def test_create_device_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.Device()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/registries/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            device=resources.Device(id="id_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.Device.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_device(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/registries/*}/devices"
            % client.transport._host,
            args[1],
        )


def test_create_device_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_device(
            device_manager.CreateDeviceRequest(),
            parent="parent_value",
            device=resources.Device(id="id_value"),
        )


def test_create_device_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.GetDeviceRequest,
        dict,
    ],
)
def test_get_device_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.Device(
            id="id_value",
            name="name_value",
            num_id=636,
            blocked=True,
            log_level=resources.LogLevel.NONE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.Device.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_device(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Device)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.num_id == 636
    assert response.blocked is True
    assert response.log_level == resources.LogLevel.NONE


def test_get_device_rest_required_fields(request_type=device_manager.GetDeviceRequest):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_device._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_device._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("field_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.Device()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = resources.Device.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_device(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_device_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_device._get_unset_required_fields({})
    assert set(unset_fields) == (set(("fieldMask",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_device_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_get_device"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_get_device"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.GetDeviceRequest.pb(
            device_manager.GetDeviceRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.Device.to_json(resources.Device())

        request = device_manager.GetDeviceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.Device()

        client.get_device(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_device_rest_bad_request(
    transport: str = "rest", request_type=device_manager.GetDeviceRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_device(request)


def test_get_device_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.Device()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.Device.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_device(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/registries/*/devices/*}"
            % client.transport._host,
            args[1],
        )


def test_get_device_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_device(
            device_manager.GetDeviceRequest(),
            name="name_value",
        )


def test_get_device_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.UpdateDeviceRequest,
        dict,
    ],
)
def test_update_device_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "device": {
            "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
        }
    }
    request_init["device"] = {
        "id": "id_value",
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4",
        "num_id": 636,
        "credentials": [
            {
                "public_key": {"format": 3, "key": "key_value"},
                "expiration_time": {"seconds": 751, "nanos": 543},
            }
        ],
        "last_heartbeat_time": {},
        "last_event_time": {},
        "last_state_time": {},
        "last_config_ack_time": {},
        "last_config_send_time": {},
        "blocked": True,
        "last_error_time": {},
        "last_error_status": {
            "code": 411,
            "message": "message_value",
            "details": [
                {
                    "type_url": "type.googleapis.com/google.protobuf.Duration",
                    "value": b"\x08\x0c\x10\xdb\x07",
                }
            ],
        },
        "config": {
            "version": 774,
            "cloud_update_time": {},
            "device_ack_time": {},
            "binary_data": b"binary_data_blob",
        },
        "state": {"update_time": {}, "binary_data": b"binary_data_blob"},
        "log_level": 10,
        "metadata": {},
        "gateway_config": {
            "gateway_type": 1,
            "gateway_auth_method": 1,
            "last_accessed_gateway_id": "last_accessed_gateway_id_value",
            "last_accessed_gateway_time": {},
        },
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.Device(
            id="id_value",
            name="name_value",
            num_id=636,
            blocked=True,
            log_level=resources.LogLevel.NONE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.Device.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_device(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Device)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.num_id == 636
    assert response.blocked is True
    assert response.log_level == resources.LogLevel.NONE


def test_update_device_rest_required_fields(
    request_type=device_manager.UpdateDeviceRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_device._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_device._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.Device()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = resources.Device.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_device(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_device_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_device._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "device",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_device_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_update_device"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_update_device"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.UpdateDeviceRequest.pb(
            device_manager.UpdateDeviceRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.Device.to_json(resources.Device())

        request = device_manager.UpdateDeviceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.Device()

        client.update_device(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_device_rest_bad_request(
    transport: str = "rest", request_type=device_manager.UpdateDeviceRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "device": {
            "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
        }
    }
    request_init["device"] = {
        "id": "id_value",
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4",
        "num_id": 636,
        "credentials": [
            {
                "public_key": {"format": 3, "key": "key_value"},
                "expiration_time": {"seconds": 751, "nanos": 543},
            }
        ],
        "last_heartbeat_time": {},
        "last_event_time": {},
        "last_state_time": {},
        "last_config_ack_time": {},
        "last_config_send_time": {},
        "blocked": True,
        "last_error_time": {},
        "last_error_status": {
            "code": 411,
            "message": "message_value",
            "details": [
                {
                    "type_url": "type.googleapis.com/google.protobuf.Duration",
                    "value": b"\x08\x0c\x10\xdb\x07",
                }
            ],
        },
        "config": {
            "version": 774,
            "cloud_update_time": {},
            "device_ack_time": {},
            "binary_data": b"binary_data_blob",
        },
        "state": {"update_time": {}, "binary_data": b"binary_data_blob"},
        "log_level": 10,
        "metadata": {},
        "gateway_config": {
            "gateway_type": 1,
            "gateway_auth_method": 1,
            "last_accessed_gateway_id": "last_accessed_gateway_id_value",
            "last_accessed_gateway_time": {},
        },
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_device(request)


def test_update_device_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.Device()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "device": {
                "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            device=resources.Device(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.Device.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_device(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{device.name=projects/*/locations/*/registries/*/devices/*}"
            % client.transport._host,
            args[1],
        )


def test_update_device_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_device(
            device_manager.UpdateDeviceRequest(),
            device=resources.Device(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_device_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.DeleteDeviceRequest,
        dict,
    ],
)
def test_delete_device_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_device(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_device_rest_required_fields(
    request_type=device_manager.DeleteDeviceRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_device._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_device._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_device(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_device_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_device._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_device_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_delete_device"
    ) as pre:
        pre.assert_not_called()
        pb_message = device_manager.DeleteDeviceRequest.pb(
            device_manager.DeleteDeviceRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = device_manager.DeleteDeviceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_device(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_device_rest_bad_request(
    transport: str = "rest", request_type=device_manager.DeleteDeviceRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_device(request)


def test_delete_device_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_device(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/registries/*/devices/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_device_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_device(
            device_manager.DeleteDeviceRequest(),
            name="name_value",
        )


def test_delete_device_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.ListDevicesRequest,
        dict,
    ],
)
def test_list_devices_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.ListDevicesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.ListDevicesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_devices(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDevicesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_devices_rest_required_fields(
    request_type=device_manager.ListDevicesRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_devices._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_devices._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "device_ids",
            "device_num_ids",
            "field_mask",
            "gateway_list_options",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = device_manager.ListDevicesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = device_manager.ListDevicesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_devices(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_devices_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_devices._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "deviceIds",
                "deviceNumIds",
                "fieldMask",
                "gatewayListOptions",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_devices_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_list_devices"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_list_devices"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.ListDevicesRequest.pb(
            device_manager.ListDevicesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = device_manager.ListDevicesResponse.to_json(
            device_manager.ListDevicesResponse()
        )

        request = device_manager.ListDevicesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = device_manager.ListDevicesResponse()

        client.list_devices(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_devices_rest_bad_request(
    transport: str = "rest", request_type=device_manager.ListDevicesRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_devices(request)


def test_list_devices_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.ListDevicesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/registries/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.ListDevicesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_devices(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/registries/*}/devices"
            % client.transport._host,
            args[1],
        )


def test_list_devices_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_devices(
            device_manager.ListDevicesRequest(),
            parent="parent_value",
        )


def test_list_devices_rest_pager(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                    resources.Device(),
                    resources.Device(),
                ],
                next_page_token="abc",
            ),
            device_manager.ListDevicesResponse(
                devices=[],
                next_page_token="def",
            ),
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                ],
                next_page_token="ghi",
            ),
            device_manager.ListDevicesResponse(
                devices=[
                    resources.Device(),
                    resources.Device(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            device_manager.ListDevicesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/registries/sample3"
        }

        pager = client.list_devices(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Device) for i in results)

        pages = list(client.list_devices(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.ModifyCloudToDeviceConfigRequest,
        dict,
    ],
)
def test_modify_cloud_to_device_config_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.DeviceConfig(
            version=774,
            binary_data=b"binary_data_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.DeviceConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.modify_cloud_to_device_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.DeviceConfig)
    assert response.version == 774
    assert response.binary_data == b"binary_data_blob"


def test_modify_cloud_to_device_config_rest_required_fields(
    request_type=device_manager.ModifyCloudToDeviceConfigRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["binary_data"] = b""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).modify_cloud_to_device_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["binaryData"] = b"binary_data_blob"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).modify_cloud_to_device_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "binaryData" in jsonified_request
    assert jsonified_request["binaryData"] == b"binary_data_blob"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.DeviceConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = resources.DeviceConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.modify_cloud_to_device_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_modify_cloud_to_device_config_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.modify_cloud_to_device_config._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "binaryData",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_modify_cloud_to_device_config_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_modify_cloud_to_device_config"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_modify_cloud_to_device_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.ModifyCloudToDeviceConfigRequest.pb(
            device_manager.ModifyCloudToDeviceConfigRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.DeviceConfig.to_json(
            resources.DeviceConfig()
        )

        request = device_manager.ModifyCloudToDeviceConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.DeviceConfig()

        client.modify_cloud_to_device_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_modify_cloud_to_device_config_rest_bad_request(
    transport: str = "rest",
    request_type=device_manager.ModifyCloudToDeviceConfigRequest,
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.modify_cloud_to_device_config(request)


def test_modify_cloud_to_device_config_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.DeviceConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            binary_data=b"binary_data_blob",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = resources.DeviceConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.modify_cloud_to_device_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/registries/*/devices/*}:modifyCloudToDeviceConfig"
            % client.transport._host,
            args[1],
        )


def test_modify_cloud_to_device_config_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.modify_cloud_to_device_config(
            device_manager.ModifyCloudToDeviceConfigRequest(),
            name="name_value",
            binary_data=b"binary_data_blob",
        )


def test_modify_cloud_to_device_config_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.ListDeviceConfigVersionsRequest,
        dict,
    ],
)
def test_list_device_config_versions_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.ListDeviceConfigVersionsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.ListDeviceConfigVersionsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_device_config_versions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.ListDeviceConfigVersionsResponse)


def test_list_device_config_versions_rest_required_fields(
    request_type=device_manager.ListDeviceConfigVersionsRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_device_config_versions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_device_config_versions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("num_versions",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = device_manager.ListDeviceConfigVersionsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = device_manager.ListDeviceConfigVersionsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_device_config_versions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_device_config_versions_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_device_config_versions._get_unset_required_fields({})
    assert set(unset_fields) == (set(("numVersions",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_device_config_versions_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_list_device_config_versions"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_list_device_config_versions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.ListDeviceConfigVersionsRequest.pb(
            device_manager.ListDeviceConfigVersionsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            device_manager.ListDeviceConfigVersionsResponse.to_json(
                device_manager.ListDeviceConfigVersionsResponse()
            )
        )

        request = device_manager.ListDeviceConfigVersionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = device_manager.ListDeviceConfigVersionsResponse()

        client.list_device_config_versions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_device_config_versions_rest_bad_request(
    transport: str = "rest", request_type=device_manager.ListDeviceConfigVersionsRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_device_config_versions(request)


def test_list_device_config_versions_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.ListDeviceConfigVersionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.ListDeviceConfigVersionsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_device_config_versions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/registries/*/devices/*}/configVersions"
            % client.transport._host,
            args[1],
        )


def test_list_device_config_versions_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_device_config_versions(
            device_manager.ListDeviceConfigVersionsRequest(),
            name="name_value",
        )


def test_list_device_config_versions_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.ListDeviceStatesRequest,
        dict,
    ],
)
def test_list_device_states_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.ListDeviceStatesResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.ListDeviceStatesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_device_states(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.ListDeviceStatesResponse)


def test_list_device_states_rest_required_fields(
    request_type=device_manager.ListDeviceStatesRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_device_states._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_device_states._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("num_states",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = device_manager.ListDeviceStatesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = device_manager.ListDeviceStatesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_device_states(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_device_states_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_device_states._get_unset_required_fields({})
    assert set(unset_fields) == (set(("numStates",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_device_states_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_list_device_states"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_list_device_states"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.ListDeviceStatesRequest.pb(
            device_manager.ListDeviceStatesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = device_manager.ListDeviceStatesResponse.to_json(
            device_manager.ListDeviceStatesResponse()
        )

        request = device_manager.ListDeviceStatesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = device_manager.ListDeviceStatesResponse()

        client.list_device_states(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_device_states_rest_bad_request(
    transport: str = "rest", request_type=device_manager.ListDeviceStatesRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_device_states(request)


def test_list_device_states_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.ListDeviceStatesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.ListDeviceStatesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_device_states(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/registries/*/devices/*}/states"
            % client.transport._host,
            args[1],
        )


def test_list_device_states_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_device_states(
            device_manager.ListDeviceStatesRequest(),
            name="name_value",
        )


def test_list_device_states_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.SetIamPolicyRequest,
        dict,
    ],
)
def test_set_iam_policy_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = return_value
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_set_iam_policy_rest_required_fields(
    request_type=iam_policy_pb2.SetIamPolicyRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["resource"] = ""
    request = request_type(**request_init)
    pb_request = request
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_iam_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["resource"] = "resource_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_iam_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "resource" in jsonified_request
    assert jsonified_request["resource"] == "resource_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = policy_pb2.Policy()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = return_value
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.set_iam_policy(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_set_iam_policy_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.set_iam_policy._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "resource",
                "policy",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_set_iam_policy_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_set_iam_policy"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_set_iam_policy"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = iam_policy_pb2.SetIamPolicyRequest()
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(policy_pb2.Policy())

        request = iam_policy_pb2.SetIamPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = policy_pb2.Policy()

        client.set_iam_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_set_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.SetIamPolicyRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_iam_policy(request)


def test_set_iam_policy_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "resource": "projects/sample1/locations/sample2/registries/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            resource="resource_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = return_value
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.set_iam_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{resource=projects/*/locations/*/registries/*}:setIamPolicy"
            % client.transport._host,
            args[1],
        )


def test_set_iam_policy_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_iam_policy(
            iam_policy_pb2.SetIamPolicyRequest(),
            resource="resource_value",
        )


def test_set_iam_policy_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = return_value
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_get_iam_policy_rest_required_fields(
    request_type=iam_policy_pb2.GetIamPolicyRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["resource"] = ""
    request = request_type(**request_init)
    pb_request = request
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_iam_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["resource"] = "resource_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_iam_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "resource" in jsonified_request
    assert jsonified_request["resource"] == "resource_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = policy_pb2.Policy()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = return_value
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_iam_policy(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_iam_policy_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_iam_policy._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("resource",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_iam_policy_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_get_iam_policy"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_get_iam_policy"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = iam_policy_pb2.GetIamPolicyRequest()
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(policy_pb2.Policy())

        request = iam_policy_pb2.GetIamPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = policy_pb2.Policy()

        client.get_iam_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.GetIamPolicyRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_iam_policy(request)


def test_get_iam_policy_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "resource": "projects/sample1/locations/sample2/registries/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            resource="resource_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = return_value
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_iam_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{resource=projects/*/locations/*/registries/*}:getIamPolicy"
            % client.transport._host,
            args[1],
        )


def test_get_iam_policy_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_iam_policy(
            iam_policy_pb2.GetIamPolicyRequest(),
            resource="resource_value",
        )


def test_get_iam_policy_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.TestIamPermissionsRequest,
        dict,
    ],
)
def test_test_iam_permissions_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = iam_policy_pb2.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = return_value
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.test_iam_permissions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_rest_required_fields(
    request_type=iam_policy_pb2.TestIamPermissionsRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["resource"] = ""
    request_init["permissions"] = ""
    request = request_type(**request_init)
    pb_request = request
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).test_iam_permissions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["resource"] = "resource_value"
    jsonified_request["permissions"] = "permissions_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).test_iam_permissions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "resource" in jsonified_request
    assert jsonified_request["resource"] == "resource_value"
    assert "permissions" in jsonified_request
    assert jsonified_request["permissions"] == "permissions_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = iam_policy_pb2.TestIamPermissionsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = return_value
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.test_iam_permissions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_test_iam_permissions_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.test_iam_permissions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "resource",
                "permissions",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_test_iam_permissions_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_test_iam_permissions"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_test_iam_permissions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = iam_policy_pb2.TestIamPermissionsRequest()
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        request = iam_policy_pb2.TestIamPermissionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        client.test_iam_permissions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_test_iam_permissions_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.TestIamPermissionsRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.test_iam_permissions(request)


def test_test_iam_permissions_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = iam_policy_pb2.TestIamPermissionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "resource": "projects/sample1/locations/sample2/registries/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            resource="resource_value",
            permissions=["permissions_value"],
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = return_value
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.test_iam_permissions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{resource=projects/*/locations/*/registries/*}:testIamPermissions"
            % client.transport._host,
            args[1],
        )


def test_test_iam_permissions_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.test_iam_permissions(
            iam_policy_pb2.TestIamPermissionsRequest(),
            resource="resource_value",
            permissions=["permissions_value"],
        )


def test_test_iam_permissions_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.SendCommandToDeviceRequest,
        dict,
    ],
)
def test_send_command_to_device_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.SendCommandToDeviceResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.SendCommandToDeviceResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.send_command_to_device(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.SendCommandToDeviceResponse)


def test_send_command_to_device_rest_required_fields(
    request_type=device_manager.SendCommandToDeviceRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["binary_data"] = b""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).send_command_to_device._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["binaryData"] = b"binary_data_blob"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).send_command_to_device._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "binaryData" in jsonified_request
    assert jsonified_request["binaryData"] == b"binary_data_blob"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = device_manager.SendCommandToDeviceResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = device_manager.SendCommandToDeviceResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.send_command_to_device(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_send_command_to_device_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.send_command_to_device._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "binaryData",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_send_command_to_device_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_send_command_to_device"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_send_command_to_device"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.SendCommandToDeviceRequest.pb(
            device_manager.SendCommandToDeviceRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = device_manager.SendCommandToDeviceResponse.to_json(
            device_manager.SendCommandToDeviceResponse()
        )

        request = device_manager.SendCommandToDeviceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = device_manager.SendCommandToDeviceResponse()

        client.send_command_to_device(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_send_command_to_device_rest_bad_request(
    transport: str = "rest", request_type=device_manager.SendCommandToDeviceRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.send_command_to_device(request)


def test_send_command_to_device_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.SendCommandToDeviceResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/registries/sample3/devices/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            binary_data=b"binary_data_blob",
            subfolder="subfolder_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.SendCommandToDeviceResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.send_command_to_device(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/registries/*/devices/*}:sendCommandToDevice"
            % client.transport._host,
            args[1],
        )


def test_send_command_to_device_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.send_command_to_device(
            device_manager.SendCommandToDeviceRequest(),
            name="name_value",
            binary_data=b"binary_data_blob",
            subfolder="subfolder_value",
        )


def test_send_command_to_device_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.BindDeviceToGatewayRequest,
        dict,
    ],
)
def test_bind_device_to_gateway_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.BindDeviceToGatewayResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.BindDeviceToGatewayResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.bind_device_to_gateway(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.BindDeviceToGatewayResponse)


def test_bind_device_to_gateway_rest_required_fields(
    request_type=device_manager.BindDeviceToGatewayRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["gateway_id"] = ""
    request_init["device_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).bind_device_to_gateway._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"
    jsonified_request["gatewayId"] = "gateway_id_value"
    jsonified_request["deviceId"] = "device_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).bind_device_to_gateway._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "gatewayId" in jsonified_request
    assert jsonified_request["gatewayId"] == "gateway_id_value"
    assert "deviceId" in jsonified_request
    assert jsonified_request["deviceId"] == "device_id_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = device_manager.BindDeviceToGatewayResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = device_manager.BindDeviceToGatewayResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.bind_device_to_gateway(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_bind_device_to_gateway_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.bind_device_to_gateway._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "gatewayId",
                "deviceId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_bind_device_to_gateway_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_bind_device_to_gateway"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_bind_device_to_gateway"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.BindDeviceToGatewayRequest.pb(
            device_manager.BindDeviceToGatewayRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = device_manager.BindDeviceToGatewayResponse.to_json(
            device_manager.BindDeviceToGatewayResponse()
        )

        request = device_manager.BindDeviceToGatewayRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = device_manager.BindDeviceToGatewayResponse()

        client.bind_device_to_gateway(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_bind_device_to_gateway_rest_bad_request(
    transport: str = "rest", request_type=device_manager.BindDeviceToGatewayRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.bind_device_to_gateway(request)


def test_bind_device_to_gateway_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.BindDeviceToGatewayResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/registries/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.BindDeviceToGatewayResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.bind_device_to_gateway(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/registries/*}:bindDeviceToGateway"
            % client.transport._host,
            args[1],
        )


def test_bind_device_to_gateway_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.bind_device_to_gateway(
            device_manager.BindDeviceToGatewayRequest(),
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )


def test_bind_device_to_gateway_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        device_manager.UnbindDeviceFromGatewayRequest,
        dict,
    ],
)
def test_unbind_device_from_gateway_rest(request_type):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.UnbindDeviceFromGatewayResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.UnbindDeviceFromGatewayResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.unbind_device_from_gateway(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, device_manager.UnbindDeviceFromGatewayResponse)


def test_unbind_device_from_gateway_rest_required_fields(
    request_type=device_manager.UnbindDeviceFromGatewayRequest,
):
    transport_class = transports.DeviceManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["gateway_id"] = ""
    request_init["device_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).unbind_device_from_gateway._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"
    jsonified_request["gatewayId"] = "gateway_id_value"
    jsonified_request["deviceId"] = "device_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).unbind_device_from_gateway._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "gatewayId" in jsonified_request
    assert jsonified_request["gatewayId"] == "gateway_id_value"
    assert "deviceId" in jsonified_request
    assert jsonified_request["deviceId"] == "device_id_value"

    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = device_manager.UnbindDeviceFromGatewayResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = device_manager.UnbindDeviceFromGatewayResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.unbind_device_from_gateway(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_unbind_device_from_gateway_rest_unset_required_fields():
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.unbind_device_from_gateway._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "gatewayId",
                "deviceId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_unbind_device_from_gateway_rest_interceptors(null_interceptor):
    transport = transports.DeviceManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DeviceManagerRestInterceptor(),
    )
    client = DeviceManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "post_unbind_device_from_gateway"
    ) as post, mock.patch.object(
        transports.DeviceManagerRestInterceptor, "pre_unbind_device_from_gateway"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = device_manager.UnbindDeviceFromGatewayRequest.pb(
            device_manager.UnbindDeviceFromGatewayRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            device_manager.UnbindDeviceFromGatewayResponse.to_json(
                device_manager.UnbindDeviceFromGatewayResponse()
            )
        )

        request = device_manager.UnbindDeviceFromGatewayRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = device_manager.UnbindDeviceFromGatewayResponse()

        client.unbind_device_from_gateway(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_unbind_device_from_gateway_rest_bad_request(
    transport: str = "rest", request_type=device_manager.UnbindDeviceFromGatewayRequest
):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/registries/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.unbind_device_from_gateway(request)


def test_unbind_device_from_gateway_rest_flattened():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = device_manager.UnbindDeviceFromGatewayResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/registries/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = device_manager.UnbindDeviceFromGatewayResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.unbind_device_from_gateway(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/registries/*}:unbindDeviceFromGateway"
            % client.transport._host,
            args[1],
        )


def test_unbind_device_from_gateway_rest_flattened_error(transport: str = "rest"):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.unbind_device_from_gateway(
            device_manager.UnbindDeviceFromGatewayRequest(),
            parent="parent_value",
            gateway_id="gateway_id_value",
            device_id="device_id_value",
        )


def test_unbind_device_from_gateway_rest_error():
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DeviceManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DeviceManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DeviceManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DeviceManagerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.DeviceManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DeviceManagerClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DeviceManagerClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DeviceManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DeviceManagerClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DeviceManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = DeviceManagerClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DeviceManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DeviceManagerGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DeviceManagerGrpcTransport,
        transports.DeviceManagerGrpcAsyncIOTransport,
        transports.DeviceManagerRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = DeviceManagerClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.DeviceManagerGrpcTransport,
    )


def test_device_manager_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.DeviceManagerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_device_manager_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.iot_v1.services.device_manager.transports.DeviceManagerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DeviceManagerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
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

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_device_manager_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.iot_v1.services.device_manager.transports.DeviceManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DeviceManagerTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudiot",
            ),
            quota_project_id="octopus",
        )


def test_device_manager_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.iot_v1.services.device_manager.transports.DeviceManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DeviceManagerTransport()
        adc.assert_called_once()


def test_device_manager_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DeviceManagerClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudiot",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DeviceManagerGrpcTransport,
        transports.DeviceManagerGrpcAsyncIOTransport,
    ],
)
def test_device_manager_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudiot",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DeviceManagerGrpcTransport,
        transports.DeviceManagerGrpcAsyncIOTransport,
        transports.DeviceManagerRestTransport,
    ],
)
def test_device_manager_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.DeviceManagerGrpcTransport, grpc_helpers),
        (transports.DeviceManagerGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_device_manager_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "cloudiot.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloudiot",
            ),
            scopes=["1", "2"],
            default_host="cloudiot.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DeviceManagerGrpcTransport,
        transports.DeviceManagerGrpcAsyncIOTransport,
    ],
)
def test_device_manager_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_device_manager_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.DeviceManagerRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_device_manager_host_no_port(transport_name):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudiot.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudiot.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudiot.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_device_manager_host_with_port(transport_name):
    client = DeviceManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudiot.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudiot.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudiot.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_device_manager_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = DeviceManagerClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = DeviceManagerClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_device_registry._session
    session2 = client2.transport.create_device_registry._session
    assert session1 != session2
    session1 = client1.transport.get_device_registry._session
    session2 = client2.transport.get_device_registry._session
    assert session1 != session2
    session1 = client1.transport.update_device_registry._session
    session2 = client2.transport.update_device_registry._session
    assert session1 != session2
    session1 = client1.transport.delete_device_registry._session
    session2 = client2.transport.delete_device_registry._session
    assert session1 != session2
    session1 = client1.transport.list_device_registries._session
    session2 = client2.transport.list_device_registries._session
    assert session1 != session2
    session1 = client1.transport.create_device._session
    session2 = client2.transport.create_device._session
    assert session1 != session2
    session1 = client1.transport.get_device._session
    session2 = client2.transport.get_device._session
    assert session1 != session2
    session1 = client1.transport.update_device._session
    session2 = client2.transport.update_device._session
    assert session1 != session2
    session1 = client1.transport.delete_device._session
    session2 = client2.transport.delete_device._session
    assert session1 != session2
    session1 = client1.transport.list_devices._session
    session2 = client2.transport.list_devices._session
    assert session1 != session2
    session1 = client1.transport.modify_cloud_to_device_config._session
    session2 = client2.transport.modify_cloud_to_device_config._session
    assert session1 != session2
    session1 = client1.transport.list_device_config_versions._session
    session2 = client2.transport.list_device_config_versions._session
    assert session1 != session2
    session1 = client1.transport.list_device_states._session
    session2 = client2.transport.list_device_states._session
    assert session1 != session2
    session1 = client1.transport.set_iam_policy._session
    session2 = client2.transport.set_iam_policy._session
    assert session1 != session2
    session1 = client1.transport.get_iam_policy._session
    session2 = client2.transport.get_iam_policy._session
    assert session1 != session2
    session1 = client1.transport.test_iam_permissions._session
    session2 = client2.transport.test_iam_permissions._session
    assert session1 != session2
    session1 = client1.transport.send_command_to_device._session
    session2 = client2.transport.send_command_to_device._session
    assert session1 != session2
    session1 = client1.transport.bind_device_to_gateway._session
    session2 = client2.transport.bind_device_to_gateway._session
    assert session1 != session2
    session1 = client1.transport.unbind_device_from_gateway._session
    session2 = client2.transport.unbind_device_from_gateway._session
    assert session1 != session2


def test_device_manager_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DeviceManagerGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_device_manager_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DeviceManagerGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DeviceManagerGrpcTransport,
        transports.DeviceManagerGrpcAsyncIOTransport,
    ],
)
def test_device_manager_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DeviceManagerGrpcTransport,
        transports.DeviceManagerGrpcAsyncIOTransport,
    ],
)
def test_device_manager_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_device_path():
    project = "squid"
    location = "clam"
    registry = "whelk"
    device = "octopus"
    expected = "projects/{project}/locations/{location}/registries/{registry}/devices/{device}".format(
        project=project,
        location=location,
        registry=registry,
        device=device,
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


def test_registry_path():
    project = "winkle"
    location = "nautilus"
    registry = "scallop"
    expected = "projects/{project}/locations/{location}/registries/{registry}".format(
        project=project,
        location=location,
        registry=registry,
    )
    actual = DeviceManagerClient.registry_path(project, location, registry)
    assert expected == actual


def test_parse_registry_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "registry": "clam",
    }
    path = DeviceManagerClient.registry_path(**expected)

    # Check that the path construction is reversible.
    actual = DeviceManagerClient.parse_registry_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = DeviceManagerClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = DeviceManagerClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DeviceManagerClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = DeviceManagerClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = DeviceManagerClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DeviceManagerClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = DeviceManagerClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = DeviceManagerClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DeviceManagerClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = DeviceManagerClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = DeviceManagerClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DeviceManagerClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = DeviceManagerClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = DeviceManagerClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DeviceManagerClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DeviceManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DeviceManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DeviceManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DeviceManagerClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = DeviceManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = DeviceManagerClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = DeviceManagerClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (DeviceManagerClient, transports.DeviceManagerGrpcTransport),
        (DeviceManagerAsyncClient, transports.DeviceManagerGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
