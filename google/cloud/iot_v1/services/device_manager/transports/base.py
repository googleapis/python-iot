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
import abc
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union
import pkg_resources

import google.auth  # type: ignore
import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.iot_v1.types import device_manager
from google.cloud.iot_v1.types import resources
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-iot",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class DeviceManagerTransport(abc.ABC):
    """Abstract transport class for DeviceManager."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloudiot",
    )

    DEFAULT_HOST: str = "cloudiot.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        **kwargs,
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
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        scopes_kwargs = {"scopes": scopes, "default_scopes": self.AUTH_SCOPES}

        # Save the scopes.
        self._scopes = scopes

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )
        elif credentials is None:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )

        # If the credentials are service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_device_registry: gapic_v1.method.wrap_method(
                self.create_device_registry,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.get_device_registry: gapic_v1.method.wrap_method(
                self.get_device_registry,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.update_device_registry: gapic_v1.method.wrap_method(
                self.update_device_registry,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.delete_device_registry: gapic_v1.method.wrap_method(
                self.delete_device_registry,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.list_device_registries: gapic_v1.method.wrap_method(
                self.list_device_registries,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.create_device: gapic_v1.method.wrap_method(
                self.create_device, default_timeout=120.0, client_info=client_info,
            ),
            self.get_device: gapic_v1.method.wrap_method(
                self.get_device,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.update_device: gapic_v1.method.wrap_method(
                self.update_device, default_timeout=120.0, client_info=client_info,
            ),
            self.delete_device: gapic_v1.method.wrap_method(
                self.delete_device,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.list_devices: gapic_v1.method.wrap_method(
                self.list_devices,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.modify_cloud_to_device_config: gapic_v1.method.wrap_method(
                self.modify_cloud_to_device_config,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.list_device_config_versions: gapic_v1.method.wrap_method(
                self.list_device_config_versions,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.list_device_states: gapic_v1.method.wrap_method(
                self.list_device_states,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy, default_timeout=120.0, client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy, default_timeout=120.0, client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.send_command_to_device: gapic_v1.method.wrap_method(
                self.send_command_to_device,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=120.0,
                ),
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.bind_device_to_gateway: gapic_v1.method.wrap_method(
                self.bind_device_to_gateway,
                default_timeout=120.0,
                client_info=client_info,
            ),
            self.unbind_device_from_gateway: gapic_v1.method.wrap_method(
                self.unbind_device_from_gateway,
                default_timeout=120.0,
                client_info=client_info,
            ),
        }

    def close(self):
        """Closes resources associated with the transport.

       .. warning::
            Only call this method if the transport is NOT shared
            with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def create_device_registry(
        self,
    ) -> Callable[
        [device_manager.CreateDeviceRegistryRequest],
        Union[resources.DeviceRegistry, Awaitable[resources.DeviceRegistry]],
    ]:
        raise NotImplementedError()

    @property
    def get_device_registry(
        self,
    ) -> Callable[
        [device_manager.GetDeviceRegistryRequest],
        Union[resources.DeviceRegistry, Awaitable[resources.DeviceRegistry]],
    ]:
        raise NotImplementedError()

    @property
    def update_device_registry(
        self,
    ) -> Callable[
        [device_manager.UpdateDeviceRegistryRequest],
        Union[resources.DeviceRegistry, Awaitable[resources.DeviceRegistry]],
    ]:
        raise NotImplementedError()

    @property
    def delete_device_registry(
        self,
    ) -> Callable[
        [device_manager.DeleteDeviceRegistryRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_device_registries(
        self,
    ) -> Callable[
        [device_manager.ListDeviceRegistriesRequest],
        Union[
            device_manager.ListDeviceRegistriesResponse,
            Awaitable[device_manager.ListDeviceRegistriesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_device(
        self,
    ) -> Callable[
        [device_manager.CreateDeviceRequest],
        Union[resources.Device, Awaitable[resources.Device]],
    ]:
        raise NotImplementedError()

    @property
    def get_device(
        self,
    ) -> Callable[
        [device_manager.GetDeviceRequest],
        Union[resources.Device, Awaitable[resources.Device]],
    ]:
        raise NotImplementedError()

    @property
    def update_device(
        self,
    ) -> Callable[
        [device_manager.UpdateDeviceRequest],
        Union[resources.Device, Awaitable[resources.Device]],
    ]:
        raise NotImplementedError()

    @property
    def delete_device(
        self,
    ) -> Callable[
        [device_manager.DeleteDeviceRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_devices(
        self,
    ) -> Callable[
        [device_manager.ListDevicesRequest],
        Union[
            device_manager.ListDevicesResponse,
            Awaitable[device_manager.ListDevicesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def modify_cloud_to_device_config(
        self,
    ) -> Callable[
        [device_manager.ModifyCloudToDeviceConfigRequest],
        Union[resources.DeviceConfig, Awaitable[resources.DeviceConfig]],
    ]:
        raise NotImplementedError()

    @property
    def list_device_config_versions(
        self,
    ) -> Callable[
        [device_manager.ListDeviceConfigVersionsRequest],
        Union[
            device_manager.ListDeviceConfigVersionsResponse,
            Awaitable[device_manager.ListDeviceConfigVersionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_device_states(
        self,
    ) -> Callable[
        [device_manager.ListDeviceStatesRequest],
        Union[
            device_manager.ListDeviceStatesResponse,
            Awaitable[device_manager.ListDeviceStatesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.SetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.GetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Union[
            iam_policy_pb2.TestIamPermissionsResponse,
            Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def send_command_to_device(
        self,
    ) -> Callable[
        [device_manager.SendCommandToDeviceRequest],
        Union[
            device_manager.SendCommandToDeviceResponse,
            Awaitable[device_manager.SendCommandToDeviceResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def bind_device_to_gateway(
        self,
    ) -> Callable[
        [device_manager.BindDeviceToGatewayRequest],
        Union[
            device_manager.BindDeviceToGatewayResponse,
            Awaitable[device_manager.BindDeviceToGatewayResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def unbind_device_from_gateway(
        self,
    ) -> Callable[
        [device_manager.UnbindDeviceFromGatewayRequest],
        Union[
            device_manager.UnbindDeviceFromGatewayResponse,
            Awaitable[device_manager.UnbindDeviceFromGatewayResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("DeviceManagerTransport",)
