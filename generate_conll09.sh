#!/bin/sh
echo "Merging semantic annotations to new IMST file"
python update09Semantics.py -oldPBFile './IO/trpb_v1.1.conll' -newIMSTFile './IO/imst141.single.tree.conll' -save_dir './IO'
echo "Arranging column orders for SRL tool"
python add_cols.py -annImstFile './IO/merged.conll'
echo "Splitting to train, dev, test"
python split.py -pbfile './IO/merged.conll.aug'
echo "Done"
