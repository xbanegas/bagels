from test_plus.test import TestCase

from .models import Tag

class TagBaseTest(TestCase):
    def setUp(self):
        self.user = self.make_user('u1')
        self.tag = self.user.tag_set.create(name='test')

    def test__str__(self):
        self.assertEqual(self.tag.__str__(), 'test')
