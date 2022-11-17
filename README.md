# UTILITY
#### Video Demo: <https://youtu.be/mjHiKE__H6k>
#### Description:

Utility is a simple program to keep record of common utilities (<b>Electricity</b>, <b>Gas</b>, and <b>Water</b>).<br/>
For years I recorded my utilities in excel. It sounds easy, but to get some insight on the usage of those utilities it was not sufficient to record the values. Every time I had to copy-past the functions for any new readings, and anytime I had to manually record the data in chronological order, that means that for any reading on a date between two already recorded I had to insert lines, copy functions, insert values, and finally get the results.<br/>
With Utility I just start the program, insert the date, the readings... <b>Done!</b> On the screen is a table with my data in chronological order showing the daily and average usage of every utilities.
The program does all the work for me. It puts my readings in chronological order, checks for double recordings, checks the validity of my data, and finally save everything in a CSV file, and as already mentioned print an easy to read table.

#### Usage:

There are two ways of running the program
- [default mode](https://github.com/scalvaruso/utility#default-mode)
- [advanced mode](https://github.com/scalvaruso/utility#advanced-mode)
<br/>

The [default mode](https://github.com/scalvaruso/utility#default-mode) runs the program with the default settings, reading and writing the data from the default file `utilities.csv`.<br/>
The [advanced mode](https://github.com/scalvaruso/utility#advanced-mode) allows to specify the origin file and the destination file, to merge two existing files to a new one, or simply to print a table from a specific file.<br/>


#### Default mode:

To use the <font color=blue><b>default mode</b></font> simply type `python utility.py`.<br/>
The program will prompt the user asking for the date of the new readings in the format YYYY-MM-DD
```
python utility.py
Date of new readings (YYYY-MM-DD): █
```
You will receive an error message and prompt back if you will insert a date
from a remote past (1801-11-07)[^battery]

[^battery]: On 7 November 1801, The Italian physicist Alessandro Volta (1745-1827) displays his newly invented battery to Napoleon (1769-1821) at Institut de France in Paris.

```
Date of new readings (YYYY-MM-DD): 1801-11-07

The earliest meter was patented by Samuel Gardiner in 1872.
There cannot be measurement before that date!

Date of new readings (YYYY-MM-DD): █
```
a date from the future (2063-04-05)[^warp]

[^warp]: On 5 April 2063, in "Star Trek: First Contact" humans succeed in their first warp 1 flight and have the first open contact with Vulcans in Bozeman, Montana.

```
Date of new readings (YYYY-MM-DD): 2063-04-05

Today is 2022-10-17
Readings cannot be in the future!

Date of new readings (YYYY-MM-DD): █
```
or a date in a format different from the one requested
```
Date of new readings (YYYY-MM-DD): Today

Date should be in the YYYY-MM-DD format.

Date of new readings (YYYY-MM-DD): 17/10/2022

Date should be in the YYYY-MM-DD format.

Date of new readings (YYYY-MM-DD): █
```
Once inserted a valid date you will be prompted to input the readings for each of the utilities
```
Date of new readings: 2022-10-17
Electricity:          █
```
The program will check for the validity of your entry, re-prompting you in case of a non valid value
or proceeding to the following reading if acceptable
```
Date of new readings: 2022-10-17
Electricity:          NA
Value should be an integer!
Electricity:          █
```
Press `ENTER` without giving any value will make the program to estimate the reading based on those already in the list

```
Electricity:          76582
Gas:                  █
```
In case the value you entered is not consistent with those already recorded (lower than a reading on a previous date, or higher than a reading on a following date) the program will re-prompt you informing you that by pressing again `ENTER` without giving any other value the program will accept your initial number

```
Gas:                  100
Entry for Gas on 2022-10-17 should be higher than 12826
To force 100 as value, press ENTER
Gas:                  █
```
If it was a mistake you can type the right value, and proceed to the next

```
Gas:                  12850
Water:                █
```
When all the values are entered the program will check if there are already readings for the given date and ask if you want to keep the original or the new values[^value].

[^value]: The program records the readings in bulk for all the utilities on the given date,
  if you need to keep some of the original readings you need to choose not to overwrite and run the program again.
```
 There is already a reading for 2022-10-17
+-----+------------+------+-------------+-----+-------+-------+-------+----+------+--------+-------+----+------+-----+
|     |    Date    | days | Electricity | kWh | kWh/d |  eT   |  Gas  | m3 | m3/d |   gT   | Water | kL | kL/d | wT  |
+-----+------------+------+-------------+-----+-------+-------+-------+----+------+--------+-------+----+------+-----+
| Old | 2022-10-17 |  10  |    76578    | 42  | 4.20  | -6.7% | 12848 | 22 | 2.20 | -22.3% | 1982  | 1  | 0.10 | N/A |
| New | 2022-10-17 |      |    76582    |     |       |       | 12850 |    |      |        | 1982  |    |      |     |
+-----+------------+------+-------------+-----+-------+-------+-------+----+------+--------+-------+----+------+-----+
 Would you like to overwrite it? [y/n] █
```

After you answer, the program will add the readings to the existing list, save it in a CSV file and print the final table.

<details>
<summary>Final table</summary>

```
Total duration: 7 years and 328 days (2883 days)

Final
Utilities
+------------+------+-------------+------+-------+--------+-------+------+------+---------+-------+-----+------+---------+
|    Date    | days | Electricity | kWh  | kWh/d |   eT   |  Gas  |  m3  | m3/d |   gT    | Water | kL  | kL/d |   wT    |
+------------+------+-------------+------+-------+--------+-------+------+------+---------+-------+-----+------+---------+
| 2014-11-25 |  0   |    63332    |  0   |  N/A  |  N/A   | 4160  |  0   | N/A  |   N/A   | 1400  |  0  | N/A  |   N/A   |
| 2016-07-28 | 611  |    66194    | 2862 | 4.68  |  N/A   | 6142  | 1982 | 3.24 |   N/A   | 1532  | 132 | 0.22 |   N/A   |
| 2017-04-17 | 263  |    67425    | 1231 | 4.68  | 0.00%  | 6995  | 853  | 3.24 |  0.00%  | 1589  | 57  | 0.22 |  0.00%  |
| 2019-11-15 | 942  |    71835    | 4410 | 4.68  | 0.00%  | 9989  | 2994 | 3.18 | -1.85%  | 1789  | 200 | 0.21 | -4.55%  |
| 2020-01-24 |  70  |    72159    | 324  | 4.63  | -1.07% | 10195 | 206  | 2.94 |  -7.5%  | 1801  | 12  | 0.17 | -19.0%  |
| 2020-02-17 |  24  |    72276    | 117  | 4.88  | +5.4%  | 10288 |  93  | 3.88 | +32.0%  | 1809  |  8  | 0.33 | +94.1%  |
| 2020-03-07 |  19  |    72368    |  92  | 4.84  | -0.82% | 10419 | 131  | 6.89 | +77.6%  | 1818  |  9  | 0.47 | +42.4%  |
| 2020-05-05 |  59  |    72659    | 291  | 4.93  | +1.86% | 10593 | 174  | 2.95 | -57.2%  | 1835  | 17  | 0.29 | -38.3%  |
| 2020-09-14 | 132  |    73122    | 463  | 3.51  | -28.8% | 10698 | 105  | 0.80 | -72.9%  | 1872  | 37  | 0.28 | -3.45%  |
| 2020-10-22 |  38  |    73289    | 167  | 4.39  | +25.1% | 10799 | 101  | 2.66 | +232.5% | 1881  |  9  | 0.24 | -14.3%  |
| 2021-04-01 | 161  |    74184    | 895  | 5.56  | +26.7% | 11570 | 771  | 4.79 | +80.1%  | 1897  | 16  | 0.10 | -58.3%  |
| 2021-04-28 |  27  |    74312    | 128  | 4.74  | -14.7% | 11667 |  97  | 3.59 | -25.1%  | 1899  |  2  | 0.07 | -30.0%  |
| 2021-08-31 | 125  |    74728    | 416  | 3.33  | -29.7% | 11765 |  98  | 0.78 | -78.3%  | 1908  |  9  | 0.07 |  0.00%  |
| 2022-03-22 | 203  |    75767    | 1039 | 5.12  | +53.8% | 12591 | 826  | 4.07 | +421.8% | 1939  | 31  | 0.15 | +114.3% |
| 2022-09-18 | 180  |    76451    | 684  | 3.80  | -25.8% | 12773 | 182  | 1.01 | -75.2%  | 1980  | 41  | 0.23 | +53.3%  |
| 2022-10-01 |  13  |    76509    |  58  | 4.46  | +17.4% | 12809 |  36  | 2.77 | +174.3% | 1981  |  1  | 0.08 | -65.2%  |
| 2022-10-07 |  6   |    76536    |  27  | 4.50  | +0.90% | 12826 |  17  | 2.83 | +2.17%  | 1981  |  0  | 0.00 | -100.0% |
| 2022-10-17 |  10  |    76582    |  46  | 4.60  | +2.22% | 12850 |  24  | 2.40 | -15.2%  | 1982  |  1  | 0.10 |   N/A   |
+------------+------+-------------+------+-------+--------+-------+------+------+---------+-------+-----+------+---------+
Values in orange are estimated

$ █
```

</details>

#### Advanced mode:

To use the <font color=blue><b>advanced mode</b></font> you will need to use arguments after `python utility.py`

- [-f, --file](https://github.com/scalvaruso/utility#-f---file)<br/>
the argument [--file](https://github.com/scalvaruso/utility#-f---file) allows to specify the CSV file with the list of readings to use<br/>
If [--file](https://github.com/scalvaruso/utility#-f---file) is not used the default used file is `utilities.csv`
- [-m, --merge](https://github.com/scalvaruso/utility#-m---merge)<br/>
the argument [--merge](https://github.com/scalvaruso/utility#-m---merge) allows to merge two specified CSV files in the default `merged.csv` file
- [-p, --print](https://github.com/scalvaruso/utility#-p---print)<br/>
the argument [--print](https://github.com/scalvaruso/utility#-p---print) allows to print a table with the list of readings from a specified CSV file
- [-s, --save](https://github.com/scalvaruso/utility#-s---save)<br/>
the argument [--save](https://github.com/scalvaruso/utility#-s---save) allows to specify a CSV file where to write the new or updated list of readings<br/>
If [--save](https://github.com/scalvaruso/utility#-s---save) is not used, the new data will be saved as `utilities.csv`, as the file specified by [--file](https://github.com/scalvaruso/utility#-f---file), or as `merged.csv` if you are using the [--merge](https://github.com/scalvaruso/utility#-m---merge) argument

Let's see their usage

##### -f, --file

The `--file` argument is used to specify a CSV file different from the default one.
Typing `python utility.py -f demo.csv` will start the program reading data from the `demo.csv` file.<br/>
If the file does not exist, the program will automatically create the file

```
$ python utility.py -f demo.csv

The file demo.csv has been created

Date of new readings (YYYY-MM-DD): █
```

The program works only with CSV files, therefore you will receive an error message if you try to use a different extension, but the program will not exit.<br/>
Program will keep running, and looking for the existence of a file with same name and CSV extension
```
$ python utility.py -f demo.txt

This program works only with CSV files

Checking for the existence of the file demo.csv...
```
If the file does not exist you will be asked if you want to create it.<br/>
In case of positive answer [<b>y</b>/n] the program will create the file and start

```
Do you want to create the file demo.csv? [y/n] y

The file demo.csv has been created

Date of new readings (YYYY-MM-DD): █
```
If the file exists you will be asked if you want to open it.<br/>
In case of positive answer [<b>y</b>/n] the program will read the data from the file and start

```
File demo.csv already exist! Do you want to open it? [y/n] y

Date of new readings (YYYY-MM-DD): █
```
In case of negative answer [y/<b>n</b>] the program will simply exit

```
Do you want to create the file demo.csv? [y/n] n

$ █
```

> If no [--save](https://github.com/scalvaruso/utility#-s---save) file is specified, your inputs will be saved to the `--file` argument

##### -m, --merge

The `--merge` option requires <u>two arguments</u> and is used to merge the two CSV files in the arguments to a new list, print the table with the merged data and save them to a new CSV file.<br/>
In case of double values for the same date, you will be prompted to choose which data you want to keep

```
$ python utility.py -m ut_ma.csv ut_mb.csv

 There is already a reading for  2014-10-14
+-----+------------+------+-------------+-----+-------+-----+-----+----+------+-----+-------+----+------+-----+
|     |    Date    | days | Electricity | kWh | kWh/d | eT  | Gas | m3 | m3/d | gT  | Water | kL | kL/d | wT  |
+-----+------------+------+-------------+-----+-------+-----+-----+----+------+-----+-------+----+------+-----+
| Old | 2014-10-14 |  0   |    63172    |  0  |  N/A  | N/A | 563 | 0  | N/A  | N/A | 1070  | 0  | N/A  | N/A |
| New | 2014-10-14 |  0   |    63172    |  0  |  N/A  | N/A | 563 | 0  | N/A  | N/A | 1070  | 0  | N/A  | N/A |
+-----+------------+------+-------------+-----+-------+-----+-----+----+------+-----+-------+----+------+-----+
 Would you like to overwrite it?  [y/n] █
```
In case one or more files in the argument do not exist the program will give an error message and terminate
```
$ python utility.py -m ut_ma.csv ut_b.csv

The file ut_b.csv does not exist!

$ █
```
In case one or more files in the argument have no CSV extension, the program will look for the existence of a CSV file with same name and ask whether you want to use those files

```
$ python utility.py -m ut_ma.txt ut_mb.csv

Only CSV files can be merged

Checking for the existence of the file ut_ma.csv...

File ut_ma.csv already exist! Do you want to merge it? [y/n] █
```

> If no [--save](https://github.com/scalvaruso/utility#-s---save) file is specified, your data will be saved to the default file `merged.csv`

##### -p, --print

The `--print` option allows to print a table with the data from the specified CSV file

```
$ python utility.py -p ut_2.csv

Utilities
+------------+------+-------------+-----+-------+-----+-----+-----+------+-----+-------+-----+------+-----+
|    Date    | days | Electricity | kWh | kWh/d | eT  | Gas | m3  | m3/d | gT  | Water | kL  | kL/d | wT  |
+------------+------+-------------+-----+-------+-----+-----+-----+------+-----+-------+-----+------+-----+
| 2022-08-01 |  0   |      0      |  0  |  N/A  | N/A |  0  |  0  | N/A  | N/A |   0   |  0  | N/A  | N/A |
| 2022-09-01 |  31  |     100     | 100 | 3.23  | N/A | 100 | 100 | 3.23 | N/A |  100  | 100 | 3.23 | N/A |
+------------+------+-------------+-----+-------+-----+-----+-----+------+-----+-------+-----+------+-----+
Values in orange are estimated

$ █
```
In case the file in the argument does not exist or has an extension different from CSV the program will give an error message and terminate
```
$ python utility.py -p utt.csv

The file utt.csv does not exist!

$ python utility.py -p ut_e.txt

Only CSV files can be printed

$ █
```

##### -s, --save

The `--save` option allows to specify a different file where you want to save your data.<br/>
In case the file in the argument have no CSV extension, the program will look for the existence of a CSV file with same name and ask whether you want to create or use that file

```
$ python utility.py -s ut_e.txt

This program can save only CSV files

Checking for the existence of the file ut_e.csv...

File ut_e.csv already exist! Do you want to overwrite it? [y/n] n

$ python utility.py -s utt.txt

This program can save only CSV files

Checking for the existence of the file utt.csv...

Do you want to create the file utt.csv? [y/n] █
```
