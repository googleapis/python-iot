import os

from clearblade.cloud import iot_v1


def sample_create_device_registry():
    # Create a client
    client = iot_v1.DeviceManagerClient()

    registry = iot_v1.DeviceRegistry(
        id='test-registry',
        mqttConfig={'mqttEnabledState':iot_v1.MqttState.MQTT_ENABLED},
        httpConfig={'httpEnabledState':iot_v1.HttpState.HTTP_ENABLED},
        logLevel=iot_v1.LogLevel.NONE,
        eventNotificationConfigs=[{'pubsubTopicName':'projects/api-project-320446546234/topics/deleting'}]
    )

    # Initialize request argument(s)
    request = iot_v1.CreateDeviceRegistryRequest(
        parent="projects/api-project-320446546234/locations/us-central1",
        device_registry=registry
    )

    # Make the request
    response = client.create_device_registry(request=request)

    # Handle the response
    print(response)


os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
sample_create_device_registry()
