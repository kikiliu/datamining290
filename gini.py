#!/usr/bin/python
"""Script can be used to calculate the Gini Index of a column in a CSV file.
'.'
Classes are strings."""

import fileinput
import csv
from collections import defaultdict, Counter


def calc_gini(a, b):
    if (a + b) > 0:
        gini = 1 - 1.0*(a**2 + b**2)/(a+b)**2 #float to start, not work at the end
        return gini
    else:
        return -1

#mapping attribute to names
(
    CMTE_ID, AMNDT_IND, RPT_TP, TRANSACTION_PGI, IMAGE_NUM, TRANSACTION_TP,
    ENTITY_TP, NAME, CITY, STATE, ZIP_CODE, EMPLOYER, OCCUPATION,
    TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID, CAND_ID, TRAN_ID, FILE_NUM,
    MEMO_CD, MEMO_TEXT, SUB_ID
) = range(22)

CANDIDATES = {
    'P80003338': 'Obama',
    'P80003353': 'Romney',
}

############### Set up variables
# TODO: declare datastructures
oba_zip_dic = defaultdict(int)
rom_zip_dic = defaultdict(int)
zip_set = Counter()
oba_count = 0
rom_count = 0
############### Read through files
for row in csv.reader(fileinput.input(), delimiter='|'):
    candidate_id = row[CAND_ID]
    if candidate_id not in CANDIDATES:
        continue

    candidate_name = CANDIDATES[candidate_id]
    zip_code = row[ZIP_CODE]
    ###
    # TODO: save information to calculate Gini Index
    ##/
    zip_set.update([zip_code])
    if candidate_name == 'Obama':
        oba_count += 1
        oba_zip_dic[zip_code] += 1
    else:
        rom_count += 1
        rom_zip_dic[zip_code] += 1
###
# TODO: calculate the values below:
gini = 0  # current Gini Index using candidate name as the class
split_gini = 1  # weighted average of the Gini Indexes using candidate names, split up by zip code
##/
##gini stands for the worst case 
gini = calc_gini(oba_count,rom_count)

for zip_code in zip_set.keys():
    if zip_code in oba_zip_dic.keys():
        oba_zip_count = oba_zip_dic[zip_code]
    else:
        oba_zip_count = 0
    if zip_code in rom_zip_dic.keys():
        rom_zip_count = rom_zip_dic.get(zip_code)
    else:
        rom_zip_count = 0
    zip_count = oba_zip_count + rom_zip_count
    total_count = oba_count + rom_count    
    zip_gini = calc_gini(oba_zip_count, rom_zip_count)
    rest_gini = calc_gini(oba_count - oba_zip_count, rom_count - rom_zip_count)
    weighted_gini = (zip_gini * zip_count + rest_gini * (total_count - zip_count)) / total_count
    if weighted_gini < split_gini:
        split_gini = weighted_gini

print "Gini Index: %s" % gini
print "Gini Index after split: %s" % split_gini