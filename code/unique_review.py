from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import re

WORD_RE = re.compile(r"[\w']+")


class UniqueReview(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    def extract_words(self, _, record):
        """Take in a record, yield <word, review_id>"""
        if record['type'] == 'review':
            ###
            # TODO: for each word in the review, yield the correct key,value
            # pair:
            for word in WORD_RE.findall(record['text']):
              yield [word, record['review_id']]
            ##/

    def count_reviews(self, word, review_ids):
        """Count the number of reviews a word has appeared in.  If it is a
        unique word (ie it has only been used in 1 review), output that review
        and 1 (the number of words that were unique)."""

        unique_reviews = set(review_ids)  # set() uniques an iterator
        ###
        # TODO: yield the correct pair when the desired condition is met:
        if len(unique_reviews) == 1:
            yield [next(iter(unique_reviews)), 1]
        ##/

    def count_unique_words(self, review_id, unique_word_counts):
        """Output the number of unique words for a given review_id"""
        ###
        # TODO: summarize unique_word_counts and output the result
        yield [review_id, sum(unique_word_counts)]
        ##/

    def aggregate_max(self, review_id, unique_word_count):
        """Group reviews/counts together by the MAX statistic."""
        ###
        # TODO: By yielding using the same keyword, all records will appear in
        # the same reducer:
        yield ["MAX", [unique_word_count, review_id]]
        ##/

    def select_max(self, stat, count_review_ids):
        """Given a list of pairs: [count, review_id], select on the pair with
        the maximum count, and output the result."""
        ###
        # TODO: find the review with the highest count, yield the review_id and
        # the count. HINT: the max() function will compare pairs by the first
        # number
        max_count_review_id = max(count_review_ids)
        yield max_count_review_id
        #/

    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        mapper1: <line, record> => <word, review_id>
        reducer1: <word, [review_id,...]> => <review_id, 1>
        reducer2: <review_id, [1,...]> => <review_id, total_count_of_unique_word>
        mapper3: <review_id, total_count_of_unique_word> => <"max", [[total_count_of_unique_word, review_id],...]>
        reducer3: <"max", [[total_count_of_unique_word, review_id],...]> => <max_review_id, count>
        """
        return [
            self.mr(self.extract_words, self.count_reviews),
            self.mr(reducer=self.count_unique_words),
            self.mr(self.aggregate_max, self.select_max)
        ]


if __name__ == '__main__':
    UniqueReview.run()
