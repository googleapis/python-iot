from clearblade.cloud import iot_v1


async def sample_update_device_registry():
    # Create a client
    client = iot_v1.DeviceManagerAsyncClient()

    # Initialize request argument(s)
    registry = iot_v1.DeviceRegistry(id='deleteTest5', name='deleteTest5',
                                     mqttConfig={'mqttEnabledState':'MQTT_DISABLED'},
                                     logLevel='ERROR')
    # Initialize request argument(s)
    request = iot_v1.UpdateDeviceRegistryRequest( name="projects/ingressdevelopmentenv/locations/us-central1/registries/deleteTest5",
                                                  updateMask='mqttConfig.mqtt_enabled_state,logLevel',
                                                  device_registry=registry
                                                )

    # Make the request
    response = await client.update_device_registry(request=request)

    # Handle the response
    print(response)
