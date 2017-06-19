from test_plus.test import TestCase


class TestBookmark(TestCase):

    def setUp(self):
        self.user = self.make_user('u1')
        self.bookmark = self.user.bookmark_set.create(url='https://foo.com', title='foo')

    def test__str__(self):
        self.assertEqual(self.bookmark.title, 'foo')

