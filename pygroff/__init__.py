"""Hello! This little library is a wrapper around groff. It will save your tears when you need to make any pdfs and word documents with more complex formatting done super easily for you. Do you know markdown already? Wow! you already know most of the syntax :)

1. Features of the library
- Write in a text file
- Add code. And get execution results directly! (No images. And no imports for now.)
- Get a cover page as well :)
- Get a Table of contents. (Due to limitations : its only on the last page for now.)
- Easy tables (Aint nobody got time for complicated ones)
- You can get a word document too (you do need libreoffice for it)
- Get auto generated, beautifully formatted pdfs and docs instantly
- Not cry because you moved an image and now your document is in hieroglyphics
- You can also write in groff syntax in the file. It will work as well. Just in case you need something extra

2. Arguments:
    -f : Input file path
    -o : Output file path
    -toc : Add table of contents : true/false
    -cov : Add cover page : true/false
    -w : Convert to word : true/false
    -n : Name for cover page 
    -t : Title for cover page
    -e : Execute and output code : true/false
    -i : Are there images : true/false
    -df : Custom date format : python strftime format
    -d : Delete intermediates or not
    -lang : custom language execute script. eg : python -c

3. For syntax, refer to syntax.pdf or syntax.docx
"""
