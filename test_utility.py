"""
Test for utility
"""


#   importing libraries
import argparse
from datetime import date
from pathlib import Path as path
import pytest
from tabulate import tabulate
from unittest.mock import patch


#   importing Classes from utility.py
from utility import Duration
from utility import Utilities

#   importing functions from utility.py
from utility import output
from utility import settings
from utility import check_csv
from utility import date_check
from utility import estimate
from utility import check_readings
from utility import check_doubles
from utility import period
from utility import ordinal
from utility import statistics
from utility import trend
from utility import de
from utility import merge


#   removing any preexisting test files
for pp in ["test.csv", "merged.csv"]:
    p = path(pp)
    p.unlink(missing_ok=True)


#   set up Constants
D = "Date"
E = "\x1b[38;5;9;1mElectricity\x1b[0m"
G = "\x1b[38;5;11;1mGas\x1b[0m"
W = "\x1b[38;5;14;1mWater\x1b[0m"
UT_0 = Utilities.read("ut_0_test.csv")  #   empty csv file
UT_1 = Utilities.read("ut_1_test.csv")  #   1 entry, values = 0
UT_2 = Utilities.read("ut_2_test.csv")  #   2 entries
UT_A = Utilities.read("ut_a_test.csv")  #   entries set a
UT_B = Utilities.read("ut_b_test.csv")  #   entries set b
UT_E = Utilities.read("ut_e_test.csv")  #   several entries
UT_MA = Utilities.read("ut_ma_test.csv")  #   merged UT_A and UT_B no overwrite
UT_MB = Utilities.read("ut_mb_test.csv")  #   merged UT_A and UT_B overwrite doubles
UT_R = Utilities.read("ut_r_test.csv")  #   raw readings no statitstics
UT_S = Utilities.read("ut_s_test.csv")  #   statistics on ut_r_test.csv


#   set up utilities
utilities = Utilities()
utilities.ukeys = {
    D: "Date",
    "days": "days",
    E: "Electricity",
    "kWh": "kWh",
    "kWh/d": "kWh/d",
    "eT": "eT",
    G: "Gas",
    "m3": "m3",
    "m3/d": "m3/d",
    "gT": "gT",
    W: "Water",
    "kL": "kL",
    "kL/d": "kL/d",
    "wT": "wT",
}
utilities.values = {
    0: {
        D: "2022-08-01",
        "days": "0",
        E: "0",
        "kWh": "0",
        "kWh/d": "N/A",
        "eT": "N/A",
        G: "0",
        "m3": "0",
        "m3/d": "N/A",
        "gT": "N/A",
        W: "0",
        "kL": "0",
        "kL/d": "N/A",
        "wT": "N/A",
    }
}
utilities.entries = 1


""" start testing   """


#   testing Classes
#   testing Class Duration
def test_Duration():
    dur = Duration.time(UT_2)
    assert dur.total == 31
    assert dur.years == 0
    assert dur.last == 31
    dur = Duration.time(UT_A)
    assert dur.total == 180
    assert dur.years == 0
    assert dur.last == 180
    dur = Duration.time(UT_E)
    assert dur.total == 225
    assert dur.years == 0
    assert dur.last == 225
    dur = Duration.time(UT_R)
    assert dur.total == 2716
    assert dur.years == 7
    assert dur.last == 161


def test_Duration_str():
    assert str(Duration.time(UT_2)) == f"\nTotal duration: 31 days (31 days)"
    assert str(Duration.time(UT_A)) == f"\nTotal duration: 180 days (180 days)"
    assert str(Duration.time(UT_E)) == f"\nTotal duration: 225 days (225 days)"
    assert (
        str(Duration.time(UT_R))
        == f"\nTotal duration: 7 years and 161 days (2716 days)"
    )


#   testing Class Utilities
def test_Utilities_read():
    assert Utilities.read("ut_1_test.csv").values == utilities.values
    assert Utilities.read("ut_1_test.csv").ukeys == utilities.ukeys
    assert Utilities.read("ut_1_test.csv").entries == utilities.entries


