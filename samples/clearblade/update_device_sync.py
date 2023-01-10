import os

from clearblade.cloud import iot_v1


def sample_update_device():
    client = iot_v1.DeviceManagerClient()

    registry_path = client.registry_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry")

    device = iot_v1.Device(id="python_11", blocked=True, log_level=iot_v1.LogLevel.ERROR)

    request = iot_v1.UpdateDeviceRequest(
        parent=registry_path,
        device=device,
        updateMask="logLevel"
    )

    response = client.update_device(request)

    print(response)


os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/rajas/Downloads/test-credentials.json"
sample_update_device()
