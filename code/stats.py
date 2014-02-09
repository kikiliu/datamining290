#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from ftp://ftp.fec.gov/FEC/2012/pas212.zip - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""

import fileinput
import csv

total = 0.0
trans_amt_list = []
median = 0.0
mean = 0.0
variance = 0.0
candidate_dict = {}
for row in csv.reader(fileinput.input(), delimiter='|'):
    # if not fileinput.isfirstline():
    transaction_amt = float(row[14])
    total += transaction_amt
    trans_amt_list.append(transaction_amt)
    if row[16] != "" and candidate_dict.get(row[16]) is None:
    	candidate_dict[row[16]] = 1
        ###
        # TODO: calculate other statistics here
        # You may need to store numbers in an array to access them together
        ##/
###
# TODO: aggregate any stored numbers here
#
##/
# Get min, max and median of transaction amount list
trans_amt_list.sort()
count = len(trans_amt_list)
mean = total/float(count)
if count%2 == 0:
	median = (trans_amt_list[count/2 - 1] + trans_amt_list[count/2])/2
else:
	median = trans_amt_list[count/2]
# Calculate SD
for amt in trans_amt_list:
	variance += (amt - mean)**2/count


##### Print out the stats
print "Total: %s" % total
print "Minimum: %s" % trans_amt_list[0]
print "Maximum: %s" % trans_amt_list[-1]
print "Mean: %.2f" % mean
print "Median: %s" % median
# square root can be calculated with N**0.5
print "Standard Deviation: %.2f" % (variance**0.5)

##### Comma separated list of unique candidate ID numbers
print "Candidates: %s unique candidate ID numbers" % len(candidate_dict.keys())
print ",".join(candidate_dict.keys())

def minmax_normalize(value):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normilzation should use the min and max amounts from the full dataset"""
    ###
    # TODO: replace line below with the actual calculations
    norm = (value - trans_amt_list[0])/(trans_amt_list[-1] - trans_amt_list[0])
    ###/
    return norm

##### Normalize some sample values
print "Min-max normalized values: %r" % map(minmax_normalize, [2500, 50, 250, 35, 8, 100, 19])
