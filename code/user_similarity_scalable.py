from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    SORT_VALUES = True

    def map_input(self, _, record):
        """Take in record and yield <business, user>"""
        if record['type'] == 'review':
            yield record['business_id'], record['user_id']

    def reduce_pairup(self, business_id, user_ids):
        """build up co-exisiting users pair and yield <pair, 1>"""
        self.increment_counter("total", "businesses")
        user_ids = list(user_ids)   #scale?
        for i in range(len(user_ids)):
            for j in range(len(user_ids)):
                if user_ids[i] <= user_ids[j]: #lower time complexity from the comparision of two sets
                    self.increment_counter("total", "pairs")
                    yield (user_ids[i], user_ids[j]), 1

    def reduce_count_pair(self, users_pair, occurances):  
        """count total number of each pair"""
        if users_pair[0] == users_pair[1]:
            self.increment_counter("total", "users")
            yield None, (0, users_pair[0], sum(occurances))
        else:
            self.increment_counter("total", "pairs")
            yield None, (1, users_pair, sum(occurances))

    def reduce_calc_similarity(self, _, dataset):
        user_count_dict = {}
        for data in dataset:
            if data[0] == 0:
                user = data[1]
                count = data[2]
                user_count_dict[user] = count
            else:
                user1 = data[1][0]
                user2 = data[1][1]
                if user1 in user_count_dict and user2 in user_count_dict:
                    common = data[2]
                    union = user_count_dict[user1] + user_count_dict[user2] - common
                    similarity = common*1.0/union
                    if similarity>= 0.5:
                        yield (user1, user2), similarity
                else:
                    self.increment_counter("total", "miss")

    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        mapper1: <line, record> => <businsess_id, user_id>
        reducer1: <businsess_id, [user_id, ...] => <users_pair, 1>
        reducer2: <users_pair, [1, 1, ...] => <users_pair, total_counts>
        mapper3: <users_pair, total_counts> => <[user_id1, user_id2], similarity]
        """
        return [
            self.mr(mapper=self.map_input, reducer=self.reduce_pairup),
            self.mr(reducer=self.reduce_count_pair),
            self.mr(reducer=self.reduce_calc_similarity)
        ]


if __name__ == '__main__':
    UserSimilarity.run()