"""Provenance CSV handler."""

import logging
from os.path import exists

try:
    from droidcsvhandlerclass import *
except ModuleNotFoundError:
    try:
        from src.anz_rosetta_csv.droidcsvhandlerclass import *
    except ModuleNotFoundError:
        from anz_rosetta_csv.droidcsvhandlerclass import *

logger = logging.getLogger(__name__)


class provenanceCSVHandler:
    # TODO: Better error handlin? Format error handling? Validation?
    provheaders = ["RECORDNUMBER", "NOTEDATE", "NOTETEXT"]

    def readProvenanceCSV(self, provcsvname):
        exportlist = None
        if not exists(provcsvname):
            logger.error(
                "it looks like you want to include provenance but the file doesn't exist: '%s'",
                provcsvname,
            )
        if exists(provcsvname):
            csvhandler = genericCSVHandler()
            exportlist = csvhandler.csvaslist(provcsvname)
            # counter a blank sheet
            if len(exportlist) < 1:
                exportlist = None
            if exportlist is not None:
                for h in self.provheaders:
                    if h not in exportlist[0]:
                        exportlist = None
                        break
        return exportlist
