import argparse


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
