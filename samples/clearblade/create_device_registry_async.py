import asyncio
import os

from clearblade.cloud import iot_v1


async def sample_create_device_registry():
    # Create a client
    client = iot_v1.DeviceManagerAsyncClient()

    registry = iot_v1.DeviceRegistry(id='test-registry', name='test-registry',
                                     mqttConfig={'mqttEnabledState':'MQTT_ENABLED'},
                                     httpConfig={'httpEnabledState':'HTTP_ENABLED'},
                                     logLevel='ERROR',
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