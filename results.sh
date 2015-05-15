#!/bin/sh

run() {
    script="$1"
    dataset="$2"
    feature="$3"
    clustering="$4"
    segmentation="$5"
    similarity="$6"
    corpus="$7"
    size="$8"
    noise="$9"

    outdir="build/$dataset"
    outfile="${outdir}/${feature}-${clustering}-${segmentation}-${similarity}-${corpus}-${size}-${noise/.}.txt"

    mkdir -p $outdir
    echo Computing $outfile
    date > $outfile
    python $script datasets/$dataset $feature $clustering $segmentation $similarity $corpus $size $noise >> $outfile 2>${outfile}.log || echo FAILED
    date >> $outfile
}

run src/execute-configuration.py mirflickr surf som slic lsi images 1000 0.2
run src/execute-configuration.py mirflickr sift som slic lsi images 1000 0.2
run src/execute-configuration.py mirflickr sift kmeans slic lsi images 1000 0.2
run src/execute-configuration.py mirflickr surf kmeans slic lsi images 1000 0.2
run src/execute-configuration.py mirflickr surf kmeans canny lsi images 1000 0.2
run src/execute-configuration.py mirflickr sift kmeans canny lsi images 1000 0.2
run src/execute-configuration.py mirflickr surf kmeans otsu lsi images 1000 0.2
run src/execute-configuration.py mirflickr sift kmeans otsu lsi images 1000 0.2
run src/execute-configuration.py mirflickr surf kmeans slic tfidf images 1000 0.2
run src/execute-configuration.py mirflickr surf kmeans slic ratcliff images 1000 0.2
run src/execute-configuration.py mirflickr surf kmeans slic tfidf segments 1000 0.2
run src/execute-configuration.py mirflickr surf som slic lsi segments 1000 0.1
run src/execute-configuration.py mirflickr surf kmeans slic lsi segments 1000 0.1
run src/execute-configuration.py mirflickr surf kmeans slic lsi segments 1000 0.2
run src/execute-configuration.py mirflickr surf kmeans slic lsi segments 1000 0.4
run src/execute-configuration.py mirflickr surf kmeans canny lsi images 5000 0.2
run src/execute-configuration.py mirflickr surf kmeans canny lsi segments 500 0.2
run src/execute-configuration.py mirflickr surf kmeans canny lsi images 500 0.2
run src/execute-configuration.py mirflickr surf kmeans slic lsi segments 5000 0.2
run src/execute-configuration.py mirflickr surf kmeans slic lsi images 5000 0.2

run src/execute-configuration.py ukbench surf som slic lsi images 1000 0.2
run src/execute-configuration.py ukbench sift som slic lsi images 1000 0.2
run src/execute-configuration.py ukbench sift kmeans slic lsi images 1000 0.2
run src/execute-configuration.py ukbench surf kmeans slic lsi images 1000 0.2
run src/execute-configuration.py ukbench surf kmeans canny lsi images 1000 0.2
run src/execute-configuration.py ukbench sift kmeans canny lsi images 1000 0.2
run src/execute-configuration.py ukbench surf kmeans otsu lsi images 1000 0.2
run src/execute-configuration.py ukbench sift kmeans otsu lsi images 1000 0.2
run src/execute-configuration.py ukbench surf kmeans slic tfidf images 1000 0.2
run src/execute-configuration.py ukbench surf kmeans slic ratcliff images 1000 0.2
run src/execute-configuration.py ukbench surf kmeans slic tfidf segments 1000 0.2
run src/execute-configuration.py ukbench surf som slic lsi segments 1000 0.1
run src/execute-configuration.py ukbench surf kmeans slic lsi segments 1000 0.1
run src/execute-configuration.py ukbench surf kmeans slic lsi segments 1000 0.2
run src/execute-configuration.py ukbench surf kmeans slic lsi segments 1000 0.4
run src/execute-configuration.py ukbench surf kmeans canny lsi images 5000 0.2
run src/execute-configuration.py ukbench surf kmeans canny lsi segments 500 0.2
run src/execute-configuration.py ukbench surf kmeans canny lsi images 500 0.2
run src/execute-configuration.py ukbench surf kmeans slic lsi segments 5000 0.2
run src/execute-configuration.py ukbench surf kmeans slic lsi images 5000 0.2
