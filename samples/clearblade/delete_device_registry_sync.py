import os

from clearblade.cloud import iot_v1


def sample_delete_device_registry():
    # Create a client
    client = iot_v1.DeviceManagerClient()

    registry_path = client.registry_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry"
    )

    # Initialize request argument(s)
    request = iot_v1.DeleteDeviceRegistryRequest(name=registry_path)

    # Make the request
    response = client.delete_device_registry(request=request)

    print(response)


os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"

sample_delete_device_registry()
