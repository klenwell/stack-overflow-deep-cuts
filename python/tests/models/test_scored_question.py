from unittest import TestCase
from unittest import skip

from models.scored_question import ScoredQuestion



class ScoredQuestionModelTest(TestCase):

    def test_expects_to_instantiate_scored_question(self):
        api_question = None
        scored_question = ScoredQuestion(api_question)
        self.assertIsInstance(scored_question, ScoredQuestion)
        self.assertFalse(scored_question.is_valid())
