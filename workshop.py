#!/Users/tm633717/source/workshop/venv/bin/python
from zowesupport import *
import json
import pandas
import argparse


# Argument Parsing
# Limits choices to valid Endevor List options
choices = ["codepages", "defaults", "dialog", "elements", "environments",
           "features", "instances", "packages", "processor-groups", "pgrp",
           "processcor-symbols", "psym", "stages", "subsystems", "symbols",
           "tasks", "type-sequence", "types"]

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--object", help="Object to list", required=True, choices=choices, dest='object')
parser.add_argument("-d","--directory", help="Output directory", default="commands")
parser.add_argument("-m", "--maxrc", help="Max return code for jobs", default=0, type=int)
parser.add_argument("-t", "--type", choices=["excel", "csv"], help="Excel or CSV", default="excel")
parser.add_argument("-f", "--filename", help="Output of filename", default="out", dest="filename")
args = parser.parse_args()


# Execution
command = f"zowe endevor list {args.object} --rft string --sm"
data = simpleCommand(command, args.directory)
data = json.loads(data, strict=False)
if args.type == "excel":
    pandas.DataFrame(data).to_excel(f"{args.filename}.xlsx")
elif args.type == "csv":
    pandas.DataFrame(data).to_csv(f"{args.filename}.csv")
else:
    print("error, unknown value")
