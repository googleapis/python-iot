from clearblade.cloud import iot_v1

async def sample_list_device_registries():
    # Create a client
    client = iot_v1.DeviceManagerAsyncClient()

    # Initialize request argument(s)
    request = iot_v1.ListDeviceRegistriesRequest(
        parent="projects/ingressdevelopmentenv/locations/us-central1",
    )

    # Make the request
    page_result = client.list_device_registries(request=request)

    # Handle the response
    async for response in page_result:
        print(response)