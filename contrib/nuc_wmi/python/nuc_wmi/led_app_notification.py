"""
`nuc_wmi.led_app_notification` provides an interface to the WMI notification functions.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file

METHOD_ID=0x07

NOTIFICATION_TYPE = [
    None,
    'save_led_config'
]

def save_led_config(control_file=None):
    """
    Send a save LED configuration LED app notification.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
    Exceptions:
       Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
       or if `read_control_file` or `write_control_file` raise an exception.
    """

    notification_byte_list = [
        METHOD_ID,
        NOTIFICATION_TYPE.index('save_led_config')
    ]

    write_control_file(notification_byte_list, control_file=control_file)

    (
        error_code,
        reserved_byte_1,
        reserved_byte_2,
        reserved_byte_3
    ) = read_control_file(control_file=control_file)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))
