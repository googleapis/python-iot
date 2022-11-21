from clearblade.cloud import iot_v1


def sample_create_device():
    # Create a client
    client = iot_v1.DeviceManagerClient()

    registry = iot_v1.DeviceRegistry(id='deleteTest5', name='deleteTest5',
                                     mqttConfig={'mqttEnabledState':'MQTT_ENABLED'},
                                     httpConfig={'httpEnabledState':'HTTP_ENABLED'},
                                     logLevel='ERROR',
                                     eventNotificationConfigs=[{'pubsubTopicName':'projects/ingressdevelopmentenv/topics/deleting'}]
                                     )

    # Initialize request argument(s)
    request = iot_v1.CreateDeviceRegistryRequest(
        parent="projects/ingressdevelopmentenv/locations/us-central1",
        device_registry=registry
    )

    # Make the request
    response = client.create_device(request=request)

    # Handle the response
    print(response)

