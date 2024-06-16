"""Archives New Zealand Rosetta CSV Generator."""

import argparse
import configparser as ConfigParser
import logging
import sys
import time

try:
    from rosetta_csv_generator import RosettaCSVGenerator
except ModuleNotFoundError:
    try:
        from src.anz_rosetta_csv.rosetta_csv_generator import RosettaCSVGenerator
    except ModuleNotFoundError:
        from anz_rosetta_csv.rosetta_csv_generator import RosettaCSVGenerator


logger = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)-15s %(levelname)s :: %(filename)s:%(lineno)s:%(funcName)s() :: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO",
)

# Default to UTC time.
logging.Formatter.converter = time.gmtime


def main():
    """Primary entry point for this script."""

    parser = argparse.ArgumentParser(
        description="Generate a Rosetta Ingest CSV from Collections List Control and DROID CSV Reports."
    )
    parser.add_argument(
        "--csv", help="Single DROID CSV to read.", default=False, required=False
    )
    parser.add_argument(
        "--exp",
        help="Archway list control sheet to map to Rosetta ingest CSV",
        default=False,
        required=False,
    )
    parser.add_argument(
        "--ros", help="Rosetta CSV validation schema", default=False, required=False
    )
    parser.add_argument(
        "--cfg", help="Config file for field mapping.", default=False, required=False
    )
    parser.add_argument(
        "--pro",
        "--prov",
        help="Flag to enable use of prov.notes file.",
        default=False,
        required=False,
    )
    parser.add_argument(
        "--args",
        "--arg",
        help="Concatenate arguments into a file for ease of use.",
        default=False,
        required=False,
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()
    if args.args:
        config = ConfigParser.RawConfigParser()
        config.read(args.args)
        if config.has_option("arguments", "title"):
            logger.info("using the '%s' args file", config.get("arguments", "title"))
        logging.info("reading args from: '%s'", args.args)
        if config.has_option("arguments", "droidexport"):
            args.csv = config.get("arguments", "droidexport")
            args.ros = config.get("arguments", "schemafile")
            args.cfg = config.get("arguments", "configfile")
            args.exp = config.get("arguments", "listcontrol")
            args.pro = config.get("arguments", "provenance")

    if args.csv and args.exp and args.ros and args.cfg:
        csvgen = RosettaCSVGenerator(
            droidcsv=args.csv,
            exportsheet=args.exp,
            rosettaschema=args.ros,
            configfile=args.cfg,
            provenance=args.pro,
        )
        res = csvgen.export_to_rosetta_csv()
        print(res)
        sys.exit()

    parser.print_help()
    sys.exit()


if __name__ == "__main__":
    main()
