
class MqttState():
    r"""Indicates whether an MQTT connection is enabled or disabled.
    See the field description for details.
    """
    MQTT_STATE_UNSPECIFIED = 0
    MQTT_ENABLED = 1
    MQTT_DISABLED = 2


class HttpState():
    r"""Indicates whether DeviceService (HTTP) is enabled or disabled
    for the registry. See the field description for details.
    """
    HTTP_STATE_UNSPECIFIED = 0
    HTTP_ENABLED = 1
    HTTP_DISABLED = 2


class LogLevel():
    r"""**Beta Feature**

    The logging verbosity for device activity. Specifies which events
    should be written to logs. For example, if the LogLevel is ERROR,
    only events that terminate in errors will be logged. LogLevel is
    inclusive; enabling INFO logging will also enable ERROR logging.
    """
    LOG_LEVEL_UNSPECIFIED = 0
    NONE = 10
    ERROR = 20
    INFO = 30
    DEBUG = 40


class GatewayType():
    r"""Gateway type."""
    GATEWAY_TYPE_UNSPECIFIED = 0
    GATEWAY = 1
    NON_GATEWAY = 2


class GatewayAuthMethod():
    r"""The gateway authorization/authentication method. This setting
    determines how Cloud IoT Core authorizes/authenticate devices to
    access the gateway.
    """
    GATEWAY_AUTH_METHOD_UNSPECIFIED = 0
    ASSOCIATION_ONLY = 1
    DEVICE_AUTH_TOKEN_ONLY = 2
    ASSOCIATION_AND_DEVICE_AUTH_TOKEN = 3


class PublicKeyCertificateFormat():
    r"""The supported formats for the public key."""
    UNSPECIFIED_PUBLIC_KEY_CERTIFICATE_FORMAT = 0
    X509_CERTIFICATE_PEM = 1


class PublicKeyFormat:
    r"""The supported formats for the public key."""
    UNSPECIFIED_PUBLIC_KEY_FORMAT = "UNSPECIFIED_PUBLIC_KEY_FORMAT"
    RSA_PEM = "RSA_PEM"
    RSA_X509_PEM = "RSA_X509_PEM"
    ES256_PEM = "ES256_PEM"
    ES256_X509_PEM = "ES256_X509_PEM"
