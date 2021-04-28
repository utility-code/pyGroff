import subprocess
from pathlib import Path

"""
This is the main module which has almost all the required functions.
"""
dict_hash = {"#" * x: f".NH {x}" for x in range(1, 6)}
dict_symbols = {
    "%": ".TL",
    "%": ".TL",
    "@": ".AU",
    "<": ".ad c",
    ">": ".ad r",
    "~": "",
    "-": ".IP ",
    "*": ".b ",
    "/": ".i ",
    "_": ".ul ",
}


def main(ag):
    """
    This calls the required functions and cleans up after the program is done
    """
    fpath = Path(ag.f)
    outfile = Path(ag.f).parent / ag.o
    with open(fpath.parent / "temp.ms", "w+") as f:
        if ag.c == True:
            f.write(
                f".ad c\n.tp\n.sp 5\n.(c\n{ag.t}\n.)c\n.sp 2\n.(c\n{ag.n}\n.)c\n.sp 2\n.(c\n{get_date(ag.df)}\n.)c\n.bp\n.ad l\n"
            )
            f.flush()

        f.write(intermediary_creator(fpath=fpath))
        f.flush()
    tempfile = fpath.parent / "temp.ms"

    subprocess.run(f"groff -ms {str(tempfile)} -Tpdf > {outfile}", shell=True)
    if ag.d == True:
        subprocess.run(f"rm {str(tempfile)}", shell=True)
    if ag.w == True:
        subprocess.run(
            f"libreoffice --headless --convert-to docx --infilter='writer_pdf_import' {str(outfile)}",
            shell=True,
        )

    print(f"Done writing the file to -> {outfile}")


def get_date(form):
    """
    Date time formate for cover page
    """
    import datetime

    return datetime.datetime.now().strftime(form)


def ret_symbol(sentence, list_flag):
    """
    This checks the dictionaries and identifies what to send to groff
    """

    s0 = sentence[0]
    se = sentence[-1]
    if s0 in list("*/"):
        return (
            "\n" + dict_symbols[s0] + "\n" + sentence[1::].lstrip() + "\n.LP",
            list_flag,
        )

    ch1 = [x in sentence for x in dict_hash.keys()]
    counthash = ch1.count(True)
    if counthash > 0 and s0 != "~":
        return (
            dict_hash["#" * counthash] + ".LP\n" + sentence[counthash::].lstrip(),
            list_flag,
        )

    else:
        currentsym = dict_symbols[s0]
        if s0 == "-":
            if list_flag == 1:
                currentsym += str(list_flag) + ")"
            else:
                currentsym += str(list_flag) + ")"
            list_flag += 1
        else:
            if list_flag > 0:
                list_flag = 1

        currentsym = currentsym + "\n" + sentence[1::].lstrip()

        if s0 in list("<>"):
            currentsym += "\n.ad l"
        return currentsym, list_flag


def intermediary_creator(fpath):
    """
    Since groff needs an intermediary file, we create it. Dont worry! It will be deleted later :)
    """
    f_in = open(fpath, "r")
    tbl = 0  # WIP
    out_string = ""
    flag = 0
    list_flag = 1
    for i, line in enumerate(f_in.readlines()):
        try:
            outs, list_flag = ret_symbol(line, list_flag=list_flag)
            out_string += outs

            flag = 0
        except KeyError:
            flag = 1
        if flag == 1:
            out_string += f".LP\n{line}"
            flag = 2
        elif flag == 2:
            out_string += line
    if tbl == True:  # Ignore this for now. Will add table creation later
        tempfile2 = fpath.parent / "temp.ps"
        subprocess.run(f"rm {str(tempfile)} {str(tempfile2)}", shell=True)

    return out_string
