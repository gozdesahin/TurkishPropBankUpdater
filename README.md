# TurkishPropBankUpdater
To make newer versions of existing semantic annotation layer


# First run update09Semantics code, because we need to match sentences first
python update09Semantics.py -oldPBFile './trpb_v1.1.conll' -newIMSTFile './new_imst.conll' -save_dir './mapping_output'

# Then you can map UD file too
python update09Semantics.py -oldPBUDFile './trpb_v1.1.conllu' -newIMSTUDFile './new_imst.conllu' -mappingFile './final_sent_map' -save_dir './mapping_output'
