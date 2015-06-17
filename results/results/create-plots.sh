#!/bin/sh

set -x
set -e

dataset="$1"

python2 generate-dat.py $dataset
rm out* || true
gnuplot recall.gnu
pdflatex out.tex
pdfcrop out.pdf
mv out-crop.pdf ../thesis/figures/$dataset-recall.pdf

rm out* || true
gnuplot precision.gnu
pdflatex out.tex
pdfcrop out.pdf
mv out-crop.pdf ../thesis/figures/$dataset-precision.pdf

rm out* || true
gnuplot fmeasure.gnu
pdflatex out.tex
pdfcrop out.pdf
mv out-crop.pdf ../thesis/figures/$dataset-fmeasure.pdf

rm out* || true
gnuplot fmeasure-avg.gnu
pdflatex out.tex
pdfcrop out.pdf
mv out-crop.pdf ../thesis/figures/$dataset-fmeasure-avg.pdf

cp build/results.tex ../thesis/generated-results-${dataset}.tex