def test_Utilities_write():
    utilities.write(utilities, "test.csv")
    with path("test.csv") as p:
        assert p.is_file() == True
    ut = Utilities.read("test.csv")
    assert ut.values == UT_1.values
    assert ut.ukeys == UT_1.ukeys
    assert ut.entries == UT_1.entries
    p.unlink(missing_ok=True)


@patch("builtins.print")
def test_Utilities_str(mock_print):
    print(utilities)
    mock_print.assert_called_with(utilities)


#   testing functions
#   testing output() for a csv file with only one entry
def test_output_one_entry():
    assert output(utilities, "test.csv") == f"\nFinal\x1b[6C\x1b[1A\n{UT_1}"
    with path("test.csv") as p:
        assert p.is_file() == True
    p.unlink(missing_ok=True)


#   testing output() for a csv file with more than one entry
def test_output():
    utilities.values.update(
        {
            1: {
                D: "2022-09-01",
                "days": "31",
                E: "100",
                "kWh": "100",
                "kWh/d": "3.23",
                "eT": "\x1b[38;5;221mN/A\x1b[0m",
                G: "100",
                "m3": "100",
                "m3/d": "3.23",
                "gT": "\x1b[38;5;221mN/A\x1b[0m",
                W: "100",
                "kL": "100",
                "kL/d": "3.23",
                "wT": "\x1b[38;5;221mN/A\x1b[0m",
            }
        }
    )
    utilities.entries = 2
    duration = Duration.time(UT_2)
    assert output(utilities, "test.csv") == f"{duration}\n\nFinal\x1b[6C\x1b[1A\n{UT_2}"
    with path("test.csv") as p:
        assert p.is_file() == True
    p.unlink(missing_ok=True)


#   setting up parser for the test of settings()
parser = argparse.ArgumentParser(description="Utilities usage")
parser.add_argument(
    "-f",
    "--file",
    default="utilities.csv",
    help="run the program on a given csv file",
    type=str,
)
parser.add_argument(
    "-p",
    "--print",
    help="print the list of readings, ordered by date, from a given csv file",
    type=str,
)
parser.add_argument(
    "-m",
    "--merge",
    nargs=2,
    help="merge two sets of readings from two csv files",
    type=str,
)
parser.add_argument("-s", "--save", help="destination file")


#   testing the -f argument
#   valid csv file
def test_settings_f_valid():
    arg_in = "-f ut_0_test.csv".split()
    args = parser.parse_args(arg_in)
    arg_out = "-f ut_0_test.csv -s ut_0_test.csv".split()
    argtest = parser.parse_args(arg_out)
    assert settings(args) == argtest


#   testing for non existing or non csv -f argument
#   answer no to prompt
def test_settings_f_noncsv_no(monkeypatch):
    arg_in = "-f notafile".split()
    args = parser.parse_args(arg_in)
    monkeypatch.setattr("builtins.input", lambda _: "n")
    with pytest.raises(SystemExit):
        settings(args)


#   testing for non existing or non csv -f argument
#   answer yes to prompt
def test_settings_f_noncsv_yes(monkeypatch):
    arg_in = "-f notafile".split()
    args = parser.parse_args(arg_in)
    arg_out = "-f notafile.csv -s notafile.csv".split()
    argtest = parser.parse_args(arg_out)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert settings(args) == argtest


#   testing the -s argument
#   valid csv file
def test_settings_s_valid():
    arg_in = "-s ut_0_test.csv".split()
    args = parser.parse_args(arg_in)
    arg_out = "-f utilities.csv -s ut_0_test.csv".split()
    argtest = parser.parse_args(arg_out)
    assert settings(args) == argtest


#   testing for non csv -s argument
#   answer no to prompt
def test_settings_s_noncsv_no(monkeypatch):
    arg_in = "-s notcsv".split()
    args = parser.parse_args(arg_in)
    monkeypatch.setattr("builtins.input", lambda _: "n")
    with pytest.raises(SystemExit):
        settings(args)


