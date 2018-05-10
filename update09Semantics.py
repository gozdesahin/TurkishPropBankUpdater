#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gözde Gül Şahin'

from merger import *
import pickle
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='update09Semantics.py')

    ## Data options
    parser.add_argument('-oldPBFile', type=str,
                        default='/media/isguderg/Work/Doktora/Data Sets/Yeni_IMST/pb/09/trpb_v1.1.conll',
                        help='Türkçe anlamsal etiketlemelerin olduğu dosya')

    parser.add_argument('-newIMSTFile', type=str,
                        default='./IO/imst141.single.tree.conll',
                        help='Yeni IMST dosyası')

    parser.add_argument('-save_dir', type=str,
                        default='/home/isguderg/Documents/mapping_output',
                        help='Kaydedilecek yer')

    opt = parser.parse_args()
    mapSemanticsToIMST(opt)


def mapSemanticsToIMST(opt):
    sents09_old = getConll09Sents(opt.oldPBFile)
    sents09_new = getConll09SentNoAnnot(opt.newIMSTFile)

    sentence_map = {}
    no_matched_sents = []
    print "********************************************************"
    print "First matching sentences - because they are not in order"
    print "********************************************************"

    # First Round
    for sent in sents09_new:
        match_ix = get_matching_sentence(sent, sents09_old, sentence_map)
        if match_ix!=-1:
            if match_ix in sentence_map:
                print "Warning: There was a match before"
            else:
                sentence_map[match_ix] = sent.idx
        else:
            print "No match found for: ",sent.idx
            no_matched_sents.append(sent.idx-1)

    print "Total match count after 1st round: ",len(sentence_map)
    print "Total not matched after 1st round: ", len(sents09_new)-len(sentence_map)
    pickle.dump(sentence_map, open("sent_map_first.pkl", "wb" ) )
    pickle.dump(no_matched_sents, open("no_match.pkl", "wb" ) )

    # Second Round
    sentence_map = pickle.load(open("sent_map_first.pkl", "rb"))
    no_matched_sents = pickle.load(open("no_match.pkl", "rb"))
    still_no_match = []
    for ix in no_matched_sents:
        sent = sents09_new[ix]
        match_ix = get_matching_sentence_tolerant(sent, sents09_old, sentence_map)
        if match_ix!=-1:
            if match_ix in sentence_map:
                print "Warning: There was a match before"
            else:
                sentence_map[match_ix] = sent.idx
        else:
            print "No match found for: ",sent.idx
            still_no_match.append(sent.idx-1)

    print "Total match count after 2nd round: ",len(sentence_map)
    print "Total not matched after 2nd round: ", len(sents09_new)-len(sentence_map)
    pickle.dump(sentence_map, open("sent_map_second.pkl", "wb"))
    pickle.dump(still_no_match, open("no_match_second.pkl", "wb"))

    # Third Round
    sentence_map = pickle.load(open("sent_map_second.pkl", "rb"))
    no_matched_sents = pickle.load(open("no_match_second.pkl", "rb"))
    still_no_match = []
    for ix in no_matched_sents:
        sent = sents09_new[ix]

        match_ix = get_matching_sentence_very_tolerant(sent, sents09_old, sentence_map)
        if match_ix!=-1:
            if match_ix in sentence_map:
                print "Warning: There was a match before"
            else:
                sentence_map[match_ix] = sent.idx
        else:
            print "No match found for: ",sent.idx
            print_sentence(sent)
            still_no_match.append(sent.idx-1)

    print "Total match count after 3rd round: ",len(sentence_map)
    print "Total not matched after 3rd round: ", len(sents09_new)-len(sentence_map)
    pickle.dump(sentence_map, open("final_sent_map.pkl", "wb"))
    pickle.dump(still_no_match, open("no_match_third.pkl", "wb"))

    print "Saving sentence index mapping to final sent map pickle file"

    # Now transfering annotation
    save_dir = opt.save_dir
    try:
        os.stat(save_dir)
    except:
        os.mkdir(save_dir)

    fIn09_wsemantic = os.path.join(save_dir, "merged.conll")
    fIn09_osemantic = os.path.join(save_dir, "semantic_layer.conll")

    # sentence_map[old_sentence_index]=new_sentence_index
    sentence_map = pickle.load(open("final_sent_map.pkl", "rb"))

    # Remove other files
    os.remove("sent_map_first.pkl")
    os.remove("no_match.pkl")
    os.remove("sent_map_second.pkl")
    os.remove("no_match_second.pkl")
    os.remove("no_match_third.pkl")

    # sentence_map[new_sentence_index]=old_sentence_index
    reverse_sentence_map = reverse_dict(sentence_map)
    annotated_sents = []
    semantic_fields = []
    for i in range(len(sents09_new)):
        nidx = (i + 1)
        sent_new = sents09_new[nidx - 1]
        if nidx in reverse_sentence_map:
            oidx = reverse_sentence_map[nidx]
            sent_old = sents09_old[oidx - 1]
            annot_sent, ann = transfer_annot_simple(sent_old, sent_new)
            annotated_sents.append(annot_sent)
            semantic_fields.append(ann)
        # No annotation exists for the sentence, just add two columns then
        else:
            annot_sent, ann = annotate_dummy(sent_new)
            annotated_sents.append(annot_sent)
            semantic_fields.append(ann)

    assert len(annotated_sents) == len(sents09_new)
    assert len(semantic_fields) == len(sents09_new)

    # write merged file
    writeToFile(fIn09_wsemantic, annotated_sents)

    # write semantic fields only
    writeToFile(fIn09_osemantic, semantic_fields)
    print "Done mapping, check output folder"

if __name__ == "__main__":
    main()