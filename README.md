# Alarm Center Import

Created this script to make it easier to import a large number of zones into alarm accounts in [SIS Alarm Center](https://www.securitysoftware.com/en-us/products/Alarm-Center) with CSV.

## Configuration

- ``server`` to MSSQL database server
- ``database`` should be the same in all instances
- ``connection_string`` is currently set for trusted connection and will use Windows Authentication
- ``input_file`` is the file with the zone information
- ``output_file`` will return any zones that were not added successfully

```
server = "HOST_ADDR"
database = "SUBSCRIBER"
connection_string = "DRIVER={SQL Server};SERVER=" + server + ";DATABASE=" + database + ";Trusted_Connection=yes;"
input_file = 'zones.csv'
output_file = 'out.csv'
```

## Requirements

Install the required ``pyodbc`` library with pip:

```
pip install -r requirements.txt
```

## Usage

### Add data to CSV
Add your zone information to the zones.csv file. Only required information is:
- Account Number With Line Code (``CSF-1234``)
- Zone # (``1``)
- Description (``Entry Motion - Room 100C``)
- Type (``ALR, PAN, DUR, TMP``)

In the ``processCSV()`` function, you can configure additional columns in ``currentZoneDict`` to be imported from CSV as well if they are used by your agency.

### Run the Script
```
> python import.py
```

