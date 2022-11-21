from clearblade.cloud import iot_v1


async def sample_get_device_registry():
    # Create a client
    client = iot_v1.DeviceManagerAsyncClient()

    # Initialize request argument(s)
    request = iot_v1.GetDeviceRegistryRequest(
        name="name_value",
    )

    # Make the request
    response = await client.get_device_registry(request=request)

    # Handle the response
    print(response)
