#!/bin/sh
set -eux
python simple_fe.py
crfsuite learn -m mymodel train.feats > train.log
crfsuite tag -m mymodel dev.feats > predtags
python tageval.py dev.txt predtags
