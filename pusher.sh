black "."
python runner.py -f "demo.txt" -o "syntax.pdf" -c True -n "Subhaditya Mukherjee" -t "pyGroff" -w True
pdoc --force --html -o docs pygroff
mv docs/pygroff/index.html docs/index.md
mv docs/pygroff/* docs/
if [[ ! -z $1 ]]; then
        git add . && git commit -m $1 && git push
fi
