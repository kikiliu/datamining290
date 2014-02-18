from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    ###
    # TODO: write the functions needed to
    # 1) find potential matches,
    # 2) calculate the Jaccard between users, with a user defined as a set of
    # reviewed businesses
    ##/

    def extract_user_biz(self, _, record):
        """Take in record and yield <user, business>"""
        if record['type'] == 'review':
            yield record['user_id'], record['business_id']

    def merge_user(self, user_id, biz_ids):
        """merge all business record for each user"""
        business_list = sorted(list(biz_ids))
        yield None, (user_id, business_list)

    def calc_similarity(self, _, users_biz):
        """calculate the similarity of each pair and yield those with >=0.5 similarity"""
        users_list = list(users_biz)
        users_count = len(users_list)
        for i in range(users_count-1):
            for j in range(i+1, users_count):
                biz_list1 = users_list[i][1]
                biz_list2 = users_list[j][1]
                common = 0
                k1=0
                k2=0
                while k1<len(biz_list1) and k2<len(biz_list2):
                    if biz_list1[k1] == biz_list2[k2]:
                        common += 1
                        k1 += 1
                        k2 += 1
                    elif biz_list1[k1] < biz_list2[k2]:
                        k1 += 1
                    else:
                        k2 += 1

                similarity = 1.0 * common / (len(biz_list1) + len(biz_list2) - common)
                if similarity >= 0.5:
                    yield (users_list[i][0], users_list[j][0]), similarity

    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        mapper1: <line, record> => <user_id, biz_id>
        reducer1: <user_id, [biz_id, ...] => <None, (user_id, set(biz_id, ...))>
        reducer2: <None, (user_id, set(biz_id, ...))> => <users_pair, similarity>
        """
        return [
            self.mr(mapper=self.extract_user_biz, reducer=self.merge_user),
            self.mr(reducer=self.calc_similarity)
        ]


if __name__ == '__main__':
    UserSimilarity.run()