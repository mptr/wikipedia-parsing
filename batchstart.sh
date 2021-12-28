#!/bin/bash

i=0;
for f in xmls/*; do
    ((i=i+1))
    name=$(printf "enwiki%03d" $i)
    echo "File -> $f - $name"
    screen -dmS $name bash -c ".venv/bin/python parse_wiki.py $f; exec bash"
done
