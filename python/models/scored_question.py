from datetime import datetime
from math import log


class ScoredQuestion(object):
    #
    # Constants / Config
    #
    MIN_OWNER_REPUTATION    = 25
    MIN_OWNER_ACCEPT_RATE   = 60
    MAX_QUESTION_ANSWERS    = 1
    MIN_QUESTION_SCORE      = 0
    HOUR_SECS               = 60 * 60

    #
    # Class Methods
    #
    @staticmethod
    def from_api_questions(api_questions):
        scored_questions = []

        for api_question in api_questions:
            scored_question = ScoredQuestion(api_question)
            if scored_question.is_valid():
                scored_questions.append(scored_question)

        return scored_questions

    @staticmethod
    def filter_deep_cuts(scored_questions):
        deep_cuts = []

        for scored_question in scored_questions:
            if scored_question.is_deep_cut():
                deep_cuts.append(scored_question)

        return deep_cuts

    @staticmethod
    def order_by_score(scored_questions):
        return sorted(scored_questions, key=lambda q: q.score, reverse=True)

    #
    # Properties
    #
    @property
    def score(self):
        # Score based on an algorithm of your own device. Should return numeric value.
        return self.score_by_rep_age_and_upvotes()

    @property
    def title(self):
        return self.question.title

    @property
    def owner(self):
        return getattr(self.question, 'owner')

    @property
    def owner_reputation(self):
        # In case the API fails to return field.
        if self.owner:
            return getattr(self.owner, 'reputation', self.MIN_OWNER_REPUTATION)
        else:
            return None

    @property
    def owner_accept_rate(self):
        # In case the API fails to return field.
        if self.owner:
            return getattr(self.owner, 'accept_rate', self.MIN_OWNER_ACCEPT_RATE)
        else:
            return None

    @property
    def answer_count(self):
        return self.question.answer_count

    @property
    def created_at(self):
        return self.question.creation_date

    @property
    def age(self):
        return datetime.now() - self.created_at

    @property
    def age_in_hours(self):
        return round(self.age.seconds / self.HOUR_SECS, 2)

    @property
    def tags(self):
        return self.question.tags

    @property
    def url(self):
        return self.question.url

    #
    # Instance Methods
    #
    def __init__(self, api_question):
        self.question = api_question

    def is_valid(self):
        return hasattr(self.question, 'owner')

    def is_answered(self):
        return self.question.is_answered

    def is_deep_cut(self):
        # Might also be called is_worthy().
        return not self.is_answered() and \
               self.owner_reputation >= self.MIN_OWNER_REPUTATION and \
               self.answer_count <= self.MAX_QUESTION_ANSWERS and \
               self.score >= self.MIN_QUESTION_SCORE and \
               self.owner_accept_rate >= self.MIN_OWNER_ACCEPT_RATE

    #
    # Scoring Algorithms
    #
    def score_by_rep_age_and_upvotes(self):
        # Prefer reputable owners with high acceptance rather
        owner_bonus = log(self.owner_reputation, 1.05) * (self.owner_accept_rate / 100.0)

        # Prefer older questions
        age_bonus = log(self.age_in_hours, 1.05)

        # Bonus for question upvotes: 20 pts per net upvote.
        upvote_bonus = self.question.score * 20.0

        # Penalize questions with answers.
        answers_penalty = 1.0 / (self.answer_count + 1)

        # Heavily penalize questions marked answered.
        answered_penalty = 1000 if self.is_answered() else 0

        # TODO: Penalize questions with a lot of comments (as they likely tend toward an answer).
        # The problem: API does not return comment count in results. Requires separate call to
        # questions endpoint to obtain.

        return (owner_bonus + age_bonus + upvote_bonus - answered_penalty) * answers_penalty

    #
    # Magic Methods
    #
    def __repr__(self):
        formatting = """\
<ScoredQuestion @ %s
  title: %s
  is_deep_cut: %s
  score: %s
  answers: %s
  url: %s
  tags: %s,
  age: %s hours>"""

        return formatting % (id(self), self.title, self.is_deep_cut(), self.score,
                             self.answer_count, self.url, self.tags, self.age_in_hours)
