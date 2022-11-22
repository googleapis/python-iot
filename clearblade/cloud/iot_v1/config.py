class ClearBladeConfig:
    def __init__(self, system_key:str = None,
                 auth_token:str = None,
                 api_url:str = None,
                 region:str = None,
                 project:str = None ) -> None:
        self._system_key = system_key
        self._auth_token = auth_token
        self._api_url = api_url
        self._region = region
        self._project = project

    @property
    def system_key(self):
        return self._system_key

    @property
    def token(self):
        return self._auth_token

    @property
    def api_url(self):
        return self._api_url

    @property
    def project(self):
        return self._project

    @property
    def region(self):
        return self._region
