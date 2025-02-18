import datetime
import json
import subprocess
from pathlib import Path
from dotmap import DotMap
import shlex
from shutil import which


ZOWE_CMD = which("zowe")

# Read config file, use dot (.) notation for accessing elements
configFile = Path("./config.json")
if configFile.exists():
    with open(configFile) as file:
        config = DotMap(json.load(file))

""" simpleCommand takes a command and directory.
It runs the command and saves the output to the directory.
If expectedOutputs is used, it will search the output for 
the values identified."""
def simpleCommand(command, dir, expectedOutputs=None):
    # output = ""
    command = shlex.split(command)
    output = subprocess.run(command, capture_output=True, text=True)
    
    content = f"Command: {command}\n"
    content += "Data:\n"
    content += f"{output}"
    
    writeToFile(dir, content)
    
    if not expectedOutputs is None:
        if not verifyOutput(content, expectedOutputs):
            raise ValueError("Value not found ", expectedOutputs)
    
    return output.stdout

def verifyOutput(data, expectedOutputs):
    for value in expectedOutputs:
        if value not in data:
            raise ValueError("Value not found ", value)
    return True

def submitandrety(dataset, dir, maxRC=0, numRetries=1):
    if numRetries > 0:
        submitJobAndDownloadOutput(dataset, dir, maxRC)
        numRetries = numRetries - 1
    else:
        raise ("Max retries exceeded")

def submitJobAndDownloadOutput(dataset, dir, maxRC=0):
    command = shlex.split(f'zowe jobs submit data-set "{dataset}" --wfo --rfj')
    content = f"Command: {command}\n"
    content += "Data:\n"
    output = subprocess.run(command, capture_output=True, text=True)
    if output.returncode > 0:
        raise ValueError("Return Code not valid", output)
    try:
        data = DotMap(json.loads(output.stdout, strict=False))
    except Exception as e:
        raise ValueError("Output is not JSON, did you use --rfj?")

    content += f"{output}"
    writeToFile(dir, content)
    retcode = int(data.data.retcode.split(" ")[1])
    if retcode > maxRC:
        print("MaxRC exceeded")
        exit(retcode)

    return data.data.owner, data.data.jobid, data.data.jobname, data.data.retcode

def downloadSpoolFile(jobId, spoolFile):
    command = shlex.split(f'zowe jobs view sfbi {jobId} {spoolFile}')
    output = subprocess.run(command, capture_output=True, text=True)
    if output.returncode > 0:
        raise ValueError("Return Code not valid", output)
    return output.stdout

"""Creates a directory and a file with the current timestamp.
If the directories don't exist, it makes them.
If they do exist, there's no error."""
def writeToFile(dir, content):
    filename = datetime.datetime.now().isoformat().replace(":","-")
    filepath = Path(dir + "/" + filename)
    filepath.parent.mkdir(exist_ok=True, parents=True)
    try:
        filepath.write_text(content)
    except:
        raise
