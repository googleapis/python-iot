import os

from clearblade.cloud import iot_v1


def sample_unbind_device_from_gateway():
    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry")

    request = iot_v1.UnbindDeviceFromGatewayRequest(
        parent=parent,
        deviceId='test-dev-1',
        gatewayId='smason_test_gateway'
    )
    response = client.unbind_device_from_gateway(request)
    print(response)


os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
sample_unbind_device_from_gateway()
