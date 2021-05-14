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
from typing import (
    Any,
    AsyncIterable,
    Awaitable,
    Callable,
    Iterable,
    Sequence,
    Tuple,
    Optional,
)

from google.cloud.iot_v1.types import device_manager
from google.cloud.iot_v1.types import resources


class ListDeviceRegistriesPager:
    """A pager for iterating through ``list_device_registries`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.iot_v1.types.ListDeviceRegistriesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``device_registries`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDeviceRegistries`` requests and continue to iterate
    through the ``device_registries`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.iot_v1.types.ListDeviceRegistriesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., device_manager.ListDeviceRegistriesResponse],
        request: device_manager.ListDeviceRegistriesRequest,
        response: device_manager.ListDeviceRegistriesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.iot_v1.types.ListDeviceRegistriesRequest):
                The initial request object.
            response (google.cloud.iot_v1.types.ListDeviceRegistriesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = device_manager.ListDeviceRegistriesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[device_manager.ListDeviceRegistriesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.DeviceRegistry]:
        for page in self.pages:
            yield from page.device_registries

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDeviceRegistriesAsyncPager:
    """A pager for iterating through ``list_device_registries`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.iot_v1.types.ListDeviceRegistriesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``device_registries`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListDeviceRegistries`` requests and continue to iterate
    through the ``device_registries`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.iot_v1.types.ListDeviceRegistriesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[device_manager.ListDeviceRegistriesResponse]],
        request: device_manager.ListDeviceRegistriesRequest,
        response: device_manager.ListDeviceRegistriesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.iot_v1.types.ListDeviceRegistriesRequest):
                The initial request object.
            response (google.cloud.iot_v1.types.ListDeviceRegistriesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = device_manager.ListDeviceRegistriesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[device_manager.ListDeviceRegistriesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.DeviceRegistry]:
        async def async_generator():
            async for page in self.pages:
                for response in page.device_registries:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDevicesPager:
    """A pager for iterating through ``list_devices`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.iot_v1.types.ListDevicesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``devices`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDevices`` requests and continue to iterate
    through the ``devices`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.iot_v1.types.ListDevicesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., device_manager.ListDevicesResponse],
        request: device_manager.ListDevicesRequest,
        response: device_manager.ListDevicesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.iot_v1.types.ListDevicesRequest):
                The initial request object.
            response (google.cloud.iot_v1.types.ListDevicesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = device_manager.ListDevicesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[device_manager.ListDevicesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[resources.Device]:
        for page in self.pages:
            yield from page.devices

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDevicesAsyncPager:
    """A pager for iterating through ``list_devices`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.iot_v1.types.ListDevicesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``devices`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListDevices`` requests and continue to iterate
    through the ``devices`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.iot_v1.types.ListDevicesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[device_manager.ListDevicesResponse]],
        request: device_manager.ListDevicesRequest,
        response: device_manager.ListDevicesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.iot_v1.types.ListDevicesRequest):
                The initial request object.
            response (google.cloud.iot_v1.types.ListDevicesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = device_manager.ListDevicesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[device_manager.ListDevicesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[resources.Device]:
        async def async_generator():
            async for page in self.pages:
                for response in page.devices:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
