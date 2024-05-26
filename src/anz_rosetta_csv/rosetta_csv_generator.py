"""Archives New Zealand Rosetta CSV Generator."""

# pylint: disable=R1710,R0902,R0913,R0912

import configparser as ConfigParser
import logging
import sys

try:
    import json_table_schema
    from droid_csv_handler_class import DroidCSVHandler, GenericCSVHandler
    from import_sheet_generator import ImportSheetGenerator
    from provenance_csv_handler_class import ProvenanceCSVHandler
    from rosetta_csv_sections_class import RosettaCSVSections
except ModuleNotFoundError:
    try:
        from src.anz_rosetta_csv.droid_csv_handler_class import (
            DroidCSVHandler,
            GenericCSVHandler,
        )
        from src.anz_rosetta_csv.import_sheet_generator import ImportSheetGenerator
        from src.anz_rosetta_csv.json_table_schema import json_table_schema
        from src.anz_rosetta_csv.provenance_csv_handler_class import (
            ProvenanceCSVHandler,
        )
        from src.anz_rosetta_csv.rosetta_csv_sections_class import RosettaCSVSections
    except ModuleNotFoundError:
        from anz_rosetta_csv.droid_csv_handler_class import (
            DroidCSVHandler,
            GenericCSVHandler,
        )
        from anz_rosetta_csv.import_sheet_generator import ImportSheetGenerator
        from anz_rosetta_csv.json_table_schema import json_table_schema
        from anz_rosetta_csv.provenance_csv_handler_class import ProvenanceCSVHandler
        from anz_rosetta_csv.rosetta_csv_sections_class import RosettaCSVSections

logger = logging.getLogger(__name__)


def ingest_path_from_droid_row(droid_row: dict, path_mask: str) -> bool:
    """Return an ingest path from a droid row with pathmask removed."""
    file_name = droid_row["NAME"].strip()
    file_path = droid_row["FILE_PATH"].strip()
    ingest_path = file_path.replace(file_name, "").replace(path_mask, "", 1)
    ingest_path = ingest_path.replace("\\", "/")
    return ingest_path.strip()


def find_path_from_subseries(
    record_title: str, droid_row: dict, lc_sub_series: str, series_mask: str
) -> bool:
    """Determine the path to add to the CSV from its sub-series"""
    file_name = droid_row["NAME"].strip()
    file_path = droid_row["FILE_PATH"].strip()
    if record_title.strip() not in file_path:
        return False
    compare = file_path.replace(file_name, "").replace(series_mask, "", 1).strip()[:-1]
    return compare == lc_sub_series


