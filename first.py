from zowesupport import *

command = "zowe endevor list packages --rft string --sm"
data = simpleCommand(command, "out")
print(data)