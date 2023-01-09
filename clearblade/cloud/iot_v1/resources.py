
class MqttState():
    r"""Indicates whether an MQTT connection is enabled or disabled.
    See the field description for details.
    """
    MQTT_STATE_UNSPECIFIED = "MQTT_STATE_UNSPECIFIED"
    MQTT_ENABLED = "MQTT_ENABLED"
    MQTT_DISABLED = "MQTT_DISABLED"


class HttpState():
    r"""Indicates whether DeviceService (HTTP) is enabled or disabled
    for the registry. See the field description for details.
    """
    HTTP_STATE_UNSPECIFIED = "HTTP_STATE_UNSPECIFIED"
    HTTP_ENABLED = "HTTP_ENABLED"
    HTTP_DISABLED = "HTTP_DISABLED"


class LogLevel:
    r"""**Beta Feature**

    The logging verbosity for device activity. Specifies which events
    should be written to logs. For example, if the LogLevel is ERROR,
    only events that terminate in errors will be logged. LogLevel is
    inclusive; enabling INFO logging will also enable ERROR logging.
    """
    LOG_LEVEL_UNSPECIFIED = "LOG_LEVEL_UNSPECIFIED"
    NONE = "NONE"
    ERROR = "ERROR"
    INFO = "INFO"
    DEBUG = "DEBUG"


class GatewayType:
    r"""Gateway type."""
    GATEWAY_TYPE_UNSPECIFIED = "GATEWAY_TYPE_UNSPECIFIED"
    GATEWAY = "GATEWAY"
    NON_GATEWAY = "NON_GATEWAY"


class GatewayAuthMethod():
    r"""The gateway authorization/authentication method. This setting
    determines how Cloud IoT Core authorizes/authenticate devices to
    access the gateway.
    """
    GATEWAY_AUTH_METHOD_UNSPECIFIED = "GATEWAY_AUTH_METHOD_UNSPECIFIED"
    ASSOCIATION_ONLY = "ASSOCIATION_ONLY"
    DEVICE_AUTH_TOKEN_ONLY = "DEVICE_AUTH_TOKEN_ONLY"
    ASSOCIATION_AND_DEVICE_AUTH_TOKEN = "ASSOCIATION_AND_DEVICE_AUTH_TOKEN"


class PublicKeyCertificateFormat():
    r"""The supported formats for the public key."""
    UNSPECIFIED_PUBLIC_KEY_CERTIFICATE_FORMAT = "UNSPECIFIED_PUBLIC_KEY_CERTIFICATE_FORMAT"
    X509_CERTIFICATE_PEM = "X509_CERTIFICATE_PEM"


class PublicKeyFormat:
    r"""The supported formats for the public key."""
    UNSPECIFIED_PUBLIC_KEY_FORMAT = "UNSPECIFIED_PUBLIC_KEY_FORMAT"
    RSA_PEM = "RSA_PEM"
    RSA_X509_PEM = "RSA_X509_PEM"
    ES256_PEM = "ES256_PEM"
    ES256_X509_PEM = "ES256_X509_PEM"