#   testing for non csv -s argument
#   answer yes to prompt
def test_settings_s_noncsv_yes(monkeypatch):
    arg_in = "-s ut_0_test".split()
    args = parser.parse_args(arg_in)
    arg_out = "-f utilities.csv -s ut_0_test.csv".split()
    argtest = parser.parse_args(arg_out)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert settings(args) == argtest


#   testing the -m argument no overwrite
def test_settings_merge_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    with pytest.raises(SystemExit) as excinfo:
        arg_in = "-m ut_a_test.csv ut_b_test.csv".split()
        args = parser.parse_args(arg_in)
        settings(args)
        assert excinfo.value.code == None
    with path("merged.csv") as p:
        assert p.is_file() == True
    assert Utilities.read("merged.csv").values == UT_MA.values
    p.unlink(missing_ok=True)


#   testing the -m argument with overwrite
def test_settings_merge_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    with pytest.raises(SystemExit) as excinfo:
        arg_in = "-m ut_a_test.csv ut_b_test.csv".split()
        args = parser.parse_args(arg_in)
        settings(args)
        assert excinfo.value.code == None
    with path("merged.csv") as p:
        assert p.is_file() == True
    assert Utilities.read("merged.csv").values == UT_MB.values
    p.unlink(missing_ok=True)


#   testing the -m argument with not existing file given
def test_settings_merge_nofile():
    with pytest.raises(SystemExit) as excinfo:
        arg_in = "-m ut_no_a.csv ut_no_b.csv".split()
        args = parser.parse_args(arg_in)
        settings(args)
        assert excinfo.value.code == None
    with path("merged.csv") as p:
        assert p.is_file() == False


#   testing for non existing or non csv arguments
#   answer no to prompt
def test_settings_merge_nocsv_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    with pytest.raises(SystemExit) as excinfo:
        arg_in = "-m ut_0_test ut_2_test".split()
        args = parser.parse_args(arg_in)
        settings(args)
        assert excinfo.value.code == None
    with path("merged.csv") as p:
        assert p.is_file() == False


#   testing for non existing or non csv arguments
#   answer yes to prompt
def test_settings_merge_nocsv_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    with pytest.raises(SystemExit) as excinfo:
        arg_in = "-m ut_0_test ut_2_test".split()
        args = parser.parse_args(arg_in)
        settings(args)
        assert excinfo.value.code == None
    with path("merged.csv") as p:
        assert p.is_file() == True
    assert Utilities.read("merged.csv").values == Utilities.read("ut_2_test.csv").values
    p.unlink(missing_ok=True)


