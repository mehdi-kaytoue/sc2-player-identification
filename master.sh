#/bin/bash

python 01-replay-parser.py replay-data/WCS_2014_season_2 100 100 replay_traces.txt \
&& python 02-features-extraction.py replay_traces.txt replay-features.txt 30\
&& python 03-model-learner.py replay-features.txt

