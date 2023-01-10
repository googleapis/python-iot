import os

from clearblade.cloud import iot_v1


def sample_create_device():
    client = iot_v1.DeviceManagerClient()
    parent = client.registry_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry")

    device = iot_v1.Device(
        id="Python_12", 
        gateway_config={"gatewayType": iot_v1.GatewayType.NON_GATEWAY},
        log_level=iot_v1.LogLevel.ERROR)
    
    request = iot_v1.CreateDeviceRequest(parent=parent, device=device)

    response = client.create_device(request)
    print(response)


os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
sample_create_device()
