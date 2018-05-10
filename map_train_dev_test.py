from merger import *
import pickle


ud_all = None #"/media/isguderg/Work/Doktora/Data Sets/Yeni_IMST/imst_son/09/imst141.single.conll"
ud_shuffled = None #"/media/isguderg/Work/Doktora/Data Sets/Yeni_IMST/imst_son/09/imst141.single.conll.test"

sentsud_all = getConll09SentNoAnnot(ud_all)
sentsud_sff = getConll09SentNoAnnot(ud_shuffled)

sentence_map = {}
no_matched_sents = []

for sent in sentsud_sff:
    match_ix = get_matching_sentence(sent, sentsud_all, sentence_map)
    if match_ix != -1:
        if match_ix in sentence_map:
            print "Warning: There was a match before"
        else:
            sentence_map[match_ix] = sent.idx
    else:
        print "No match found for: ", sent.idx
        print_sentence(sent)
        no_matched_sents.append(sent.idx - 1)

print "Total match count after 1st round: ", len(sentence_map)
print "Total number of sentences: ", len(sentsud_sff)
pickle.dump(sentence_map, open("sent_map_test.pkl", "wb"))
