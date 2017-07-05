from datetime import datetime


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
    def filter_search_results(questions, sort=True):
        scored_questions = []

        for question in questions:
            scored_question = ScoredQuestion(question)
            if scored_question.is_valid() and scored_question.is_deep_cut():
                scored_questions.append(scored_question)

        if sort:
            scored_questions = sorted(scored_questions, key=lambda q: q.score, reverse=True)

        return scored_questions

    #
    # Properties
    #
    @property
    def score(self):
        """Scores question based on a subjective formula of your device.
        TODO: include comments as factor since a lot of questions get resolved in
        comments before any answer submitted.
        """
        score = 0.0

        # Bonuses
        score += float(self.age.seconds) / (24 * self.HOUR_SECS) * 100
        score += self.owner_reputation / 20.0
        score += self.question.score * 20.0
        score += self.owner_accept_rate

        # Penalties
        answer_count_penalty = self.answer_count * 500.0
        score = max(score - answer_count_penalty, self.MIN_QUESTION_SCORE + 1)

        return int(score)

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
    def __init__(self, stack_question):
        self.question = stack_question

    def is_answered(self):
        return self.question.is_answered

    def is_valid(self):
        return hasattr(self.question, 'owner')

    def is_deep_cut(self):
        # Might also be called is_worthy().
        return not self.is_answered() and \
               self.owner_reputation >= self.MIN_OWNER_REPUTATION and \
               self.answer_count <= self.MAX_QUESTION_ANSWERS and \
               self.score >= self.MIN_QUESTION_SCORE and \
               self.owner_accept_rate >= self.MIN_OWNER_ACCEPT_RATE

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
