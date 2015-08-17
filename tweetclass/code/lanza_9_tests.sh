#!/bin/bash

./prepara_test.sh 02$1 model_summary_clean.txt modeled_mixed_scored_tweets.pkl
./prepara_test.sh 03$1 model_summary_clean.txt modeled_mixed_scored_tweets.pkl
./prepara_test.sh 04$1 model_summary_hashtags.txt modeled_mixed_scored_tweets.pkl
./prepara_test.sh 05$1 model_summary_hashtags.txt modeled_mixed_scored_tweets.pkl
./prepara_test.sh 06$1 model_summary_clean.txt modeled_mixed_scored_tweets.pkl
./prepara_test.sh 07$1 model_summary_clean.txt modeled_mixed_scored_tweets.pkl
./prepara_test.sh 08$1 model_summary_hashtags.txt modeled_mixed_scored_tweets.pkl
./prepara_test.sh 09$1 model_summary_hashtags.txt modeled_mixed_scored_tweets.pkl



