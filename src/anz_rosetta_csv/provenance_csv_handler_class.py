"""Provenance CSV handler."""

import logging
from os.path import exists

try:
    from droid_csv_handler_class import GenericCSVHandler
except ModuleNotFoundError:
    try:
        from src.anz_rosetta_csv.droid_csv_handler_class import GenericCSVHandler
    except ModuleNotFoundError:
        from anz_rosetta_csv.droid_csv_handler_class import GenericCSVHandler

logger = logging.getLogger(__name__)


class ProvenanceCSVHandler:
    """Provenance CSV handler class."""

    provheaders = ["RECORDNUMBER", "NOTEDATE", "NOTETEXT"]

    def read_provenance_csv(self, provcsvname):
        """Read provenance CSV and return it to the caller."""
        exportlist = None
        if not exists(provcsvname):
            logger.error(
                "it looks like you want to include provenance but the file doesn't exist: '%s'",
                provcsvname,
            )
        if exists(provcsvname):
            csvhandler = GenericCSVHandler()
            exportlist = csvhandler.csv_as_list(provcsvname)
            # counter a blank sheet
            if len(exportlist) < 1:
                exportlist = None
            if exportlist is not None:
                for h in self.provheaders:
                    if h not in exportlist[0]:
                        exportlist = None
                        break
        return exportlist
