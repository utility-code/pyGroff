import subprocess
from pathlib import Path
from pygroff.processor import *

"""
This is the main module which calls all the required functions.
"""


def clean_up(ag, tempfile, tempfile2, outfile):
    """
    Delete unneeded files
    Convert to word document if needed
    """
    if ag.d == True:  # For debugging, delete or not delete files
        subprocess.run(f"rm {str(tempfile)}", shell=True)
        if ag.i == True:
            subprocess.run(f"rm {str(tempfile2)}", shell=True)
    if ag.w == True:
        subprocess.run(
            f"libreoffice --headless --convert-to docx --infilter='writer_pdf_import' {str(outfile)}",
            shell=True,
        )


def decide_image(ag, tempfile, tempfile2, outfile):
    """
    Decide if the file has images. Default is true. Not much difference, except more images = more compile time
    """
    if ag.i == False:  # If there are images
        subprocess.run(
            f"tbl {str(tempfile)}|groff -e -mspdf -Tpdf > {outfile}", shell=True
        )
    else:  # Save compile time
        subprocess.run(
            f"tbl {str(tempfile)} | groff -e -mspdf -Tps > {str(tempfile2)} && ps2pdf {str(tempfile2)} {outfile}",
            shell=True,
        )


def main(ag):
    """
    This calls the required functions and cleans up after the program is done
    """
    fpath = Path(ag.f)
    outfile = Path(ag.f).parent / ag.o
    with open(fpath.with_suffix(".ms"), "w+") as f:
        if ag.cov == True:  # Add cover
            f.write(
                f".ad c\n.tp\n.sp 5\n.(c\n{ag.t}\n.)c\n.sp 2\n.(c\n{ag.n}\n.)c\n.sp 2\n.(c\n{get_date(ag.df)}\n.)c\n.bp\n.ad l\n"
            )
            f.flush()
        f.write(intermediary_creator(fpath=fpath, ag=ag))

        if ag.toc == True:  # Add table of contents
            f.write("\n.TC\n")

    tempfile, tempfile2 = fpath.with_suffix(".ms"), fpath.with_suffix(".ps")
    decide_image(ag, tempfile, tempfile2, outfile)
    clean_up(ag, tempfile, tempfile2, outfile)

    print(f"Done writing the file to -> {outfile}")
