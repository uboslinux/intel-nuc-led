"""
`nuc_wmi.set_led_control_item` provides an interface to the WMI set control item function.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file

METHOD_ID = 0x06

def set_led_control_item(led_type, led_indicator_option, control_item, control_item_value, control_file=None):
    """
    Set the control item for the LED indicator option for the specified LED type,

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      control_item: The control item to set the value for.
      control_item_value: The value for the control item to set.
      led_indicator_option: The LED indicator option of the LED type for which to set the control item.
      led_type: The LED type for which to set the control item.
    Exceptions:
       Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
       or if `read_control_file` or `write_control_file` raise an exception.
    """

    set_led_control_item_byte_list = [METHOD_ID, led_type, led_indicator_option, control_item, control_item_value]

    write_control_file(set_led_control_item_byte_list, control_file=control_file)

    (
        error_code,
        reserved_byte_1,
        reserved_byte_2,
        reserved_byte_3
    ) = read_control_file(control_file=control_file)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))
