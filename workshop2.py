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