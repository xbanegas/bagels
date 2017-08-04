from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from test_plus.test import TestCase

from .views import index, bookmark_detail

def insert_sessions(request):
    from django.contrib.messages.storage.fallback import FallbackStorage
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)


class BaseManagerTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user('u1')
        self.factory = RequestFactory()


class TestIndex(BaseManagerTestCase):

    def test_index_response(self):
        request = self.factory.get('/')
        request.user = self.user
        response = index(request)
        self.response_200(response)

    def test_index_post_response(self):
        request = self.factory.post('/', {'url': 'https://bar.uk/'})
        request.user = self.user
        response = index(request)
        self.response_200(response)

    def test_index_post_error(self):
        request = self.factory.post('/', {'url': ''})
        request.user = self.user
        insert_sessions(request)
        response = index(request)
        self.assertEqual(response.status_code, 400)


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
        request = self.factory.post('/', {'url': 'https://foo.com/'})
        request.user = self.user
        insert_sessions(request)
        response = index(request)
        self.assertEqual(response.status_code, 400)

    def test_duplicates_across_users(self):
        request = self.factory.post('/', {'url': 'https://foo.com/'})
        request.user = self.user2
        response = index(request)
        self.assertEqual(response.status_code, 200)


class TestBookmarkDetail(BaseManagerTestCase):

    def setUp(self):
        super(TestBookmarkDetail, self).setUp()
        self.bookmark = self.user.bookmark_set.create(url='https://foo.com/')

    def test_bookmark_detail_response(self):
        bookmark_id = self.bookmark.pk
        request = self.factory.get('/bookmark/{}/'.format(bookmark_id))
        request.user = self.user
        response = bookmark_detail(request, bookmark_id)
        self.response_200(response)

    def test_bookmark_detail_post(self):
        bookmark_id = self.bookmark.pk
        bookmark_url = self.bookmark.url
        request = self.factory.post('/bookmark/{}/'.format(bookmark_id),
                                    {
                                        'url': '{}'.format(bookmark_url),
                                        'title': 'foo'
                                    }
                                    )
        request.user = self.user
        insert_sessions(request)
        response = bookmark_detail(request, bookmark_id)
        self.response_200(response)
