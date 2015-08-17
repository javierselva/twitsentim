#!/bin/bash

if [ ! -d "summary_test_files" ]; then
    mkdir "summary_test_files"
fi

if [ -d "summary_test_files/summary_model_"$1 ]; then
    rm -r "summary_test_files/"*$1
fi


MAIN_FOLDER="summary_test_files/"
mkdir $MAIN_FOLDER"summary_model_"$1
mkdir $MAIN_FOLDER"summary_results_"$1
mkdir $MAIN_FOLDER"summary_rouge_results_"$1
mkdir $MAIN_FOLDER"summary_raw_"$1

cp summary_test_files/$2 summary_test_files/summary_model_$1/manual_summary.txt
cp summary_test_files/$3 summary_test_files/summary_raw_$1/original_tweets.pkl

python summary_test.py $1 > summary_test_files/summary_rouge_results_$1/resultados.html 2>esto_es_una_prueba.txt 

