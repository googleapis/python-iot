from clearblade.cloud import iot_v1


async def sample_delete_device_registry():
    # Create a client
    client = iot_v1.DeviceManagerAsyncClient()

    # Initialize request argument(s)
    request = iot_v1.DeleteDeviceRegistryRequest(
        name="projects/ingressdevelopmentenv/locations/us-central1/registries/deleteTest2"
    )

    # Make the request
    await client.delete_device_registry(request=request)
