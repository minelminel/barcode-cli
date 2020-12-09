import os
import sys
import logging
from logging import StreamHandler
import argparse
from types import SimpleNamespace

import barcode
from barcode.writer import ImageWriter

log = logging.getLogger(__name__)
LEVELS = ["DEBUG", "INFO", "WARN"]

def get_defaults():
    defaults = SimpleNamespace(
        output=os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"),
        width=.35,
        height=10,
        log="INFO",
    )
    return defaults

def configure_logging(level):
    logging.basicConfig(format='%(asctime)s %(message)s', level=getattr(logging, level))
    log.info(f"Using log level: {level}")

def cli():
    default = get_defaults()
    parser = argparse.ArgumentParser(usage="barcoder [data] [options]" , description="Generate barcode image from input data")
    parser.add_argument("data", help="Integer to be encoded")
    parser.add_argument("--output", type=str, default=default.output, help=f"Path to folder where images will be saved, default={default.output}")
    parser.add_argument("--width", type=int, default=default.width, help=f"Width of output image, default={default.width}")
    parser.add_argument("--height", type=int, default=default.height, help=f"Height of output image, default={default.height}")
    parser.add_argument("--log", type=str, default=default.log, choices=LEVELS, help=f"Logging verbosity level. Choices are {LEVELS}")
    return parser

def create_output_folder(path):
    if not os.path.exists(path):
        log.info(f"Output folder does not yet exist, creating: {path}")
        try:
            os.mkdir(path)
        except Exception as e:
            log.error(e)
            sys.exit(1)
    else:
        log.info(f"Output folder already exists: {path}")
        pass

def main():
    parser = cli()
    if len(sys.argv) == 1:
        parser.print_help()
        return
    args = parser.parse_args()
    configure_logging(args.log)
    create_output_folder(args.output)
    log.info(f"Data to be written: {args.data}")
    img = barcode.get('code128', args.data, writer=ImageWriter())
    params = {
        "module_width": args.width, 
        "module_height": args.height, 
        "font_size": 18, 
        "text_distance": 1, 
        "quiet_zone": 3}
    filename = img.save(
        os.path.join(args.output, args.data),
        params)
    log.info(f"Saved file to: {filename}")

if __name__ == "__main__":
    main()