#   testing the creation of a csv file from a given name with different extension
def test_check_csv(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert check_csv("ut_a_test", "merge") == "ut_a_test.csv"
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert check_csv("ut_c_test", "file") == "ut_c_test.csv"


#   testing the interruption of the program
def test_check_csv_error(monkeypatch):
    with pytest.raises(SystemExit):
        check_csv("uta_test", "merge")
    with pytest.raises(SystemExit):
        monkeypatch.setattr("builtins.input", lambda _: "n")
        check_csv("uta_test", "file")
    with pytest.raises(SystemExit):
        monkeypatch.setattr("builtins.input", lambda _: "n")
        check_csv("ut_a_test", "file")


#   testing given date
def test_date_check():
    #   correct format given
    assert date_check("2022-09-14") == "2022-09-14"
    #   today date assigned when [ENTER] given with no entry
    assert date_check("") == str(date.today())


#   testing the error message for wrong date given
def test_date_check_error():
    #   date in the future
    with pytest.raises(ValueError) as ve:
        date_check("2122-01-01")
        assert (
            str(ve.value).strip("ValueError(").strip(")")
            == f"\n\x1b[38;5;216mToday is {date.today()}\nReadings cannot be in the future!\x1b[0m"
        )
    #   date too far in the past
    with pytest.raises(ValueError) as ve:
        date_check("1871-12-31")
        assert (
            str(ve.value).strip("ValueError(").strip(")")
            == f"\n\x1b[38;5;216mThe earliest meter was patented by Samuel Gardiner in 1872.\nThere cannot be measurement before that date!\x1b[0m"
        )
    #   any format different from YYYY-MM-DD
    with pytest.raises(ValueError) as ve:
        date_check("Today")
        assert (
            str(ve.value).strip("ValueError(").strip(")")
            == f"\n\x1b[38;5;160mDate should be in the YYYY-MM-DD format.\x1b[0m"
        )


#   testing the estimated values when [ENTER] given with no entry
def test_estimate():
    #   date before the first reading
    rdate = "2022-01-01"
    assert estimate(UT_E, rdate, E) == "\x1b[38;5;208;1m5\x1b[0m"
    assert estimate(UT_E, rdate, G) == "\x1b[38;5;208;1m4\x1b[0m"
    assert estimate(UT_E, rdate, W) == "\x1b[38;5;208;1m1\x1b[0m"
    #   date between the existing readings
    rdate = "2022-05-12"
    assert estimate(UT_E, rdate, E) == "\x1b[38;5;208;1m660\x1b[0m"
    assert estimate(UT_E, rdate, G) == "\x1b[38;5;208;1m528\x1b[0m"
    assert estimate(UT_E, rdate, W) == "\x1b[38;5;208;1m132\x1b[0m"
    #   date after the last reading
    rdate = "2022-09-16"
    assert estimate(UT_E, rdate, E) == "\x1b[38;5;208;1m1295\x1b[0m"
    assert estimate(UT_E, rdate, G) == "\x1b[38;5;208;1m1036\x1b[0m"
    assert estimate(UT_E, rdate, W) == "\x1b[38;5;208;1m259\x1b[0m"
    #   any date when csv file is empty or non yet created
    assert estimate(UT_0, rdate, E) == "\x1b[38;5;208;1m0\x1b[0m"
    assert estimate(UT_0, rdate, G) == "\x1b[38;5;208;1m0\x1b[0m"
    assert estimate(UT_0, rdate, W) == "\x1b[38;5;208;1m0\x1b[0m"


#   testing the validity of the readings
def test_check_readings():
    #   testing for entries before the first set of recorded readings
    rdate = "2022-01-15"
    assert check_readings(UT_E, rdate, 159, E) == True
    assert check_readings(UT_E, rdate, 127, G) == True
    assert check_readings(UT_E, rdate, 31, W) == True
    assert check_readings(UT_E, rdate, 161, E) == 161
    assert check_readings(UT_E, rdate, 129, G) == 129
    assert check_readings(UT_E, rdate, 33, W) == 33
    #   testing for entries between two sets of recorded readings
    rdate = "2022-08-31"
    assert check_readings(UT_E, rdate, 1064, E) == 1064
    assert check_readings(UT_E, rdate, 851, G) == 851
    assert check_readings(UT_E, rdate, 212, W) == 212
    assert check_readings(UT_E, rdate, 1215, E) == True
    assert check_readings(UT_E, rdate, 972, G) == True
    assert check_readings(UT_E, rdate, 243, W) == True
    assert check_readings(UT_E, rdate, 1286, E) == 1286
    assert check_readings(UT_E, rdate, 1029, G) == 1029
    assert check_readings(UT_E, rdate, 258, W) == 258
    #   testing for entries after the last set of recorded readings
    rdate = "2022-09-16"
    assert check_readings(UT_E, rdate, 1295, E) == True
    assert check_readings(UT_E, rdate, 1036, G) == True
    assert check_readings(UT_E, rdate, 259, W) == True
    assert check_readings(UT_E, rdate, 1284, E) == 1284
    assert check_readings(UT_E, rdate, 1027, G) == 1027
    assert check_readings(UT_E, rdate, 256, W) == 256


#   testing for preexisting values for the date of new readings
def test_check_doubles(monkeypatch):
    ut_e = UT_E
    #   no entries for 2022-08-15
    reads = {
        D: "2022-08-15",
        "days": "",
        E: "1135",
        "kWh": "",
        "kWh/d": "",
        "eT": "",
        G: "908",
        "m3": "",
        "m3/d": "",
        "gT": "",
        W: "227",
        "kL": "",
        "kL/d": "",
        "wT": "",
    }
    assert check_doubles(ut_e, reads) == True
    #   existing values for 2022-08-01
    reads = {
        D: "2022-08-01",
        "days": "",
        E: "1080",
        "kWh": "",
        "kWh/d": "",
        "eT": "",
        G: "860",
        "m3": "",
        "m3/d": "",
        "gT": "",
        W: "220",
        "kL": "",
        "kL/d": "",
        "wT": "",
    }
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert check_doubles(ut_e, reads) == False
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert check_doubles(ut_e, reads) == False
    assert ut_e.values[3] == reads


#   testing the days between to dates
def test_period():
    assert period("2022-08-01", "2022-08-31") == 30


#   testing the ordinal value of a date in YYYY-MM-DD format
def test_ordinal():
    assert ordinal("2000-01-01") == 730120
    assert ordinal("2022-09-08") == 738406
    assert ordinal("2022-09-16") == 738414


#   testing for statistics on given values
def test_statistics():
    assert statistics(UT_R).values == UT_S.values


#   test if values are increasing or decreasing
def test_trend():
    #   test return for valid values
    assert trend(3.51, 4.93) == "\x1b[38;5;10m-28.8%\x1b[0m"
    assert trend(4.00, 4.20) == "\x1b[38;5;221m-4.76%\x1b[0m"
    assert trend(4.86, 4.66) == "\x1b[38;5;221m+4.29%\x1b[0m"
    assert trend(4.39, 3.51) == "\x1b[38;5;9m+25.1%\x1b[0m"
    #   test return for ValueError and ZeroDivisionError
    assert trend("N/A", "N/A") == "\x1b[38;5;221mN/A\x1b[0m"
    assert trend(4.5, "N/A") == "\x1b[38;5;221mN/A\x1b[0m"
    assert trend(4.2, 0) == "\x1b[38;5;221mN/A\x1b[0m"


#   test if a non formatted str is returned
def test_de():
    assert de(125) == "125"
    assert de("55") == "55"
    assert de("\x1b[38;5;10m-28.8%\x1b[0m") == "-28.8%"
    assert de("\x1b[38;5;221m-4.76%\x1b[0m") == "-4.76%"
    assert de("\x1b[38;5;221m+4.29%\x1b[0m") == "+4.29%"
    assert de("\x1b[38;5;9m+25.1%\x1b[0m") == "+25.1%"
    assert de("\x1b[38;5;9mElectricity\x1b[0m") == "Electricity"


#   test if a new file with values from two csv files is created
#   keeping values from first file
def test_merge_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    duration = Duration.time(UT_MA)
    assert merge(UT_A, UT_B, None) == f"{duration}\n\nFinal\x1b[6C\x1b[1A\n{UT_MA}"
    with path("merged.csv") as p:
        assert p.is_file() == True
    p.unlink(missing_ok=True)
    assert (
        merge(UT_A, UT_B, "test.csv") == f"{duration}\n\nFinal\x1b[6C\x1b[1A\n{UT_MA}"
    )
    with path("test.csv") as p:
        assert p.is_file() == True
    p.unlink(missing_ok=True)


#   overwriting values from second file
def test_merge_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    duration = Duration.time(UT_MB)
    assert merge(UT_A, UT_B, None) == f"{duration}\n\nFinal\x1b[6C\x1b[1A\n{UT_MB}"
    with path("merged.csv") as p:
        assert p.is_file() == True
    p.unlink(missing_ok=True)
    assert (
        merge(UT_A, UT_B, "test.csv") == f"{duration}\n\nFinal\x1b[6C\x1b[1A\n{UT_MB}"
    )
    with path("test.csv") as p:
        assert p.is_file() == True
    p.unlink(missing_ok=True)


#   removing any residual test files
for pp in ["test.csv", "merged.csv"]:
    p = path(pp)
    p.unlink(missing_ok=True)
