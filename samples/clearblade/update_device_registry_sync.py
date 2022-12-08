import os

from clearblade.cloud import iot_v1


def sample_update_device_registry():
    # Create a client
    client = iot_v1.DeviceManagerClient()
    registry = iot_v1.DeviceRegistry(
        id='deleteTest5', 
        name='deleteTest5',
        mqttConfig={'mqttEnabledState':'MQTT_DISABLED'},
        logLevel='ERROR'
    )
    # Initialize request argument(s)
    request = iot_v1.UpdateDeviceRegistryRequest( 
        name="projects/api-project-320446546234/locations/us-central1/registries/deleteTest5",
        updateMask='mqttConfig.mqtt_enabled_state,logLevel',
        device_registry=registry
    )

    # Make the request
    response = client.update_device_registry(request=request)

    # Handle the response
    print(response)

os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/rajas/Downloads/test-credentials.json"

sample_update_device_registry()
