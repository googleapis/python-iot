from clearblade.cloud import iot_v1

def sample_create_device():
    client = iot_v1.DeviceManagerClient()

    device = iot_v1.Device(id="Python_11", name="Python_11")
    request = iot_v1.CreateDeviceRequest(device=device)

    response = client.create_device(request)

sample_create_device()