#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from ftp://ftp.fec.gov/FEC/2012/pas212.zip - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""

import fileinput
import csv
trans_amt_list = []

def build_candidate_dict():
    candidate_dict = {}
    for row in csv.reader(fileinput.input(), delimiter='|'):
        # if not fileinput.isfirstline():
        if row[14] != "":
            transaction_amt = float(row[14])
            trans_amt_list.append(transaction_amt)

            # ignore the transaction_amt without corresponding candidate ID
            if row[16] != "":
                if candidate_dict.get(row[16]) is None:
                    candidate_dict[row[16]] = [transaction_amt]
                else:
                    candidate_dict[row[16]].append(transaction_amt)
    return candidate_dict


def calc_stats(amt_list):

    amt_list.sort()
    minimum = amt_list[0]
    maximum = amt_list[-1]

    total = sum(amt_list)
    count = len(amt_list)
    mean = total/float(count)

    # Calculate median
    if count%2 == 0:
        median = (amt_list[count/2 - 1] + amt_list[count/2])/2
    else:
        median = amt_list[count/2]

    # Calculate SD
    sd = sum([(amt - mean)**2/count for amt in amt_list])**0.5

    return (total, minimum, maximum, mean, median, sd)    

def minmax_normalize(value):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normilzation should use the min and max amounts from the full dataset"""
    ###
    # TODO: replace line below with the actual calculations
    norm = (value - trans_amt_list[0])/(trans_amt_list[-1] - trans_amt_list[0])
    ###/
    return norm

if __name__ == "__main__":
        ###
        # TODO: calculate other statistics here
        # You may need to store numbers in an array to access them together
        ##/
###
# TODO: aggregate any stored numbers here
##
# Get min, max and median of transaction amount list
    candidate_dict = build_candidate_dict()
    stats = calc_stats(trans_amt_list) #trans_amt_list will be sorted in this step
                                       #then can be used in minmax_normalize
    ##### Print out the stats
    print "Total: %s" % stats[0]
    print "Minimum: %s" % stats[1]
    print "Maximum: %s" % stats[2]
    print "Mean: %.2f" % stats[3]
    print "Median: %s" % stats[4]
    # square root can be calculated with N**0.5
    print "Standard Deviation: %.2f" % stats[5]

    ##### Comma separated list of unique candidate ID numbers
    print "Candidates: %s unique candidate ID numbers" % len(candidate_dict.keys())
    print ",".join(candidate_dict.keys())

    ##### Normalize some sample values
    print "Min-max normalized values: %r" % map(minmax_normalize, [2500, 50, 250, 35, 8, 100, 19])