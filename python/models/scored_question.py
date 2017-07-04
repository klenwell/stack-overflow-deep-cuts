class ScoredQuestion(object):

    #
    # Class Methods
    #
    @staticmethod
    def filter_search_results(questions):
        scored_questions = []

        try:
            for question in questions:
                scored_question = ScoredQuestion(question)
                if scored_question.is_deep_cut():
                    scored_questions.append(scored_question)
        except Exception as e:
            print('Hit error filtering search results: %s. Stop and return scored questions now.', e)
        finally:
            return scored_questions

    #
    # Properties
    #
    @property
    def title(self):
        return self.question.title

    @property
    def score(self):
        return 0

    #
    # Instance Methods
    #
    def __init__(self, stack_question):
        self.question = stack_question

    def is_deep_cut(self):
        return True

    def __repr__(self):
        return "<ScoredQuestion '%s' (score: %s) at %s>" % (self.title, self.score, id(self))
