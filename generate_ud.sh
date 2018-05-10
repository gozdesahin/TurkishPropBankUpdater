#!/bin/sh
echo "Merging semantic annotations to new IMST-UD file"
python updateUDSemantics.py -oldPBUDFile './IO/trpb_ud_v1.1.conllu' -newIMSTUDFile './IO/imst141.single.conllu.trimmed' -mappingFile './final_sent_map.pkl' -save_dir './IO'
echo "Splitting to train, dev, test"
python split.py -pbfile './IO/merged.conllu'
echo "Done"
