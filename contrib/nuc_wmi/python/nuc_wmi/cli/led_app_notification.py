"""
`nuc_wmi.cli.led_app_notification` provides a CLI interface to the WMI notification functions.
"""

from __future__ import print_function

from argparse import ArgumentParser
from json import dumps
from sys import exit

from nuc_wmi import CONTROL_FILE
from nuc_wmi.led_app_notification import save_led_config

def save_led_config_cli(cli_args=None):
    """
    Send a save LED configuration LED app notification.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with notification state or error message with
               failure error.
    Exit code:
       0 on successfully sending the save led config notification or 1 on error.
    """

    parser = ArgumentParser(
        description='Send a save LED configuration app notification.'
    )

    parser.add_argument(
        '-c',
        '--control-file',
        default=None,
        help='The path to the NUC WMI control file. Defaults to ' + CONTROL_FILE + ' if not specified.'
    )

    try:
        args = parser.parse_args(args=cli_args)

        save_led_config(control_file=args.control_file)

        print(
            dumps(
                {
                    'led_app_notification': {
                        'type': 'save_led_config'
                    }
                }
            )
        )
    except Exception as err:
        print(dumps({'error': str(err)}))

        exit(1)
