# ************ Utility ************

"""
In a csv files stores date and value for selected utilities
Opens csv file (Default: utilities.csv)
Prompts the user for the new values
Returns:
    Tab with updated values
    Everage dayly use in the last period
    Comparison with previous period
Save the new values sorted by date in the csv file (Default: utilities.csv)
"""

# Importing all the required libraries.

import argparse
import csv
from datetime import date
import inflect
from pathlib import Path as path
import re
import sys
from tabulate import tabulate

i = inflect.engine()

# Set Constant Variables.

D = "Date"
E = "\x1b[38;5;9;1mElectricity\x1b[0m"
G = "\x1b[38;5;11;1mGas\x1b[0m"
W = "\x1b[38;5;14;1mWater\x1b[0m"


# Creating classes.

# Class containing reading values.

class Utilities:
    
    def __init__(self, values={}, ukeys={}, entries=0):
        self.values = values
        self.ukeys = ukeys
        self.entries = entries

    def __str__(self):
        tab = []
        
        for row in self.values:
            tab.append(self.values[row])
        
        return f"\nUtilities\n{tabulate(tab, headers='keys', tablefmt='pretty')}\n\x1b[38;5;208;1mValues in orange are estimated\x1b[0m\n"

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        self._values = values
        ...

    @property
    def ukeys(self):
        return self._ukeys

    @ukeys.setter
    def ukeys(self, ukeys):
        self._ukeys = ukeys
        ...

    @property
    def entries(self):
        return self._entries

    @entries.setter
    def entries(self, entries):
        self._entries = entries
        ...

    @classmethod
    def read(cls, csvfile):
        n = 0
        verbose = 1
        ukeys = {
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
        values = {n: {}}
        
        try:
            with open(csvfile) as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    val = {}
                    
                    for key in ukeys.keys():
                        if key in row.keys():
                            val[key] = row[key]
                        elif key == E:
                            val[key] = row["Electricity"]
                        elif key == G:
                            val[key] = row["Gas"]
                        elif key == W:
                            val[key] = row["Water"]
                        else:
                            val[key] = ""
                    
                    v = {n: val}
                    values.update(v)
                    n += 1

# Get the numbers of entries in the csv file.

            entries = len(values)  
            
            if values == {0: {}}:
                verbose = 0
                raise FileNotFoundError
            else:
                pass  # return cls(values, ukeys, entries)
        
        except FileNotFoundError:
            
            if verbose != 0:
                print(
                    f"\n\x1b[38;5;2mThe file \x1b[4m{csvfile}\x1b[0m\x1b[38;5;2m has been created\x1b[0m"
                )
            ukeys = {
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
            values.update(
                {
                    0: {
                        D: str(date.today()),
                        "days": "",
                        E: "0",
                        "kWh": "",
                        "kWh/d": "",
                        "eT": "",
                        G: "0",
                        "m3": "",
                        "m3/d": "",
                        "gT": "",
                        W: "0",
                        "kL": "",
                        "kL/d": "",
                        "wT": "",
                    }
                }
            )
            entries = 0

        return cls(values, ukeys, entries)

    @classmethod
    def update(cls, self, readings=None):
        values = self.values
        ukeys = self.ukeys
        entries = self.entries
        
        if readings == None:
            pass
        else:
            values.update({entries: readings})
        
        entries = len(values)
        new = []
        
        if entries > 1:
            
            for l in range(entries):
                new.append(values[l])
            sorted_ut = sorted(new, key=lambda k: k[D])
            n = 0
            
            for row in sorted_ut:
                dr = {n: row}
                values.update(dr)
                n += 1
        
        return cls(values, ukeys, entries)

    @classmethod
    def write(cls, self, csvfile):
        
        with open(csvfile, "w") as file:
            writer = csv.DictWriter(file, self.ukeys)
            file = csv.DictWriter.writeheader(writer)
            
            for row in self.values:
                writer.writerow(self.values[row])

# Class for the duration.

class Duration:
    
    def __init__(self, total=0, years=0, last=0):
        self.total = total
        self.years = years
        self.last = last

    def __str__(self):
        t = f"{self.total} {i.plural('day', self.total)}"
        y = f"{self.years} {i.plural('year', self.years)}"
        l = f"{self.last} {i.plural('day', self.last)}"
        
        if self.years < 1:
            p = l
            pass
        elif self.last < 1:
            p = y
            pass
        else:
            p = f"{y} and {l}"
        
        return f"\nTotal duration: {p} ({t})"

    @classmethod
    def time(cls, utilities):
        total = period(
            utilities.values.get(0)[D],
            utilities.values.get(utilities.entries - 1)[D],
        )
        years = int(total / 365)
        last = total % 365
        
        return cls(total, years, last)


# Main function.

def main():

# Set the optional arguments.
    
    parser = argparse.ArgumentParser(description="This program read and write set of readings of utilities (Electricity, Gas, Water) from the default utilities.csv file")
    parser.add_argument(
        "-f",
        "--file",
        default="utilities.csv",
        help="run the program on the given csv file",
        type=str,
    )
    parser.add_argument(
        "-m",
        "--merge",
        nargs=2,
        help="merge two sets of readings from two csv files",
        type=str,
    )
    parser.add_argument(
        "-p",
        "--print",
        help="print the list of readings, ordered by date, from a given csv file",
        type=str,
    )
    parser.add_argument("-s", "--save", help="set a new csv output file")
    args = settings(parser.parse_args())

 # Read the the csv file.

    utilities = Utilities.read(args.file)
 
 # Ask the user for the new readings.
 
    readings = {}

# Input date of new readings.

    while True:

        try:
            print()
            readings[D] = date_check(input("Date of new readings (YYYY-MM-DD): "))
            print(f"\x1b[19C\x1b[1A: {readings[D]}", " " * 20)

        except ValueError as ve:
            print(ve)
            pass
        else:
            break

    keys = utilities.ukeys

# Input new readings for all the utilities.

    force = None
    
    for key in keys:
    
        if key == D:
            pass
        elif key in [E, G, W]:
            
            while True:
                try:
                    ir = input(f"{key}:\x1b[{20 - len(de(key))}C")
                    
                    if ir == "" and force != None:
                        ir = int(force)
                        print("\x1b[19C", "\x1b[1A", ir)
                        force = True
                    elif ir == "":
                        readings[key] = estimate(utilities, readings[D], key)
                        print("\x1b[19C", "\x1b[1A", readings[key])
                    else:
                        readings[key] = int(ir)
                    
                    if force == True:
                        pass
                    else:
                        force = check_readings(utilities, readings[D], int(de(readings[key])), key)
                    
                    if force == True:
                        force = None
                        break
                    else:
                        pass
                
                except (ValueError):
                    print("\x1b[38;5;160mValue should be an integer!\x1b[0m")
        
        else:
            readings[key] = ""
    
    if check_doubles(
        
# Check if there is alreading a reading for the input data.
        
        utilities, readings
    ):
        utilities = Utilities.update(
            utilities, readings
        )

# Print the table of the utilities updated with new readings.

    print(output(utilities, args.save))


# Return the table of utilities and save the data in a csv file.

def output(utils, file):
    
    if utils.entries < 2:
        dur = f"\n"
        pass
    else:
        duration = Duration.time(utils)
        dur = f"{duration}\n\n"
    
    utilities = statistics(utils)
    utilities.write(utilities, file)
    
    return f"{dur}Final\x1b[6C\x1b[1A\n{utilities}"


# Parse the argument given with the filename.

def settings(args):

# Print a table from the data in the argument file.

    if args.print != None:

        if re.search(r"^.+\.csv$", args.print):
        
            if path(args.print).is_file():
                utilities = Utilities.update(Utilities.read(args.print))
                print(utilities)
            else:
                print(
                    f"\n\x1b[38;5;160mThe file \x1b[4m{args.print}\x1b[0m\x1b[38;5;160m does not exist!\x1b[0m",
                    end="\n" * 2,
                )
        
        else:
            print(
                "\n\x1b[38;5;160m" + "Only csv files can be printed" + "\x1b[0m",
                end="\n" * 2,
            )
        
        sys.exit()

# Save the results to the argument file.

    if args.save != None:

        if re.search(r"^.+\.csv$", args.save):
            pass
        else:
            print(
                "\n\x1b[38;5;160m" + "This program can save only csv files" + "\x1b[0m",
                end="\n" * 2,
            )
            args.save = check_csv(args.save, "overwrite")

# Merge the argument files to a new file and print the new table.

    if args.merge != None:
        ut = {}
        er = []
        
        for f in range(2):
            
            if re.search(r"^.+\.csv$", args.merge[f]):
                
                if path(args.merge[f]).is_file():
                    
                    if Utilities.read(args.merge[f]) != {}:
                        pass
                
                else:
                    er = er + [f"{args.merge[f]}"]
            
            else:
                print(
                    "\n\x1b[38;5;160m" + "Only csv files can be merged" + "\x1b[0m",
                    end="\n" * 2,
                )
                args.merge[f] = check_csv(args.merge[f], "merge")
                print(end="\n" * (f + 1))
        
        if er != []:
            l = len(er)
            err = i.join(er)
            print(
                f"\n\x1b[38;5;160mThe {i.plural('file',l)} \x1b[4m{err}\x1b[0m\x1b[38;5;160m {i.plural_verb('does',l)} not exist!\x1b[0m",
                end="\n" * 2,
            )
            sys.exit()
        else:
            print(merge(Utilities.read(args.merge[0]), Utilities.read(args.merge[1]), args.save))
            sys.exit()

# Open the argument file.

    if re.search(r"^.+\.csv$", args.file):
        pass
    else:
        print(
            "\n\x1b[38;5;160m" + "This program works only with csv files" + "\x1b[0m",
            end="\n" * 2,
        )
        args.file = check_csv(args.file, "open")
    
    if args.save == None:
        args.save = args.file
    return args

# Check if a csv file already exist with given argument name.

def check_csv(name, act):

    m = re.match(r"([a-zA-Z0-9_]+)(\.[a-zA-Z0-9_]+)*?", name)
    name = m.group(1) + ".csv"
    print(f"Checking for the existence of the file \x1b[4m{name}\x1b[0m...\n")
    
    if path(name).is_file():
        say = f"File \x1b[4m{name}\x1b[0m already exist! Do you want to {act} it?"
    else:
        
        if act == "merge":
            print(f"File \x1b[4m{name}\x1b[0m do not exist!\n")
            sys.exit()
        
        say = f"\x1b[38;5;216mDo you want to create the file \x1b[4m{name}\x1b[0m\x1b[38;5;216m?"
    
    if input(f"{say} \x1b[7m[y/n]\x1b[0m ") == "y":
        return name
    else:
        print()
        sys.exit()


# Check the format and validity of the given date.

def date_check(d):

    if d == "":
        d = str(date.today())
        print("\x1b[19C", "\x1b[1A", d)
        return d
    else:
        ec = 0

        try:
            od = ordinal(d)

            if od > (date.today()).toordinal():
                ec = 1

                raise ValueError(
                    "\n\x1b[38;5;216m"
                    + f"Today is {date.today()}\n"
                    + "Readings cannot be in the future!"
                    + "\x1b[0m"
                )

            elif od < 683369:  # This number correspond to 1872-01-01.
                ec = 2

                raise ValueError(
                    "\n\x1b[38;5;216m"
                    + "The earliest meter was patented by Samuel Gardiner in 1872."
                    + "\nThere cannot be measurement before that date!"
                    + "\x1b[0m"
                )

            else:
                return d

        except ValueError as ve:

            if ec != 0:
                raise ValueError(ve)
            else:
                raise ValueError(
                    "\n\x1b[38;5;160m"
                    + "Date should be in the YYYY-MM-DD format."
                    + "\x1b[0m"
                )


# Calculate an estimate value for the key reading.

def estimate(utilities, rdate, key):

    if utilities.entries == 0:
        return "\x1b[38;5;208;1m0\x1b[0m"

    r = utilities.entries - 1

    if r < 7:
        fqu = r - 1
        lqu = r - 1
    else:
        fqu = 6
        lqu = 6

    fq = utilities.values[0 + fqu]
    lq = utilities.values[r - lqu]
    t = utilities.values[r]

    for l in range(utilities.entries):
        u = utilities.values[l]

        if l == 0:
            b = u
        else:
            b = utilities.values[l - 1]

        if rdate <= b[D]:
            td = period(b[D], fq[D])

            if td == 0:
                td = 1

            e = (int(de(fq[key])) - int(de(b[key]))) / td
            d = period(rdate, b[D])

            if d == 0:
                d = 1

            rkey = str(int(de(b[key])) - int(e * d))
            return "\x1b[38;5;208;1m" + rkey + "\x1b[0m"

        elif b[D] < rdate <= u[D]:

            if u[D] < t[D]:
                ul = utilities.values[l + 1]
            else:
                ul = u

            td = period(b[D], ul[D])

            if td == 0:
                td = 1

            e = (int(de(ul[key])) - int(de(b[key]))) / td
            d = period(b[D], rdate)
            rkey = str(int(de(b[key])) + int(e * d))
            return "\x1b[38;5;208;1m" + rkey + "\x1b[0m"

        elif rdate >= t[D]:
            td = period(lq[D], t[D])

            if td == 0:
                td = 1
            e = (int(de(t[key])) - int(de(lq[key]))) / td
            d = period(t[D], rdate)

            if d == 0:
                d = 1

            rkey = str(int(de(t[key])) + int(e * d))
            return "\x1b[38;5;208;1m" + rkey + "\x1b[0m"

        else:
            pass


# Check the validity of the input readings.

def check_readings(utilities, rdate, rkey, key):

    if utilities.entries == 0:
        return True
    
    r = utilities.entries - 1
    t = utilities.values[r]
    
    for l in range(utilities.entries):
        u = utilities.values[l]
    
        if l == 0:
            b = u
        else:
            b = utilities.values[l - 1]
    
        if rdate < b[D]:
    
            if rkey <= int(de(b[key])):
                return True
            else:
                print(
                    "Entry for",
                    key,
                    "\x1b[0m" + "on" + "\x1b[38;5;216m",
                    rdate,
                    "\x1b[0m" + "should be lower than" + "\x1b[38;5;216;1m",
                    u[key],
                    "\x1b[0m" + "\nTo force" + "\x1b[38;5;216;1m",
                    rkey,
                    "\x1b[0m" + "as value, press ENTER"
                )
                return rkey
    
        elif b[D] <= rdate < u[D]:
    
            if int(de(b[key])) <= rkey <= int(de(u[key])):
                return True
            else:
                print(
                    "Entry for",
                    key,
                    "\x1b[0m" + "on" + "\x1b[38;5;216m",
                    rdate,
                    "\x1b[0m" + "should be between" + "\x1b[38;5;216;1m",
                    b[key],
                    "\x1b[0m" + "and" + "\x1b[38;5;216;1m",
                    u[key],
                    "\x1b[0m" + "\nTo force" + "\x1b[38;5;216;1m",
                    rkey,
                    "\x1b[0m" + "as value, press ENTER."
                )
                return rkey
    
        elif rdate == u[D]:
    
            if rkey >= int(de(b[key])):
                return True
            else:
                print(
                    "Entry for",
                    key,
                    "\x1b[0m" + "on" + "\x1b[38;5;216m",
                    rdate,
                    "\x1b[0m" + "should be higher than" + "\x1b[38;5;216;1m",
                    b[key],
                    "\x1b[0m" + "\nTo force" + "\x1b[38;5;216;1m",
                    rkey,
                    "\x1b[0m" + "as value, press ENTER."
                )
                return rkey
    
        elif rdate > t[D]:
    
            if rkey >= int(de(t[key])):
                return True
            else:
                print(
                    "Entry for",
                    key,
                    "\x1b[0m" + "on" + "\x1b[38;5;216m",
                    rdate,
                    "\x1b[0m" + "should be higher than" + "\x1b[38;5;216;1m",
                    t[key],
                    "\x1b[0m" + "\nTo force" + "\x1b[38;5;216;1m",
                    rkey,
                    "\x1b[0m" + "as value, press ENTER."
                )
                return rkey
    
        else:
            pass
    
    return True


# Check if there are other readings for that date.

def check_doubles(utilities, reads):

    for l in range(utilities.entries):
        u = utilities.values[l]

        if reads[D] == u[D]:
            print(
                "\n\x1b[38;5;196m",
                "There is already a reading for",
                "\x1b[48;5;11m",
                reads[D],
                "\x1b[0m",
            )
            old = ["Old"]
            new = ["New"]

            for val in u.values():
                old.append(val)

            for val in reads.values():
                new.append(val)

            print(tabulate((old, new), headers=utilities.ukeys, tablefmt="pretty"))
            print(
                "\x1b[38;5;196m",
                "Would you like to overwrite it?",
                "\x1b[48;5;196m",
                "[y/n]",
                "\x1b[0m",
                end="",
            )

            if input(" ") == "y":
                utilities.values[l] = reads
                return False
            else:
                return False

        else:
            pass

    return True


# Calculate days between two dates.

def period(start, last):
    return ordinal(last) - ordinal(start)


# Convert the date from yyyy-mm-dd format to an ordinal number.

def ordinal(iso):
    return (date.fromisoformat(iso)).toordinal()


# Calculate some basic statistics on the readings.

def statistics(utils):

    for l in range(utils.entries):
        u = utils.values[l]

        if l == 0:
            b = u
        else:
            b = utils.values[l - 1]

        u["days"] = period(b[D], u[D])
        u["kWh"] = int(de(u[E])) - int(de(b[E]))
        u["m3"] = int(de(u[G])) - int(de(b[G]))
        u["kL"] = int(de(u[W])) - int(de(b[W]))

        if u["days"] == 0:
            u["kWh/d"] = u["eT"] = u["m3/d"] = u["gT"] = u["kL/d"] = u["wT"] = "N/A"
        else:
            u["kWh/d"] = "{:.2f}".format(u["kWh"] / u["days"])
            u["eT"] = trend(u["kWh/d"], b["kWh/d"])
            u["m3/d"] = "{:.2f}".format(u["m3"] / u["days"])
            u["gT"] = trend(u["m3/d"], b["m3/d"])
            u["kL/d"] = "{:.2f}".format(u["kL"] / u["days"])
            u["wT"] = trend(u["kL/d"], b["kL/d"])

        for key in utils.ukeys:
            u[key] = str(u[key])

    return utils


# Calculate the variance from the previous period.

def trend(u, b):

    try:
        s = ""
        u = float(u)
        b = float(b)
        p = ((u - b) / b) * 100
        limit = 5

        if float(p) >= limit:
            col = 9
            x = "{:.1f}"
        elif -limit < float(p) < limit:
            col = 221
            x = "{:.2f}"
        elif float(p) <= -limit:
            col = 10
            x = "{:.1f}"

        if float(p) > 0:
            s = "+"

        return f"\x1b[38;5;{col}m{s}{x.format(p)}%\x1b[0m"

    except (ValueError, ZeroDivisionError):
        return "\x1b[38;5;221mN/A\x1b[0m"


# Return unformated value for a reading.

def de(n):

    if matches := re.search(
        r"^(?:\x1b\[[0-9]{1,3};[0-9]{1,3};[0-9]{1,3}(?:;[0-1])?m)?([0-9a-zA-Z-+=./%]*)(?:\x1b\[0m)?$",
        str(n),
    ):
        return matches.group(1)


# Merge two sets of readings from two csv files.

def merge(a, b, save):

    if save == None:
        save = "merged.csv"

    for row in b.values:

        if check_doubles(a, b.values[row]):
            a = Utilities.update(a, b.values[row])
        else:
            pass

    return output(a, save)


if __name__ == "__main__":
    main()
