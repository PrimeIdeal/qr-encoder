import argparse

from common import select_encoder


def get_parser() -> argparse.ArgumentParser:
    """
    Creates command line parser for the encoding process.

    Returns
    -------
    argparse.ArgumentParser
        Parser object.
    """
    parser = argparse.ArgumentParser(description='Parser for QR Encoder')

    parser.add_argument(
        '-c',
        '--correction-level',
        type=str,
        default='L',
        help='Error correction level for the QR encoder.'
    )
    parser.add_argument(
        '-f',
        '--file-path',
        type=str,
        default=None,
        help='File path for text to be encoded.'
    )
    parser.add_argument(
        '-t',
        '--text',
        type=str,
        default=None,
        help='Text string to be encoded.'
    )

    return parser


def main():
    args = get_parser().parse_args()

    if args.file_path is not None:
        with open(args.file_path) as file:
            message = file.read()
    else:
        message = args.text

    encoder = select_encoder(message, args.correction_level)
