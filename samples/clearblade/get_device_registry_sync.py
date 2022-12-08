import os

from clearblade.cloud import iot_v1


def sample_get_device_registry():
    # Create a client
    client = iot_v1.DeviceManagerClient()

    registry_path = client.registry_path(
        "api-project-320446546234", 
        "us-central1", 
        "rajas-test")

    # Initialize request argument(s)
    request = iot_v1.GetDeviceRegistryRequest(
        name=registry_path,
    )

    # Make the request
    response = client.get_device_registry(request=request)

    # Handle the response
    print(response.name)

os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/rajas/Downloads/test-credentials.json"
sample_get_device_registry()
