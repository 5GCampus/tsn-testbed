#! /bin/bash

mkdir -p temp_tex
cp main.tex temp_tex/
cd temp_tex
lualatex --enable-write18 main.tex
mv main-figure0.pdf ../plot.pdf
cd ..
rm -rf temp_tex