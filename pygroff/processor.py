import subprocess
from pathlib import Path

#  import re

"""
This module takes care of the bulk of processing etc
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
    "!": ".PDFPIC",
    "+": ".bp",
}


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
        subprocess.run(
            f"convert {str(fpath)} {str(fpath.with_suffix('.ps'))}", shell=True
        )
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
                    f'python -c "{x[1::]}"', shell=True, stdout=subprocess.PIPE
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


def ret_symbol(sentence, list_flag, ag):
    """
    This checks the dictionaries and identifies what to send to groff
    """

    s0 = sentence[0]
    if s0 == "!":
        return grab_image_and_convert(sentence), list_flag

    if s0 == "^":
        return "\*{" + sentence[1::], list_flag
    if s0 == "=":
        return "\n.EQ\n" + sentence[1::] + "\n.EN\n", list_flag

    if s0 == ")":
        return code_runner(sentence, ag), list_flag
    if s0 == "|":
        return table_creator(sentence), list_flag

    if s0 in list("*/"):
        return (
            "\n" + dict_symbols[s0] + "\n" + sentence[1::].lstrip() + "\n.LP",
            list_flag,
        )

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


#  def quotematcher(sentence):
#      """
#      Find if there are any strings in quotes
#      """
#      return re.findall(r'\"(.+?)\"', sentence)

#
#  def quotereplace(quoted, line):
#      for i in quoted:
#          line = line.replace(f'"{i}"', f"\*(lq{i}\*(rq")
#      return line
#


def intermediary_creator(fpath, ag):
    """
    Since groff needs an intermediary file, we create it. Dont worry! It will be deleted later :)
    """
    f_in = open(fpath, "r")
    tbl = 0  # WIP
    out_string = ""
    flag = 0
    list_flag = 1
    for i, line in enumerate(f_in.readlines()):
        #  quoted = quotematcher(line)
        #  line = quotereplace(quoted, line)

        try:
            outs, list_flag = ret_symbol(line, list_flag=list_flag, ag=ag)
            out_string += outs

            flag = 0
        except KeyError:
            flag = 1
        if flag == 1:
            out_string += f".LP\n{line}"
            flag = 2
        elif flag == 2:
            out_string += line

    return out_string
