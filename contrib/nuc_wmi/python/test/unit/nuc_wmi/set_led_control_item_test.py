"""
The `test.unit.nuc_wmi.set_led_control_item_test` module provides unit tests for the functions in
`nuc_wmi.set_led_control_item`.

Classes:
    TestSetLedControlItem: A unit test class for the functions in `nuc_wmi.set_led_control_item`.
"""

import unittest

from mock import patch

from nuc_wmi import CONTROL_ITEM, CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR, LED_BRIGHTNESS_MULTI_COLOR
from nuc_wmi import LED_INDICATOR_OPTION, LED_TYPE, NucWmiError
from nuc_wmi.set_led_control_item import METHOD_ID, set_led_control_item

import nuc_wmi


class TestSetLedControlItem(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.set_led_control_item`

    Methods:
        setUp: Unit test initialization.
        test_set_led_control_item: Tests that it sends the expected byte list to the control file, tests that the
                                   returned control file response is properly processed, tests that it raises an
                                   exception when the control file returns an error code.
    """

    def setUp(self):
        """
        Initializes the unit tests;
        """

        self.maxDiff = None


    @patch('nuc_wmi.set_led_control_item.read_control_file')
    @patch('nuc_wmi.set_led_control_item.write_control_file')
    def test_Set_led_control_item(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `Set_led_control_item` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.set_led_control_item.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.set_led_control_item.write_control_file is nuc_wmi_write_control_file)

        # Branch 1: Test that set_led_control_item sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Set HDD LED HDD Activity Indicator Brightness of 30% for multi color led
        expected_write_byte_list = [
            METHOD_ID,
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Brightness',
                    'Options': LED_BRIGHTNESS_MULTI_COLOR
                }
            ),
            LED_BRIGHTNESS_MULTI_COLOR.index('30')
        ]
        read_byte_list = [
            0x00,
            0x00,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_set_led_control_item = set_led_control_item(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Brightness',
                    'Options': LED_BRIGHTNESS_MULTI_COLOR
                }
            ),
            LED_BRIGHTNESS_MULTI_COLOR.index('30')
        )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(returned_set_led_control_item, None)

        # Reset
        nuc_wmi_read_control_file.reset_mock()
        nuc_wmi_write_control_file.reset_mock()

        # Branch 2: Test that set_led_control_item raises an exception when the control file returns an
        #           error code.

        # Incorrect led
        expected_write_byte_list = [
            METHOD_ID,
            len(LED_TYPE['new']), # Incorrect led
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Brightness',
                    'Options': LED_BRIGHTNESS_MULTI_COLOR
                }
            ),
            LED_BRIGHTNESS_MULTI_COLOR.index('30')
        ]
        read_byte_list = [
            0xE4,
            0x00,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            returned_set_led_control_item = set_led_control_item(
                len(LED_TYPE['new']), # Incorrect led
                LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                    {
                        'Control Item': 'Brightness',
                        'Options': LED_BRIGHTNESS_MULTI_COLOR
                    }
                ),
                LED_BRIGHTNESS_MULTI_COLOR.index('30')
            )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(str(err.exception), 'Error (Invalid Parameter)')
