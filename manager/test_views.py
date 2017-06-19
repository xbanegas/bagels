from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from test_plus.test import TestCase

from .views import index


class BaseManagerTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user('u1')
        self.factory = RequestFactory()


class TestIndexLoginRequired(BaseManagerTestCase):

    def test_home_redirects_anon(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = index(request)
        self.response_302(response)

    def test_home_renders_to_user(self):
        request = self.factory.get('/')
        request.user = self.user
        # @TODO work around template error
        response = index(request)
        self.assertEqual(response.status_code, 200)

class TestDuplicateBookmark(BaseManagerTestCase):

    def setUp(self):
        super(TestDuplicateBookmark, self).setUp()

        self.bookmark = self.user.bookmark_set.create(url='https://foo.com/')
        self.user2 = self.make_user('u2')
        self.bookmark2 = self.user2.bookmark_set.create(url='https://bar.uk/')

    def test_duplicate_rejected(self):
        pass

    def test_duplicates_across_users(self):
        pass