class RosettaCSVGenerator:
    """Rosetta CSV Generator Object."""

    config = None
    droidcsv = None
    exportsheet = None
    rosettaschema = None
    rosettasections = None
    prov = None
    rosettacsvdict = None

    def __init__(
        self,
        droidcsv=None,
        exportsheet=None,
        rosettaschema=None,
        configfile=None,
        provenance=None,
    ):
        if not configfile:
            logger.error("a configuration file hasn't been provided")
            sys.exit(1)

        self.subseriesmask = None
        self.rnumber = None
        self.droidlist = None
        self.exportlist = None
        self.provlist = None
        self.duplicates = None

        logging.info("reading app config from '%s'", configfile)
        self.config = ConfigParser.RawConfigParser()
        self.config.read(configfile)

        self.droidcsv = droidcsv
        self.exportsheet = exportsheet

        # NOTE: A bit of a hack, compare with import schema work and refactor
        self.rosettaschema = rosettaschema
        self.read_rosetta_schema()

        # Grab Rosetta Sections
        rs = RosettaCSVSections(configfile)
        self.rosettasections = rs.sections

        # set provenance flag and file
        self.prov = False
        if provenance:
            self.prov = True
            self.provfile = provenance
            logger.info("provenance being read from : `%s`", self.provfile)
            if self.config.has_option("provenance", "file"):
                # Legacy mechanism to override the detaul provenance
                # file. This can be removed in future.
                self.provfile = self.config.get("provenance", "file")

            self.provhash = "MD5"
            if self.config.has_option("application configuration", "provhash"):
                self.provhash = self.config.get("application configuration", "provhash")

        self.pathmask = self.__setpathmask__()

        # Get some functions from ImportGenerator
        self.impgen = ImportSheetGenerator()

        # List duplicate items to check...
        self.duplicateitemsaddedset = set()

    def add_csv_value(self, value):
        """Format the value for the CSV."""
        value = value.replace("\r", "").replace("\n", "")
        field = f'"{value}"'
        return field

    def read_rosetta_schema(self):
        """Read the Rosetta Schema File."""
        importschemajson = None
        with open(self.rosettaschema, "r", encoding="utf-8") as rosetta_schema:
            importschemajson = rosetta_schema.read()
        importschema = json_table_schema.JSONTableSchema(importschemajson)

        importschemadict = importschema.as_dict()
        importschemaheader = importschema.as_csv_header()

        self.rosettacsvheader = importschemaheader + "\n"
        self.rosettacsvdict = importschemadict["fields"]

    def createcolumns(self, column_number):
        """Create a number of empty columns in Rosetta CSV."""
        columns = ""
        for _ in range(column_number):
            columns = f'{columns}"",'
        return columns

    def normalize_spaces(self, filename):
        """Normalize spacces in a filename."""
        if filename.find("  ") != -1:
            filename = filename.replace("  ", " ")
            return self.normalize_spaces(filename)
        return filename

    def compare_filenames_as_titles(self, droidrow, listcontroltitle):
        """Test filename titles to confirm equivalence."""
        droid_filename_title = self.impgen.get_title(droidrow["NAME"])
        normalized_droid_filename = self.normalize_spaces(droid_filename_title)
        normalized_lc_title = self.normalize_spaces(listcontroltitle)
        if normalized_droid_filename == normalized_lc_title:
            return True
        return False

    def get_droid_value(
        self, checksum, lc_title, lc_sub_series, rosetta_field, droid_field, path_mask
    ):
        """Retrieve a row from a DROID sheet."""
        returnfield = ""
        for drow in self.droidlist:
            addtorow = False

            checksumfromdroid = ""
            if "MD5_HASH" in drow:
                checksumfromdroid = drow["MD5_HASH"]
            elif "SHA1_HASH" in drow:
                checksumfromdroid = drow["SHA1_HASH"]
            elif "SHA256_HASH" in drow:
                checksumfromdroid = drow["SHA256_HASH"]
            elif "SHA512_HASH" in drow:
                checksumfromdroid = drow["SHA512_HASH"]
            else:
                logger.error("no hash available to use in DROID export.")
                sys.exit(1)

            if checksumfromdroid == checksum:
                if not self.compare_filenames_as_titles(drow, lc_title):
                    continue

                # Performance, only do more work, if we have to care about it...
                if checksumfromdroid not in self.duplicates:
                    addtorow = True
                else:
                    addtorow = find_path_from_subseries(
                        record_title=lc_title,
                        droid_row=drow,
                        lc_sub_series=lc_sub_series,
                        series_mask=self.subseriesmask,
                    )
                    item_to_monitor = (
                        f"{lc_sub_series}\\{lc_title} checksum: {checksumfromdroid}"
                    )
                    self.duplicateitemsaddedset.add(item_to_monitor)

            if addtorow is True:
                droidfield = drow[droid_field]
                if rosetta_field == "File Original Path":
                    returnfield = ingest_path_from_droid_row(
                        droid_row=drow, path_mask=path_mask
                    )
                else:
                    returnfield = droidfield

        return returnfield

    def csvstringoutput(self, csvlist):
        """Output CSV as a string."""

        csvrows = self.rosettacsvheader
        sip_row = ['"",'] * len(self.rosettacsvdict)
        sip_row[0] = '"SIP",'
        sip_title = '"CSV Load",'
        if self.config.has_option("rosetta mapping", "SIP Title"):
            sip_title = f'"{self.config.get("rosetta mapping", "SIP Title")}",'
        sip_row[1] = sip_title
        sip_row = "".join(sip_row).rstrip(",")
        csvrows = f"{csvrows}{sip_row}\n"
        for sectionrows in csvlist:
            rowdata = ""
            for sectionrow in sectionrows:
                for fielddata in sectionrow:
                    rowdata = f"{rowdata}{fielddata},"
                rowdata = f'{rowdata.rstrip(",")}\n'
            csvrows = csvrows + rowdata

        # this is the best i can think of because ExLibris have named two fields
        # with the same title in CSV which doesn't help us when we're trying to
        # use unique names for populating rows replaces SIP Title with Title (DC)
        csvrows = csvrows.replace(
            '"Object Type","SIP Title"', '"Object Type","Title (DC)"'
        )

        for dupe in self.duplicateitemsaddedset:
            logger.info("duplicates to monitor: %s", dupe)

        return csvrows

    def handleprovenanceexceptions(
        self, provenance_field, sectionrow, field, csvindex, rnumber
    ):
        """Read a provenance CSV file for exceptions on specific rows."""
        ignorefield = False
        if not self.prov:
            return False
        for p_row in self.provlist:
            if p_row["RECORDNUMBER"] != rnumber:
                continue
            if (provenance_field == "CHECKSUM" and field == self.provhash) or (
                provenance_field == "ORIGINALNAME" and field == "File Original Name"
            ):
                if p_row[provenance_field].lower().strip() != "ignore":
                    ignorefield = True
                    sectionrow[csvindex] = self.add_csv_value(p_row[provenance_field])
        return ignorefield

    def __setpathmask__(self):
        pathmask = ""
        if self.config.has_option("path values", "pathmask"):
            pathmask = self.config.get("path values", "pathmask")
        return pathmask

    def populaterows(self, field, listcontrolitem, sectionrow, csvindex, rnumber):
        """Populate the rows in the Rosetta CSV."""

        # populate cell with static values from config file
        if self.config.has_option("static values", field):
            rosettafield = self.config.get("static values", field)
            sectionrow[csvindex] = self.add_csv_value(rosettafield)

        # if there is a mapping configured to the list control, grab the value
        if self.config.has_option("rosetta mapping", field):
            rosettafield = self.config.get("rosetta mapping", field)
            addvalue = listcontrolitem[rosettafield]

            # ****MULTIPLE ACCESS RESTRICTIONS****#
            # If the field we've got in the config file is Access, we need to
            # Then grab the Rosetta access code for the correct restriction status
            # Following a trail somewhat, but enables more flexible access restrictions in
            if field == "Access Rights Policy ID (IE)":
                if self.config.has_option("access values", addvalue):
                    # addvalue becomes the specific code given to a specific restriction status...
                    addvalue = self.config.get("access values", addvalue)

            # place value into the cell within the row...
            sectionrow[csvindex] = self.add_csv_value(addvalue)

        # if there is a mapping to a value in the droid export...
        elif self.config.has_option("droid mapping", field):
            rosettafield = self.config.get("droid mapping", field)
            ignorefield = self.handleprovenanceexceptions(
                "ORIGINALNAME", sectionrow, field, csvindex, rnumber
            )

            # if ignorefield is still false, check our checksum field as well...
            if not ignorefield:
                ignorefield = self.handleprovenanceexceptions(
                    "CHECKSUM", sectionrow, field, csvindex, rnumber
                )

            if not ignorefield:
                sectionrow[csvindex] = self.add_csv_value(
                    self.get_droid_value(
                        checksum=listcontrolitem["Missing Comment"],
                        lc_title=listcontrolitem["Title"],
                        lc_sub_series=listcontrolitem["Sub-Series"],
                        rosetta_field=field,
                        droid_field=rosettafield,
                        path_mask=self.pathmask,
                    )
                )

        elif self.prov is True:
            for p in self.provlist:
                if p["RECORDNUMBER"] == rnumber:
                    if field == "Event Identifier Type":
                        sectionrow[csvindex] = self.add_csv_value("EXTERNAL")
                    if field == "Event Identifier Value":
                        sectionrow[csvindex] = self.add_csv_value("EXT_1")
                    if field == "Event Type":
                        sectionrow[csvindex] = self.add_csv_value("CREATION")
                    if field == "Event Description":
                        sectionrow[csvindex] = self.add_csv_value("Provenance Note")
                    if field == "Event Date":
                        sectionrow[csvindex] = self.add_csv_value(p["NOTEDATE"])
                    if field == "Event Outcome1":
                        sectionrow[csvindex] = self.add_csv_value("SUCCESS")
                    if field == "Event Outcome Detail1":
                        sectionrow[csvindex] = self.add_csv_value(p["NOTETEXT"])

    def create_rosetta_csv(self):
        """Primary loop to create the Rosetta CSV from the given list
        control.
        """
        self.subseriesmask = ""
        if self.duplicates:
            logger.info(
                "duplicate checksums in list control, ensure '[path values] subseriesmask=' is set in config"
            )
            if self.config.has_option("path values", "subseriesmask"):
                self.subseriesmask = self.config.get("path values", "subseriesmask")
            else:
                logger.info("subseries mask is not set in config")

        csv_index_start = 2
        csvindex = csv_index_start

        self.rnumber = 0
        fields = []

        for item in self.exportlist:
            itemrow = []

            # self.rosettasections, list of dictionaries generated from CFG file...
            for sections in self.rosettasections:
                # sections, individual dictionaries from CFG file...

                # section row is entire length of x-axis in spreadsheet from CSV JSON Config file...
                sectionrow = ['""'] * len(self.rosettacsvdict)

                section_key = list(sections)[0]

                # Add key to the Y-axis of spreadsheet from dict...
                sectionrow[0] = self.add_csv_value(section_key)

                # driven by CFG file, not JSON, so field occurs in CFG file first...
                # e.g. IE, REPRESENTATION, FILE, then each field in each of those...
                for field in sections[section_key]:
                    # store for record level handling like provenance
                    if field == "Archway Unique ID (Object Identifier)":
                        self.rnumber = item["Item Code"]

                    # if we have a matching field in the cfg, and json, populate it...
                    if field == self.rosettacsvdict[csvindex]["name"]:
                        self.populaterows(
                            field, item, sectionrow, csvindex, self.rnumber
                        )
                    else:
                        logger.error(
                            "field in config: '%s' is not aligned with JSON schema '%s'",
                            field,
                            self.rosettacsvdict[csvindex]["name"],
                        )
                        sys.exit(1)

                    # increment csvindex along the x-axis...
                    csvindex += 1

                itemrow.append(sectionrow)
            fields.append(itemrow)
            csvindex = csv_index_start

        return self.csvstringoutput(fields)

    def listduplicates(self):
        """List duplicates discovered running this script."""
        seen = []
        dupe = []
        for row in self.droidlist:
            cs = ""
            if "MD5_HASH" in row:
                cs = row["MD5_HASH"]
            elif "SHA1_HASH" in row:
                cs = row["SHA1_HASH"]
            elif "SHA256_HASH" in row:
                cs = row["SHA256_HASH"]
            elif "SHA512_HASH" in row:
                cs = row["SHA512_HASH"]
            else:
                logging.error("no hash available to use in DROID export")
                sys.exit(1)
            if cs not in seen:
                seen.append(cs)
            else:
                dupe.append(cs)
        return set(dupe)

    def read_export_csv(self):
        """Read a list control CSV."""
        if self.exportsheet is not False:
            csvhandler = GenericCSVHandler()
            exportlist = csvhandler.csv_as_list(self.exportsheet)
            return exportlist

    def read_droid_csv(self):
        """Read a DROID CSV."""
        if self.droidcsv is not False:
            droidcsvhandler = DroidCSVHandler()
            droidlist = droidcsvhandler.read_droid_csv(self.droidcsv)
            droidlist = droidcsvhandler.remove_folders(droidlist)
            return droidcsvhandler.remove_container_contents(droidlist)

    def export_to_rosetta_csv(self):
        """Convert a list control and droid sheet to a Rosetta CSV."""
        if self.droidcsv is not False and self.exportsheet is not False:
            self.droidlist = self.read_droid_csv()
            self.exportlist = self.read_export_csv()
            if self.prov is True:
                provhandler = ProvenanceCSVHandler()
                self.provlist = provhandler.read_provenance_csv(self.provfile)
                if self.provlist is None:
                    self.prov = False
            self.duplicates = self.listduplicates()
            return self.create_rosetta_csv()
