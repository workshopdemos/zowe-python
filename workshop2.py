from zowesupport import *
from fpdf import FPDF

pdf = FPDF('L', 'mm', 'Letter')
pdf.add_page()

ds = "cust001.marbles.jcl(marbdb2)"
output = submitJobAndDownloadOutput(ds, "output", 104)
print(output)
pdf.set_font("Courier", size=9)
for i in output.split("\n"):
    pdf.cell(80, 5, txt=i, ln=1, align='L')
# pdf.cell(50,5, txt=output, ln=1, align='L')
pdf.output("out.pdf")

