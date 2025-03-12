"""Rosetta CSV generator tests.

An original test from the first iteration of this code hence its dated
look.
"""

# pylint: disable=R0914

import io

from src.anz_rosetta_csv.rosetta_csv_generator import RosettaCSVGenerator


def test_normalize_spaces(mocker):
    """Test spaces are normalized correctly."""

    placeholder_config = io.StringIO("")
    mocker.patch.object(RosettaCSVGenerator, "read_rosetta_schema")

    rosetta_csv_gen = RosettaCSVGenerator(False, False, False, placeholder_config)

    # 1
    case_blank_two_spaces = "  "
    result_blank_two_spaces = " "

    # 2
    case_words_two_spaces = "one  two"
    result_words_two_spaces = "one two"

    # 3
    case_words_three_spaces = "one   two"
    result_words_three_spaces = "one two"

    # 4
    case_multiple_words_spaces = "one  two  three"
    result_multiple_words_spaces = "one two three"

    # 5
    case_filename_xls = "001 SPREADSHEET  FILE.xls"
    result_filename_xls = "001 SPREADSHEET FILE.xls"

    # 5
    case_filename_doc = "001       DOCUMENT        FILE.xls"
    result_filename_doc = "001 DOCUMENT FILE.xls"

    # 7
    case_nospace = "word"
    result_nospace = "word"

    # 8
    case_onespace = "word space"
    result_onespace = "word space"

    assert (
        rosetta_csv_gen.normalize_spaces(case_blank_two_spaces)
        == result_blank_two_spaces
    )
    assert (
        rosetta_csv_gen.normalize_spaces(case_words_two_spaces)
        == result_words_two_spaces
    )
    assert (
        rosetta_csv_gen.normalize_spaces(case_words_three_spaces)
        == result_words_three_spaces
    )
    assert (
        rosetta_csv_gen.normalize_spaces(case_multiple_words_spaces)
        == result_multiple_words_spaces
    )
    assert rosetta_csv_gen.normalize_spaces(case_filename_xls) == result_filename_xls
    assert rosetta_csv_gen.normalize_spaces(case_filename_doc) == result_filename_doc
    assert rosetta_csv_gen.normalize_spaces(case_nospace) == result_nospace
    assert rosetta_csv_gen.normalize_spaces(case_onespace) == result_onespace


def test_compare_filenames_as_titles(mocker):
    """Test that filenames are compared correctly."""
    placeholder_config = io.StringIO("")
    mocker.patch.object(RosettaCSVGenerator, "read_rosetta_schema")
    rosetta_csv_gen = RosettaCSVGenerator(False, False, False, placeholder_config)

    # Standard true comparison, expected result
    case_comparison_no_dot = {
        "STATUS": "Done",
        "MIME_TYPE": "application/msword",
        "NAME": "FILENAME",
        "PUID": "fmt/1",
    }  # truncated dict
    result_comparison_no_dot = "FILENAME"

    # Standard true comparison, expected result
    case_comparison_dot = {
        "STATUS": "Done",
        "MIME_TYPE": "application/msword",
        "NAME": "NEWFILENAME.DOC",
        "PUID": "fmt/1",
    }
    result_comparison_dot = "NEWFILENAME"

    # False result: Checks that stipping of extension happens
    case_false_result = {
        "STATUS": "Done",
        "MIME_TYPE": "application/msword",
        "NAME": "FALSENAME.DOC",
        "PUID": "fmt/1",
    }
    result_false_result = "FALSENAME.DOC"

    # Multiple dots should only see removal of one
    case_multiple_dots = {
        "STATUS": "Done",
        "MIME_TYPE": "application/msword",
        "NAME": "MANY.EXT.EXT.DOC",
        "PUID": "fmt/1",
    }
    result_multiple_dots = "MANY.EXT.EXT"

    # TRUE tests
    assert (
        rosetta_csv_gen.compare_filenames_as_titles(
            case_comparison_no_dot, result_comparison_no_dot
        )
        is True
    )
    assert (
        rosetta_csv_gen.compare_filenames_as_titles(
            case_comparison_dot, result_comparison_dot
        )
        is True
    )
    assert (
        rosetta_csv_gen.compare_filenames_as_titles(
            case_multiple_dots, result_multiple_dots
        )
        is True
    )

    # FALSE tests
    assert (
        rosetta_csv_gen.compare_filenames_as_titles(
            case_false_result, result_false_result
        )
        is False
    )
