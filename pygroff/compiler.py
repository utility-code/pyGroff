import subprocess
from pathlib import Path
from pygroff.processor import *

"""
This is the main module which calls all the required functions.
"""


def main(ag):
    """
    This calls the required functions and cleans up after the program is done
    """
    fpath = Path(ag.f)
    outfile = Path(ag.f).parent / ag.o
    with open(fpath.with_suffix(".ms"), "w+") as f:
        if ag.cov == True:
            f.write(
                f".ad c\n.tp\n.sp 5\n.(c\n{ag.t}\n.)c\n.sp 2\n.(c\n{ag.n}\n.)c\n.sp 2\n.(c\n{get_date(ag.df)}\n.)c\n.bp\n.ad l\n"
            )
            f.flush()
        f.write(intermediary_creator(fpath=fpath, ag=ag))
        if ag.toc == True:
            f.write("\n.TC\n")

    tempfile = fpath.with_suffix(".ms")
    tempfile2 = fpath.with_suffix(".ps")

    if ag.i == False:
        subprocess.run(
            f"tbl {str(tempfile)}|groff -e -mspdf -Tpdf > {outfile}", shell=True
        )
    else:
        subprocess.run(
            f"tbl {str(tempfile)} | groff -e -mspdf -Tps > {str(tempfile2)} && ps2pdf {str(tempfile2)} {outfile}",
            shell=True,
        )

    if ag.d == True:
        subprocess.run(f"rm {str(tempfile)}", shell=True)
        if ag.i == True:
            subprocess.run(f"rm {str(tempfile2)}", shell=True)
    if ag.w == True:
        subprocess.run(
            f"libreoffice --headless --convert-to docx --infilter='writer_pdf_import' {str(outfile)}",
            shell=True,
        )

    print(f"Done writing the file to -> {outfile}")
