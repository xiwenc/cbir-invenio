#!/bin/sh

set -x
set -e

python plots/generate-tags.py
rm out* || true
gnuplot plots/tags.gnu
pdflatex out.tex
pdfcrop out.pdf
mv out-crop.pdf thesis/figures/mirflickr-tags.pdf

python plots/generate-dat.py mirflickr
rm out* || true
gnuplot plots/recall.gnu
pdflatex out.tex
pdfcrop out.pdf
mv out-crop.pdf thesis/figures/mirflickr-recall.pdf

rm out* || true
gnuplot plots/precision.gnu
pdflatex out.tex
pdfcrop out.pdf
mv out-crop.pdf thesis/figures/mirflickr-precision.pdf

rm out* || true
gnuplot plots/fmeasure.gnu
pdflatex out.tex
pdfcrop out.pdf
mv out-crop.pdf thesis/figures/mirflickr-fmeasure.pdf

rm out* || true
gnuplot plots/fmeasure-avg.gnu
pdflatex out.tex
pdfcrop out.pdf
mv out-crop.pdf thesis/figures/mirflickr-fmeasure-avg.pdf

cp build/results.tex thesis/generated-results-mirflickr.tex

python plots/mirflickr-detail.py build/mirflickr/surf-kmeans-slic-lsi-segments-1000-04.txt > thesis/generated-mirflickr-surf-kmeans-slic-lsi-segments-1000-04.tex
python plots/mirflickr-detail.py build/mirflickr/surf-kmeans-slic-lsi-segments-1000-02.txt > thesis/generated-mirflickr-surf-kmeans-slic-lsi-segments-1000-02.tex
python plots/mirflickr-detail.py build/mirflickr/sift-kmeans-canny-lsi-images-1000-02.txt > thesis/generated-mirflickr-sift-kmeans-canny-lsi-images-1000-02.tex
python plots/mirflickr-detail.py build/mirflickr/surf-kmeans-canny-lsi-images-500-02.txt > thesis/generated-mirflickr-surf-kmeans-canny-lsi-images-500-02.tex

python plots/generate-dat.py ukbench
rm out* || true
gnuplot plots/recall.gnu
pdflatex out.tex
pdfcrop out.pdf
mv out-crop.pdf thesis/figures/ukbench-recall.pdf

rm out* || true
gnuplot plots/precision.gnu
pdflatex out.tex
pdfcrop out.pdf
mv out-crop.pdf thesis/figures/ukbench-precision.pdf

rm out* || true
gnuplot plots/fmeasure.gnu
pdflatex out.tex
pdfcrop out.pdf
mv out-crop.pdf thesis/figures/ukbench-fmeasure.pdf

rm out* || true
gnuplot plots/fmeasure-avg.gnu
pdflatex out.tex
pdfcrop out.pdf
mv out-crop.pdf thesis/figures/ukbench-fmeasure-avg.pdf

cp build/results.tex thesis/generated-results-ukbench.tex
python plots/compare.py build/ukbench/surf-kmeans-slic-tfidf-images-1000-02.txt build/ukbench/surf-kmeans-slic-tfidf-segments-1000-02.txt > thesis/generated-ukbench-segments-images.tex
