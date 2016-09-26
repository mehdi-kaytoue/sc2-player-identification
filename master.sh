#/bin/bash

python 01-replay-parser.py replay-data/Whitera_replay_pack 100 100 replay_traces.txt
python 02-features-extraction.py replay_traces.txt replay-features.txt
python 03-model-learner.py replay-features.txt

