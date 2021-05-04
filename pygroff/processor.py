import subprocess
from pathlib import Path
from PIL import Image

#  import re

"""
This module takes care of the bulk of processing etc
"""

# adds ranges of headers
dict_hash = {"#" * x: f".NH {x}" for x in range(1, 6)}
dict_symbols = {
    "%": ".TL",
    "@": ".AU",
    "<": ".ad c",
    ">": ".ad r",
    "~": "",
    "-": ".IP ",
    "*": ".b ",
    "/": ".i ",
    "_": ".ul ",
    "!": ".PDFPIC",
    "+": ".bp",
}
full_list = list("#%@<>~*/_!+=")


def get_date(form):
    """
    Date time formate for cover page
    """
    import datetime

    return datetime.datetime.now().strftime(form)


def grab_image_and_convert(sentence):
    """
    Reads image, if not in .ps -> converts it to .ps and returns the required string
    """
    fpath = Path(sentence[1::].strip())
    if fpath.suffix != ".ps":
        Image.open(fpath).convert("RGB").save(
            str(fpath.with_suffix(".ps")), lossless=True
        )

        #
        #  subprocess.run(
        #      f"convert {str(fpath)} {str(fpath.with_suffix('.ps'))}", shell=True
        #  )
    return f".DS L\n\n.PSPIC {str(fpath.with_suffix('.ps'))}\n.DE\n"


def code_runner(x, ag):
    """
    Formats the code with newline separated by ;
    Also saves the output of the code
    """
    cod = "\n\n".join(x[1::].split(";")) + "\n"
    if ag.e == True:
        cod += (
            "\n Output : \n\n"
            + str(
                subprocess.Popen(
                    f'{ag.l} "{x[1::]}"', shell=True, stdout=subprocess.PIPE
                )
                .communicate()[0]
                .decode("utf-8")
            )
            + "\n"
        )
    return cod


def table_creator(x):
    """
    Add tables very easily
    """
    tb = "\n.TS\ntab(;) allbox ;\n"
    x = x[1::]
    tb_vals = x[x.find("(") + 1 : -2]
    temp_tb = tb_vals.split(",")
    count_cols = len(temp_tb[0].split(";"))
    tb += "c " + "s " * (count_cols - 1)
    tb += "\n" + "c" * count_cols + " .\n"
    if "[" in x:
        tb += x[1 : x.find("]")] + "\n"
    else:
        tb += "Table\n"
    tb += "\n".join(temp_tb) + "\n.TE\n"
    return tb


def subscript(sentence):
    return "\*{" + sentence[1::]


def eqn(sentence):
    """
    Returns a tag of equations. This is preprocessed by eqn (GNU troff)
    """
    return "\n.EQ\n" + sentence[1::] + "\n.EN\n"


def ret_symbol(sentence, list_flag, ag):
    """
    This checks the dictionaries and identifies what to send to groff
    """

    s0 = sentence[0]
    if s0 == "!":
        return grab_image_and_convert(sentence), list_flag

    if s0 == "^":
        return subscript(sentence), list_flag
    if s0 == "=":
        return eqn(sentence), list_flag

    if s0 == ")":
        return code_runner(sentence, ag), list_flag
    if s0 == "|":
        return table_creator(sentence), list_flag

    if s0 in list("*/"):
        return (
            "\n" + dict_symbols[s0] + "\n" + sentence[1::].lstrip() + "\n.LP",
            list_flag,
        )
    if list_flag > 0 and s0 in full_list:
        list_flag = 0

    ch1 = [x in sentence for x in dict_hash.keys()]
    counthash = ch1.count(True)
    if counthash > 0 and s0 != "~":
        val = sentence[counthash::].lstrip()
        return (
            dict_hash["#" * counthash] + "\n.XN " + sentence[counthash::].lstrip(),
            list_flag,
        )

    else:
        currentsym = dict_symbols[s0]
        if s0 == "-" and list_flag == 0:
            list_flag = 1
            currentsym += str(list_flag) + ")"
        elif s0 == "-" and list_flag > 0:
            list_flag += 1
            currentsym += str(list_flag) + ")"
        currentsym = currentsym + "\n" + sentence[1::].lstrip()

        if s0 in list("<>"):
            currentsym += "\n.ad l"
        return currentsym, list_flag


def intermediary_creator(fpath, ag):
    """
    Since groff needs an intermediary file, we create it. Dont worry! It will be deleted later :)
    """
    f_in = open(fpath, "r")
    out_string = ""
    flag = 0
    list_flag = 0
    for i, line in enumerate(f_in.readlines()):
        try:
            outs, list_flag = ret_symbol(line, list_flag=list_flag, ag=ag)
            out_string += outs
            flag = 0
        except KeyError:  # Basically every other letter
            flag = 1
        if flag == 1:
            out_string += f".LP\n{line}"
            flag = 2
        elif flag == 2:
            out_string += line

    return out_string
