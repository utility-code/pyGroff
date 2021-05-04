# pyGroff

- A wrapper for groff using python to have a nicer syntax for groff documents
- [DOCUMENTATION](https://subhadityamukherjee.github.io/pyGroff/)
- Very similar to markdown. So if you know what that is. You will love this :)
- We hate word -.-
- Editing pdfs is a pain and please we are lazy
- We love markdown. But we need pdfs and docx. So why not 
- LaTEX is amazing but it is tooo much work for small things.
- Vim is love. What can we do without keyboard shortcuts ):

## What can you do
- Write in a text file
- Get a cover page as well :)
- Get a Table of contents. (Due to limitations : its only on the last page for now.)
- Add code. And get execution results directly! Default is python. You can use any other language in your system
- Easy tables (Aint nobody got time for complicated ones)
- You can get a word document too (you do need libreoffice for it)
- Get auto generated, beautifully formatted pdfs and docs instantly
- Not cry because you moved an image and now your document is in hieroglyphics
- (You can also write in groff syntax in the file. It will work as well. Just in case you need something extra)

## Requirements
- You need python of course.
- For python dependencies, using pip install -r requirements.txt (Only PIL)
- Almost every unix system has groff preinstalled.
- If you want to convert to word, you need libreoffice.
- If you want to get a table of contents you will need pdftk
        - yay pdftk #arch
        - sudo pacman -S pdftk #arch
        - sudo apt install pdftk

## Syntax
- p runner.py -f "demo.txt" -o "syntax.pdf"  (most basic)
- p runner.py -f "demo.txt" -o "syntax.pdf" -c True -n "Subhaditya Mukherjee" -t "pyGroff" (with cover page)
- Please please look at arguments
- By default, it is assumed that you have images. If you wish to disable it (for more speed), just use -i False
- Check syntax.pdf and demo.txt for an example
- Refer to syntax.pdf for new, easier syntax :)
- This was also generated by the program hehe

## Examples of langauge strings
- python -c (default)
- argument -l
- R -e

## FAQ
- I dont like the cover page
        - If you know a bit of groff (check the links below), you can use "-d False" and then edit whatever you want using groff itself.
        - Then run "groff -ms {infile} -Tpdf > {outfile}" replacing the infile and outfile respectively.

## Contribution guidelines
- Can I contribute?
        - YES
- What to do?
        - Check todo.md
- Restrictions?
        - File an issue first, if it looks useful. Go for it
- Spelling mistakes?
        - I mean sure why not xD

## References
- [Markdown syntax](https://www.markdownguide.org/basic-syntax/)
- [My groff tutorial](https://github.com/SubhadityaMukherjee/groffTutorial)
- [More syntax](https://opensource.com/article/18/2/how-format-academic-papers-linux-groff-me)

