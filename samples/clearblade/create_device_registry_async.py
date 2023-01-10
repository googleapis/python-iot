import asyncio
import os

from clearblade.cloud import iot_v1


async def sample_create_device_registry():
    # Create a client
    client = iot_v1.DeviceManagerAsyncClient()

    registry = iot_v1.DeviceRegistry(id='rajas-dummy-registry',
                                     mqttConfig={'mqttEnabledState':iot_v1.resources.MqttState.MQTT_ENABLED},
                                     httpConfig={'httpEnabledState':iot_v1.resources.HttpState.HTTP_ENABLED},
                                     logLevel=iot_v1.resources.LogLevel.ERROR,
                                     eventNotificationConfigs=[{'pubsubTopicName':'projects/ingressdevelopmentenv/topics/deleting'}]
                                     )

    # Initialize request argument(s)
    request = iot_v1.CreateDeviceRegistryRequest(
        parent="projects/api-project-320446546234/locations/us-central1",
        device_registry=registry
    )

    # Make the request
    response = await client.create_device_registry(request=request)

    # Handle the response
    print(response)

os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
asyncio.run(sample_create_device_registry())
