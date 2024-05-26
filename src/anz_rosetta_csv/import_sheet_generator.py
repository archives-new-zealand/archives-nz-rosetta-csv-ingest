"""Functions shared with the Collections Import Sheet Generator."""

# pylint: disable=R0903


class ImportSheetGenerator:
    """Import Sheet Generator Class."""

    def get_title(self, title):
        """Return a title from a filename string."""
        return title.rsplit(".", 1)[
            0
        ].rstrip()  # split once at full-stop (assumptuon 'ext' follows)
