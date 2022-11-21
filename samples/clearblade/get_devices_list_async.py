from clearblade.cloud import iot_v1

async def sample_get_devices_list_async():
    client = iot_v1.DeviceManagerAsyncClient()

    request = iot_v1.ListDevicesRequest(parent='projects/ingressdevelopmentenv/locations/us-central1')

    response = await client.list_devices(request)
    for page_result in response:
        print(page_result)