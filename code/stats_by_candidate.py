#### Extra credit question
from stats import build_candidate_dict, calc_stats

if __name__ == "__main__":

	candidate_amt_dict = build_candidate_dict()
	candidate_stats_dict = {}
	amt_list_by_id = []
	for cid in candidate_amt_dict.keys():
		candidate_stats_dict[cid] = calc_stats(candidate_amt_dict[cid])
		amt_list_by_id.append(candidate_stats_dict[cid][0])
	stats_by_id = calc_stats(amt_list_by_id)
	mean_by_id = stats_by_id[3]
	sd_by_id = stats_by_id[5]
	for (key, stats) in candidate_stats_dict.items():
		print "Candidate: %s, Total: %s, Minimum: %s, Maximum: %s, Mean: %.2f, Median: %s, Standard Deviation: %.2f, Z-score: %r" % (key, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], (stats[0]-mean_by_id)/sd_by_id)