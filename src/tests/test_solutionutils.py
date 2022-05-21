from unittest import TestCase
from src.utils.solutionutils import get_project_root


class Test(TestCase):
    def test_get_project_root(self):
        self.assertTrue(isinstance(get_project_root(), str))
