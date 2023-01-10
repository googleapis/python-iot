from .utils import get_value
from .resources import HttpState, MqttState, LogLevel

class EventNotificationConfig:
    def __init__(self, pub_sub_topic_name, subfolder_matches=None) -> None:
        self._pub_sub_topic_name = pub_sub_topic_name
        self._sub_folder_matches = subfolder_matches

    @property
    def pub_sub_topic_name(self):
        return self._pub_sub_topic_name

    @property
    def sub_folder_matches(self):
        return self._sub_folder_matches

class DeviceRegistry:
    def __init__(self, id:str = None, name:str = None,
                 eventNotificationConfigs:list = [],
                 stateNotificationConfig:dict = {'pubsubTopicName': ''},
                 mqttConfig:dict = {'mqttEnabledState': MqttState.MQTT_ENABLED},
                 httpConfig:dict = {'httpEnabledState': HttpState.HTTP_ENABLED},
                 logLevel:str = LogLevel.NONE, credentials:list = []) -> None:
        self._id = id
        self._name = name
        self._event_notification_configs = eventNotificationConfigs
        self._state_notification_config = stateNotificationConfig
        self._mqtt_config = mqttConfig
        self._http_config = httpConfig
        self._loglevel = logLevel
        self._credentials = credentials

    @staticmethod
    def from_json(registry_json):
        event_notification_configs = []
        if "eventNotificationConfigs" in registry_json:
            event_notification_configs_json = registry_json['eventNotificationConfigs']

            for event_notification_config_json in event_notification_configs_json:
                if "subfolderMatches" in event_notification_config_json:
                    event_notification_config = EventNotificationConfig(event_notification_config_json['pubsubTopicName'], event_notification_config_json["subfolderMatches"])
                else:
                    event_notification_config = EventNotificationConfig(event_notification_config_json['pubsubTopicName'])
                event_notification_configs.append(event_notification_config)

        return DeviceRegistry(id=get_value(registry_json,'id'), name=get_value(registry_json,'name'),
                              eventNotificationConfigs=event_notification_configs,
                              stateNotificationConfig=get_value(registry_json,'stateNotificationConfig'),
                              mqttConfig=get_value(registry_json,'mqttConfig'),
                              httpConfig=get_value(registry_json,'httpConfig'),
                              credentials=get_value(registry_json,'credentials'),
                              logLevel=get_value(registry_json,'logLevel'))

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def event_notification_configs(self):
        return self._event_notification_configs

    @property
    def state_notification_config(self):
        return self._state_notification_config

    @property
    def mqtt_config(self):
        return self._mqtt_config

    @property
    def http_config(self):
        return self._http_config

    @property
    def log_level(self):
        return self._loglevel

    @property
    def credentials(self):
        return self._credentials
    
class CreateDeviceRegistryRequest:
    def __init__(self, parent:str = None,
                 device_registry:DeviceRegistry = None) -> None:
        self._parent = parent
        self._device_registry = device_registry

    @property
    def parent(self) -> str:
        return self._parent

    @property
    def device_registry(self)-> DeviceRegistry:
        return self._device_registry

class UpdateDeviceRegistryRequest:
    def __init__(self, name:str = None,
                 updateMask:str = None,
                 device_registry:DeviceRegistry = None) -> None:
        self._name = name
        self._update_mask = updateMask
        self._device_registry = device_registry

    @property
    def name(self) -> str:
        return self._name

    @property
    def update_mask(self) -> str:
        return self._update_mask

    @property
    def device_registry(self)-> DeviceRegistry:
        return self._device_registry

class GetDeviceRegistryRequest:
    def __init__(self, name:str = None) -> None:
        self._name = name
    
    @property
    def name(self):
        return self._name

class DeleteDeviceRegistryRequest:
    def __init__(self, name:str = None) -> None:
        self._name = name
    
    @property
    def name(self):
        return self._name


class ListDeviceRegistriesRequest:
    def __init__(self, parent:str = None,
                 page_size:int = None,
                 page_token:str = None) -> None:
        self._parent = parent
        self._page_size = page_size
        self._page_token = page_token

    @property
    def parent(self):
        return self._parent

    @property
    def page_size(self):
        return self._page_size

    @property
    def page_token(self):
        return self._page_token

class ListDeviceRegistriesResponse:
    def __init__(self, device_registries, next_page_token) -> None:
        self._device_registries = device_registries
        self._next_page_token = next_page_token

    @property
    def raw_page(self):
        return self

    @property
    def device_registries(self):
        return self._device_registries

    @property
    def next_page_token(self):
        return self._next_page_token

    @staticmethod
    def from_json(response_json):
        devices_registries_json = get_value(response_json, 'deviceRegistries')
        next_page_token = get_value(response_json, 'nextPageToken')
        device_registries = []

        for device_registry_json in devices_registries_json:
            device_registry = DeviceRegistry.from_json(registry_json=device_registry_json)
            device_registries.append(device_registry)

        return ListDeviceRegistriesResponse(device_registries, next_page_token)