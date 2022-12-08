import json
import httpx
from .config import *

class HttpClient():
    def __init__(self,
                 clearblade_config:ClearBladeConfig = None) -> None:

        self._clearblade_config = clearblade_config
        self._system_key = self._clearblade_config.system_key
        self._auth_token = self._clearblade_config.token
        self._post_url : str = None
        self._request_headers : dict = None
        self._post_body : dict = None

    def _get_time_out(self):
        return httpx.Timeout(timeout=10.0, read=None)

    def _get_api_url(self, api_name:str = None, is_web_hook:bool = True) -> str:
        api_web_hook_path = "api/v/4/webhook/execute"
        if not is_web_hook:
            api_web_hook_path = "api/v/1/code"

        return "{}:{}/{}/{}/{}?".format(self._clearblade_config.api_url,
                                        "443",
                                        api_web_hook_path,
                                        self._system_key,
                                        api_name)

    def _headers(self):
        return {'ClearBlade-UserToken':self._clearblade_config.token, 'Content-Type':'application/json'}

    def _process_request_body(self, request_body = {}):
        return json.dumps(request_body)

    def get(self,api_name:str = None):
        self._post_url = self._get_api_url(api_name=api_name)
        self._request_headers = self._headers()

    def post(self, api_name:str = None,
             is_webhook_folder:bool = True,
             request_body:dict = {}):

        self._post_url = self._get_api_url(api_name=api_name, is_web_hook=is_webhook_folder)
        self._request_headers = self._headers()
        self._post_body = self._process_request_body(request_body=request_body)

    def delete(self,api_name:str = None):
        self._post_url = self._get_api_url(api_name=api_name)
        self._request_headers = self._headers()

    def patch(self, api_name:str = None, request_body:dict = {}):
        self._post_url = self._get_api_url(api_name=api_name)
        self._request_headers = self._headers()
        self._post_body = self._process_request_body(request_body=request_body)

class SyncClient(HttpClient):

    def __init__(self, clearblade_config: ClearBladeConfig = None) -> None:
        super().__init__(clearblade_config)
        self._sync_client = httpx.Client(timeout=self._get_time_out())

    def get(self, api_name:str = None, request_params:dict = {}):
        super().get(api_name=api_name)
        response = self._sync_client.get(url=self._post_url,
                                     headers=self._request_headers,
                                     params=request_params)
        self._sync_client.close()
        return response

    def post(self, api_name:str = None,
             is_webhook_folder:bool = True,
             request_params = {}, request_body = {}):
        super().post(api_name=api_name, is_webhook_folder=is_webhook_folder,
                     request_body=request_body)
        response = self._sync_client.post(url=self._post_url,
                                      headers=self._request_headers,
                                      params=request_params,
                                      data=self._post_body)
        self._sync_client.close()
        return response

    def delete(self, api_name:str = None, request_params:dict = None):
        super().delete(api_name = api_name)
        response = self._sync_client.delete(url=self._post_url,
                                        headers=self._request_headers,
                                        params=request_params)
        self._sync_client.close()
        return response

    def patch(self, api_name: str = None, request_body: dict = {}, request_params:dict = {}):
        super().patch(api_name, request_body)
        response = self._sync_client.patch(url=self._post_url,
                                           headers=self._request_headers,
                                           params = request_params,
                                           data=self._post_body)
        self._sync_client.close()
        return response

class AsyncClient(HttpClient):

    def __init__(self, clearblade_config: ClearBladeConfig = None) -> None:
        super().__init__(clearblade_config)
        self._async_client = httpx.AsyncClient(timeout=self._get_time_out())

    async def get(self, api_name:str = None, request_params:dict = {}):
        super().get(api_name=api_name)
        response = await self._async_client.get(url=self._post_url,
                                            headers=self._request_headers,
                                            params=request_params)
        await self._async_client.aclose()
        return response

    async def post(self, api_name:str = None,
                   is_webhook_folder:bool = True,
                   request_params = {}, request_body={}):
        super().post(api_name=api_name, is_webhook_folder=is_webhook_folder,
                     request_body=request_body)
        response = await self._async_client.post(url=self._post_url,
                                             headers=self._request_headers,
                                             params=request_params,
                                             data=self._post_body)
        await self._async_client.aclose()
        return response

    async def delete(self, api_name:str = None, request_params:dict = {}):
        super().delete(api_name=api_name)
        return await self._async_client.delete(url=self._post_url,
                                               headers=self._request_headers,
                                               params=request_params)

    async def patch(self, api_name:str = None, request_params:dict = {}, request_body:dict = {}):
        super().patch(api_name = api_name, request_body=request_body)
        return await self._async_client.patch(url=self._post_url,
                                              headers=self._request_headers,
                                              params = request_params,
                                              data=self._post_body)
