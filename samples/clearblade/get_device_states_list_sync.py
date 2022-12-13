import os

from clearblade.cloud import iot_v1


def sample_get_device_states_list():
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(
        "api-project-320446546234",
        "us-central1",
        "test-registry",
        "test-dev-1"
    )

    request = iot_v1.ListDeviceStatesRequest(name=device_path, numStates=3)
    response = client.list_device_states(request)

    print(response.device_states)


os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/DummyUser/Downloads/test-credentials.json"
sample_get_device_states_list()
