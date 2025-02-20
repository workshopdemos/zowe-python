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

# parser = argparse.ArgumentParser()
# parser.add_argument("-o", "--object", help="Object to list", required=True, dest='object')
# parser.add_argument("-d","--directory", help="Output directory", default="commands")
# parser.add_argument("-m", "--maxrc", help="Max return code for jobs", default=0, type=int)
# parser.add_argument("-t", "--type", choices=["excel", "csv"], help="Excel or CSV", default="excel")
# parser.add_argument("-f", "--filename", help="Output of filename", default="out", dest="filename")
# args = parser.parse_args()

# Execution
command = "zowe endevor list packages --rft string --sm"
data = simpleCommand(command, "output")
print(data)