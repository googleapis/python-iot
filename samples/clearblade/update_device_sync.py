import os

from clearblade.cloud import iot_v1


def sample_update_device():
    client = iot_v1.DeviceManagerClient()
    
    registry_path = client.registry_path(
        "api-project-320446546234", 
        "us-central1", 
        "rajas-test")
    
    device = iot_v1.Device(id="test-dev-1", blocked=True, log_level='NONE')

    request = iot_v1.UpdateDeviceRequest(
        parent=registry_path,
        device=device,
        updateMask="logLevel"
    )

    response = client.update_device(request)

    print(response)

os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/rajas/Downloads/test-credentials.json"
sample_update_device()
