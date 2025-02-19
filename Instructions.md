# Introduction
During this exercise, you will work with Python to automate a number of actions using [Zowe CLI](https://zowe.org).

# Getting Started
Zowe CLI is a command line interface.  It is often used for automation, much like a Rexx would be used on the mainframe.

Rexx is very powerful.  And so is Python.  Rexx can automate many actions on the mainframe but has also been ported to other platforms.  Python can be used to automate things on the mainframe and distributed environments.

A big advantage of Python over Rexx is library support.  In Rexx, you can find scripts to perform many actions, however, interacting with off host applications might require a lot more work.  

Using libraries in Python, we can integrate with a variety of systems and applications with little code.

## What is Python
Python is a versatile and powerful scripting language known for its simplicity and readability. Here's a summary of the key aspects:

**Scripting Nature**: Python is interpreted, meaning it executes code line by line without prior compilation, making it ideal for rapid development and experimentation.

**Readability and Simplicity**: It features a clean syntax that emphasizes readability, such as using indentation to define code blocks, which contributes to writing clear and maintainable scripts.

**Versatility**: Python finds applications in various domains, including web development (with frameworks like Django), data analysis (using libraries like Pandas), and machine learning (through TensorFlow).

**Open-Source**: As an open-source language, Python benefits from a collaborative community that continuously contributes to its improvement and supports free usage.

**Community Support**: A robust developer community provides extensive resources, forums (like Stack Overflow), and libraries, facilitating problem-solving and learning.

**Ease of Use vs. Performance**: While Python may be slower than compiled languages for CPU-intensive tasks due to the Global Interpreter Lock (GIL), it compensates with ease of use and rapid development capabilities. Workarounds using multiprocessing or asynchronous programming can enhance performance.

**Libraries and Modules**: Python boasts a comprehensive standard library and access to numerous third-party packages via tools like pip, enabling developers to extend functionality without reinventing the wheel.

**Learning Resources**: Abundant tutorials, books, and online courses are available, making Python an accessible language for both newcomers and experienced developers.

In summary, Python is a powerful yet approachable scripting language with strong community support, extensive libraries, and versatility across multiple applications, positioning it as an excellent choice for developers at all levels.

## Python conventions
There are some things to know about writing Python.  For our purposes, we want to keep in mind a couple of things:
1. Python tracks code blocks using spaces or tabs.  To be consistent, use one or the other but not both.  This workshop uses tabs.  If you have different indentation levels, you will get errors during the execution.
2. Functions are defined as `def functionName(parameters):` All the commands in the function must be indented under the def block.
3. In this example, we are using very basic error checking.  There are more advanced methods not covered here.
4. Python can be run as a script (as we are here) or interactively (great for testing/debugging).

----
# Our First Challenge
We want to create a script to export information from Endevor.  This could be a list of elements, systems, packages, etc.  

We want to export this information into Microsoft Excel.  This is a binary document that has to be in a specific format for Excel to read it.  There are various methods to get the data into Excel, including exporting screen captures, writing some Rexx to get the data into CSV or using Endevor's CSV Utility and transferring it to our desktop.  

When we decide on automating an action, we must look at ways to perform the action.  Let's assume we want to:
1. Run this off host
2. Make it flexible
3. Output the data in CSV or Excel formats
4. Use the Endevor REST API

## Run Off Host
We may want to use automation, perhaps a scheduler, to get the information regularly.  We may also want to perform actions with the data, such as generating a chart.  It might be difficult to perform that on the mainframe using Rexx, so using it off host may make sense.

## Flexibility
The operation should allow us to work with multiple Endevor objects.  Perhaps we want to export information regarding elements but later want to export processor groups.  Thinking ahead gives us the ability to perform those actions with minimal effort.

## Output
There can be a ton of ways to look at information.  On and off the mainframe, there are various reporting engines.  Business Analysts love Excel.  So, let's assume we want to use Excel and CSV as output formats.  

These aren't the only formats available.  If we wanted use to time series values, we might export the data to a database so it could be manipulated in different ways.

## Using Endevor REST API
Endevor offers multiple ways to get data out of it.  JCL and CSVs are common ways to get data out.  Endevor also offers a [REST based API](https://aws.amazon.com/what-is/restful-api/).

The [Endevor REST API](https://techdocs.broadcom.com/us/en/ca-mainframe-software/devops/ca-endevor-software-change-manager/19-0/using/using-the-rest-api.html) can be accessed directly, much like a web browser communicates with a web server.  This offers a lot of flexibility, but we can also use the Zowe CLI to perform the action for us.  The Zowe CLI (command line interface) uses a configuration file to manage connection and profile information.  It also provides a nice structure for interacting with Endevor.

The Zowe CLI does have some limitations.  It wasn't designed to export Excel documents, for example.  

Let's take our first run at getting data from Endevor.  Let's use the terminal.  It can be accessed using the hamburger menu (three horizontal lines), Terminal, New Terminal:

`zowe endevor list packages`

This command give a tabluar view of output:
----
```
Running on host: HOST:7080 instance: NDVRWEBS
pkgId            description                                   status     updtDate                    updtUsrid
ARADEMO          DEMO FOR ARA                                  APPROVED   2025-01-14T13:16:25.20+0000 MCQTH01  
AS               Created from SNOW                             APPROVED   2025-01-14T13:41:22.77+0000 MCQTH01  
BANK DEMO        Bank Demo                                     INEDIT     2024-11-12T08:37:29.11+0000 JAGBR01  
BANK DEMO 2      demo                                          INEDIT     2024-11-12T10:13:31.40+0000 JAGBR01  
BANK DEMO 3      BANK DEMO                                     INEDIT     2024-11-12T13:00:10.93+0000 JAGBR01  
BATTIVA          promotion pkg                                 EXECUTED   2024-01-11T13:18:49.70+0000 FERTI99  
BATTIVATPKG      teste                                         INEDIT     2024-01-15T10:54:51.94+0000 FERTI99  
BATTIVA0         std package                                   COMMITTED  2024-01-11T16:02:13.72+0000 FERTI99  
BATTIVA1         battiva1                                      EXECUTED   2024-01-11T16:38:54.18+0000 FERTI99  
BK001            Demo Package                                  INEDIT     2021-09-21T16:35:56.16+0000 CUST001  
BRBD4TPACKAGT001 Deployed to DEP4TEST by BERBE02 @ 9 Sep 2019  EXECFAILED 2019-09-09T12:55:01.69+0000 BERBE02
```
----
A table like this might be great for viewing information but it does have limits.  If we want to import it into Excel, we have to identify columns.  And that's usually interactive.  That's not good for automation.  And what if we change the columns?  That automation might break.  And the more columns, the longer the output.  

Try running the previous command with `--full-output` and see how much information is returned.

Is there a way to export into CSV format from Zowe CLI's Endevor Plugin?

Check the documentation by running in terminal:

`zowe endevor list packages --help`

If you see the section, "Response Format Options", you'll notice there's three options.
1. Response Format Filter (--rff) is used to specify a list of fields you want to display.  While helpful in getting just the data we want, it won't help put the data into an Excel spreadsheet.
2. Response Format Type (--rft) is used to specify the output type.  This could get us to CSV or Excel, but those don't seem to be options.  It offers TABLE, LIST, OBJECT or STRING.  
    TABLE is the default option.  That's not overly flexible in this situation.
    LIST provides the information in a series of JSON objects. 
    OBJECT lists the values, but they are a single object:value pair per line.  
    STRING lists the data in a large array in a JSON string.
3. Response Format Header (--rfh) is a boolean value that just determines if the headers are printed.  

None of the options allow for easy CSV export, so we need to find a different way. 

Run the commands to see the outputs and compare them:

`zowe endevor list packages --rft table`

`zowe endevor list packages --rft list`

`zowe endevor list packages --rft object`

`zowe endevor list packages --rft string`

Out of the all options, it looks like `--rft string` is the closest to capturing column and row information.  However, if you run this, you'll notice messages at the top of the output.  Let's remove those using the suppress messages flag, `--sm`.
]\
Run:

`zowe endevor list packages --rft string --sm`

And check the output, it should be just data, no header or other information.

Now that we have identified a way to get the data out, let's look at automating it.

## Automating the action
Command line applications can run as single command, or they can take options to be more flexible, like the Zowe CLI. 

Our first goal is to execute the command then make it flexible.  

Create a new file, call it `first.py`.  You can create the file through the file option or using the terminal and typing `code first.py`.

Copy this text into file:

```
from zowesupport import *

command = "zowe endevor list packages --rft string --sm"
data = simpleCommand(command, "out")
print(data)
```

This is a simple application to introduce a couple of concepts.

The first line imports the zowesupport library. This library wraps functions for calling command line utilities and running mainframe jobs. It also stores the output from the commands.

`command = "zowe..."` assigns the command we want to run to the variable command.

`data = simpleCommand...` runs the command, writes the command output to the out folder, the takes the output from the command and assigns it to a variable named `data`.

`print(data)` does exactly that, it prints the data on the command line. 

If you did this correctly, you should get the same output as running the zowe command directly.

Now that you've seen what it takes to get the output, let's look at the main application so we can modify it for our job, exporting the data into Excel.

## Workshop.py
Take a look at the Workshop.py file.  You'll notice import statements at the top.

### Libraries
`from zowesupport import *` imports our library.

`import json` imports a library to work with JSON data.

`import pandas` imports the pandas library.

`import argparse` imports an argument parser for various options.


A quick message about libraries.  There are a ton of libraries for performing a multitude of operations.  If you visit [PYPI](https://pypi.org) you can find a lot of libraries online.  You can write webservers (Streamlit, Django, Flask), work with data (Pandas, Numpy) and even read and write Excel files (openpyxl).

These libraries are installed using Python's package manager, pip.  All the libraries for this workshop are already installed, but if you needed to install one, you could run a command such as `pip install openpyxl` to install that libary.

### Execution
Search down for the **# Execution** comment.  This is where the application actually does the work.

You will find `command = ""`.  We need to put our command in the quotes.


Replace `command = ""` with `command = "zowe endevor list packages --rft string --sm"`.

The next line with `simpleCommand` executes the command and returns the output into the data variable.

As the final line in the code, add `print(data)`.

Now run the application, the output should be the same as `first.py`.

### Output to Excel
There are multiple libraries to perform actions.  One library, OpenPyxl, allows direct interation with Excel spreadsheets.  This library breaks the file into workbooks and sheets.  However, to move data into Excel, we'd have to parse the data and specify the location for it.

We have a shortcut, however.  There's a library called Pandas.  You'll notice that we didn't load OpenPyxl in the import section.  The library has been installed, but we won't be calling it directly.  We will use Pandas.  It's a heavily used library to deal with cell based data, often used in AI model creation.

Before we can use Pandas, the data needs to be converted from a string to an object.  JSON is a string that makes it easy to work with data, much like XML.  It has rules and we will use a library to work with it.

Replace your print command with a new line:

`data = json.loads(data, strict=False)`

The data variable was filled with a string.  We are going to reuse the same variable name and recast it as an object.  The object is going to be created using the `jsons.loads` function. It takes a string, in this case data, and returns the object.  Sometimes, the Zowe command will return data that isn't completely valid in JSON, so using the `strict=False` flag allows the data to be loaded properly.

The data is now in object form and we can use Pandas to write the file as an Excel spreadsheet.

Add the following line to the end of your script:

`pandas.DataFrame(data).to_excel("packages.xlsx")`

*What does this command do?*

[Pandas](https://pypi.org/project/pandas/) is a data manipulation library.  If you look at the documentation, you'll see one of the major modules is called a [DataFrame](https://pandas.pydata.org/docs/reference/frame.html).  The data frame is used to house the information and work with it.

`pandas.DataFrame(data)` uses the pandas Library and creates a DataFrame using the data from the JSON output of our Zowe command. We can then call a function of the data frame to export to Excel (the *.to_excel()* function).  We pass in a filename and it will write that to an Excel spreadsheet.

Note:  This is a shortcut method.  We could have written the code to look like:

```
pd = pandas.DataFrame(data)
pd.to_excel("packages.xlsx")
```

But this creates another variable for one call.  Better to have cleaner code (both visually and programmatically) and just not have another variable and line.

Once you make this change, save and execute the python program:

`python workshop.py`

It should not really display any information, however, it will write out a file called "packages.xlsx" in your current directory.

The file should be seen in the File Explorer or you can list is using the `ls -l` command in the terminal window.

### Flexibility is good
Let's make the script more flexible.  We want the user to select any available object for listing, including elements, systems, subsystems, etc.  And what if they need it in CSV instead of Excel?  Let's also allow the user to specify the name of the file.

Using the ArgParse library will allow us to do that.

[ArgParse](https://docs.python.org/3/library/argparse.html) is library that works with command line arguments. Instead of managing them manually, we can use a library and set up some simple rules.  

There's a section of code (lines 13-19).  It is commented out (# in first column).  Remove the comments.  You can highlight the commands and press CTRL-/ (windows) or Command-/ (mac) and it will remove the comment block for you.

`parser = argparse.ArgumentParser()`

This creates a parser object called parser.  We can add arguments, determine values for them, make the required, etc.  

You will find a section of add_arguments commands.  These add arguments to the command, as well as help and various options. 

We also have options for object, output directory, max return code, type and filename.
    Object is the item we want to query.  Let's require that.
    Directory is where the output of our commands will be stored.  We may or may not want this, however, it's useful for debugging if needed.
    Max Return Code could be used if we have a range of acceptable return codes.  Typically, it will be used when executing jobs.
    Type is used to determine if the output will be CSV or Excel
    Filename is used to set the filename for the CSV/Excel file.

    Review the other arguments for each *.add_argument()* command.  You'll see you can make them required or optional, display help and even assign the value to a variable.

`parse_args()` will parse the arguements during the command line execution, making them available.

Now that we have some flexible data entry, we need to adjust the commands to work with it.

The first place to change is the command string.  It's currently hard coded, so let's make it more flexible.

Let's change the code so it can take the object passed in via the command line so we don't have to hardcode the value.

Find the `command = "zowe ..."` string and change it to:

`command = f"zowe endevor list {args.object} --rft string --sm"`

Place an "f" in front of a string turns it to an "F-Mode string".  This allows us to interpolate variables into the string.  It will substitue the string values, making it easier to read.  If we didn't use them, the string would look more complicated, like a Rexx string.  It would look like:
`command = "zowe endevor list " + args.object + " --rft string --sm"`

F-Mode strings simplify this.  Using a Python editor, it will even highlight the variable different in the string.

Now, let's adjust the `data = simpleCommand(command, "command")` so that we can pass a user selectable directory. To do that change the code to:

`data = simpleCommand(command, args.directory)`

Now, let's adjust the code so it will write the appropriate file type out, based upon the `--type` flag.  This new block of code tests the args.type variable to see if it is Excel or CSV and writes the appropriate file extension.

Replace the current pandas.DataFrame(data) line with the following code block:

```
if args.type == "excel":
    pandas.DataFrame(data).to_excel(f"{args.filename}.xlsx")
elif args.type == "csv":
    pandas.DataFrame(data).to_csv(f"{args.filename}.csv")
else:
    print("error, unknown value")
```

You should be able to run the following command to create an Excel spreadsheet with the data.

`python workshop.py -o packages`

Why didn't we have to specify Excel or CSV?  We set the default as Excel on the parse command for type.

The defaults were also included for directory, maxrc and even the filename.

However, we aren't done yet.  If you have a typo for the object name, the command will fail.  You may not see the failure unless you view the command directory.

Let's make this a little more user friendly.  If the user has a typo, let's correct them before we even execute the command.

You'll notice there's a line `choices = ["codepages", "defaults"...]`.  This is called a Python dictionary.  ArgParser can validate the values for arguments using dictionaries.  Rather than put them inline, making the code harder to read, we created a dictionary called choices with a list of valid choices.  

If you look at the type arguement line, you will see it listed there:
`parser.add_argument("-t", "--type", choices=["excel", "csv"], help="Excel or CSV", default="excel")`

The argument, `choices=["excel", "csv"]` defines them.  That list is small and pretty readable.  But the long list of available arguments for the object would be unreadable in the command itself.  So, we are going to change:

`parser.add_argument("-o", "--object", help="Object to list", required=True, dest='object')`

to

`parser.add_argument("-o", "--object", help="Object to list", choices=choices, required=True, dest='object')`

Save the file and run it again.  If you run

`python workshop.py -o pacages`

You will get better output:
```
usage: workshop.py [-h]
                   -o {codepages,defaults,dialog,elements,environments,features,instances,packages,processor-groups,pgrp,processcor-symbols,psym,stages,subsystems,symbols,tasks,type-sequence,types}
                   [-d DIRECTORY] [-m MAXRC] [-t {excel,csv}] [-f FILENAME]
workshop.py: error: argument -o/--object: invalid choice: 'pacages' (choose from 'codepages', 'defaults', 'dialog', 'elements', 'environments', 'features', 'instances', 'packages', 'processor-groups', 'pgrp', 'processcor-symbols', 'psym', 'stages', 'subsystems', 'symbols', 'tasks', 'type-sequence', 'types')
```

We've now made the application more rubust.

Note, argparse creates a help system.  You can run:

`python workshop.py -h`

And it will provide a full description of the application and options, all from the ArgParse library.

### Let's make it easier to execute.
Python is a scripting language.  If you've ever used BATCH on DOS/Windows, you know you can execute it directly.  On Linux/USS, you can do the same with other scripting languages, but it takes two steps to do it.  The environment we are using now is a Linux environment.

**First Part**

We have to add a new line to the script to call the interpreter.  Second, we need to change permissions of the file so it can be executed.

The first line of a script can have a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) directive to indicate which engine to run.  We can run Bourne Shells, Python, Javascript, Perl, etc.  The first line identifies which one to use.  

We can also have multiple versions of the same scripting engine installed (such as Python 2.7 vs 3.0 vs 3.11).  We need to specify which one to use.  How do we find it?

On most Unix/Linux distributions, there's a utility called `which`.   Others use `type`.  Either command should return the location where an application is installed and running from.  It must be within the PATH environment variable.  If it is not in the PATH, it will not be found. 

Run:

`which python`

It should show `/usr/bin/python`.  This is the location of Python for this machine.

We are going to add the shebang to the top of the file, like this:

`#!/usr/bin/python`

This should be above the `from zowesupport import *` line.

We've now told our operating system what to do, but if we run it, it will still fail.

**Second Part**

The script, as created has Read/Write privileges for the current user, and read for everyone else.  We need to set the execution bit.  We can do that using the `chmod` command.  

To set the execution bit, we run:

`chmod +x workshop.sh`

**Executing the program**
Linux/USS do not have the current directory in the execution path.  This is a security measure.  In order to execute an application in the current directory, we must explicitly call that file using the path.

A shortcut to the current path is "./".  

To execute our application now, we can simply type:

`./workshop.py` 

You will see the basic help show up on the screen.

### Seeing the results
If you've run this to create an Excel file, we need to view it.  If you have Excel on your local system, use the file explorer to right click on the file and select download.  You can download and use the file with Excel.

If you don't have Excel, you can use a viewer in VS Code.  Go to the extensions, search for Excel.  Install the Excel Viewer by GrapeCity.  You may get a licensing message, but it will show the file in a spreadsheet mode.

----

### Challenge Mode
Here's a simple challenge.  

Modify this line so it has a default object instead of forcing the user to type a name:

`parser.add_argument("-o", "--object", help="Object to list", required=True, choices=choices, dest='object')`

### Challenge Mode 2
Modify the command to show all the output for packages.  You may want to review the command:

`zowe endevor list packages --help`

There's an option for output, to get it all.  Add that to the command line (at the end is perfectly fine).  

Review the resulting Excel file.

## Workshop Wrap up
Using libraries, like `zowesupport` and `pandas`, we've written an application to export multiple object types in Endevor.  It can write them as CSV or Excel files.  You can also name the files and determine the output directory.

And you did that in roughly 30 lines of code.  

----

# Bonus Activity
In the previous activity, we used Zowe's Endevor plugin to access data.  

Zowesupport also offers job support.  We can run a job, extract the data, then process it.  

Doing something similar to the previous exercise, we will run a job and save the data as a PDF.  

## Set up the environment
We are going to use the [FPDF](https://pypi.org/project/fpdf/) library to create a PDF.  To use the FPDF library we need to install it.  The library was installed in the previous examples, but this time we will have to install the library ourselves.  To install the libary, we will use the Python package manager, pip. In the terminal, run this command:

`pip install fpdf`

It is now available for use in the python code. 

## Create the code

Create a new file, call it `workshop2.py`.  It can be created using the menu or in the terminal running `code workshop2.py`.

Just like before, we will import our libraries at the top:

```
from zowesupport import *
from fpdf import FPDF
```

The import command allows us to use the FPDF object. 

Let's create a function to write the PDF.  It should take two parameters. It will accept the contents for the PDF and the name.
This FPDF object manages the PDF. We will create a pdf variable from the FPDF object.  In this case, it is creating a document in Landscape, using a US Letter size. We then add a page and then set the font.  

The content will be split into lines, so let's iterate over those lines.  The .split('\n') function creates a list we can iterate over.  This will create a temporary array, and it will send each line to the pdf.cell() function, printing it onto the page.  

It finishes by writing the file using the filename we passed it.

```
def write_pdf(contents, filename):
    pdf = FPDF('L', 'mm', 'Letter')
    pdf.add_page()
    pdf.set_font("Courier", size=9)
    for i in contents.split("\n"):
        pdf.cell(80, 5, txt=i, ln=1, align='L')
    pdf.output(filename)
```

For simplicity's sake, we are going to hard code a a filename for the pdf and a dataset name.  Using the previous example, you could use ArgParse to pass that through to make the utility more flexible.  We will pass the dataset name into submitJobAndDownloadOutput().  It takes 3 parameters, the dataset name, a folder to download the output to and the spool file number.  This is just an example, but in this case, the JCL will run a DB2 select statement to display a table.

```
filename = "marbles.pdf"
ds = "cust001.marbles.jcl(marbdb2)"
owner, jobId, jobName, retCode = submitJobAndDownloadOutput(ds, "output", 104)
```

Python allows multiple variables as a return value.  In this case, submitJobAndDownloadOutput returns the owner, jobid, jobname and retcode.  If you look in the zowesupport implementation, if the job fails, the application will exit.  However, let's test it here, too.

We know the return code is in the format "CC 0000", so we need to break the string apart then cast it to an integer.  We test the integer to see if it greater than 0.  If it is, we simply exit the program passing in the return code.

```
if int(retCode.split(" ")[1]) > 0:
    print("job failed, see output")
    exit(int(retCode.split(" ")[1]))
```

Finally, we want to download the spool file.  In this case, the spool file number is 104.  We download the file from the jobid we received when we submitted the job.  

This will call write_pdf, passing in the contents and filename.  

Once it creates the PDF, it prints a message to the user.

```
contents = downloadSpoolFile(jobId, 104)
write_pdf(contents, filename)
print(f"Wrote PDF to {filename}")
```


Here's the completed version of the code:

```
from zowesupport import *
from fpdf import FPDF

def write_pdf(contents, filename):
    pdf = FPDF('L', 'mm', 'Letter')
    pdf.add_page()
    pdf.set_font("Courier", size=9)
    for i in contents.split("\n"):
        pdf.cell(80, 5, txt=i, ln=1, align='L')
    pdf.output(filename)


filename = "marbles.pdf"
ds = "cust001.marbles.jcl(marbdb2)"
owner, jobId, jobName, retCode = submitJobAndDownloadOutput(ds, "output", 104)
if int(retCode.split(" ")[1]) > 0:
    print("job failed, see output")
    exit(int(retCode.split(" ")[1]))

contents = downloadSpoolFile(jobId, 104)
write_pdf(contents, filename)
print(f"Wrote PDF to {filename}")
```

We took 22 lines of code to run a job, download the output and then save it to a PDF.

# Conclusion

You've seen how using Python libraries can enhance output from the mainframe.  There are tons of ways to continue to enhance your work and output.

Python offers all sorts of libaries, making it convenient to work with multiple solutions.  

This can be just the beginning.  Python is now available on USS using to Z Open Automation Utilities (ZOAU), making it even more useful.  ZOAU has libraries to support accessing datasets, jobs, etc., directly while running on the mainframe itself.  And while not all libraries are currently supported on USS, many are.

----

# Thank you!