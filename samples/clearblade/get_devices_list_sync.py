from clearblade.cloud import iot_v1

def sample_get_devices_list():
    client = iot_v1.DeviceManagerClient()

    request = iot_v1.ListDevicesRequest(parent='projects/ingressdevelopmentenv/locations/us-central1')
    response = client.list_devices(request=request)
    for page_result in response:
        print(page_result)
