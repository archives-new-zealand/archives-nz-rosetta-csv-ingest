"""Functions shared with the Collections Import Sheet Generator."""

# pylint: disable=R0903


class ImportSheetGenerator:
    """Import Sheet Generator Class."""

    def get_title(self, title):
        """Return a title from a filename string."""
        return title.rsplit(".", 1)[
            0
        ].rstrip()  # split once at full-stop (assumptuon 'ext' follows)
        
        # for processing transfers where the record name provided is full file name WITH file extension: 
        # 1) un-comment the line below (starts with "return title.rstrip()") and 
        # 2) comment-out 3 lines above (starting with "return")
        # return title.rstrip()  # split once at full-stop (assumptuon 'ext' follows)

