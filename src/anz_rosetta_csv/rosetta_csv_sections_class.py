"""Rosetta CSV sections handler."""

import configparser as ConfigParser
import logging
import sys

logger = logging.getLogger(__name__)


class RosettaCSVSections:
    """Rosetta CSV sections handler object."""

    sections = None
    config = None

    def __init__(self, configfile):
        logging.info("reading app config from '%s'", configfile)
        self.config = ConfigParser.RawConfigParser()
        self.config.read(configfile)

        # Configure via CFG to avoid users having to edit code
        sections = []
        if self.config.has_option("rosetta csv fields", "CSVSECTIONS"):
            sections = self.config.get("rosetta csv fields", "CSVSECTIONS").split(",")

        self.sections = []
        for section in sections:
            if self.config.has_option("rosetta csv fields", section):
                sectiondict = {}
                fieldlist = self.config.get("rosetta csv fields", section)
                sectiondict[section] = fieldlist.split(",")
                self.sections.append(sectiondict)
            else:
                logging.error("error reading fields from config file, exiting...")
                sys.exit(1)
