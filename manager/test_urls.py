from django.core.urlresolvers import reverse, resolve

from test_plus.test import TestCase


class TestManagerUrls(TestCase):

    def setup(self):
        self.user = self.make_user()

    def test_list_reverse(self):
        self.assertEqual(reverse('manager:home'), '/')

    def test_list_resolve(self):
        self.assertEqual(resolve('/').view_name, 'manager:home')

    # @TODO move api to own namespace


    def test_api_bookmarks_reverse(self):
        self.assertEqual(reverse('manager:link_rest_api'), '/api/bookmarks/')

    def test_api_bookmarks_resolve(self):
        self.assertEqual(
            resolve('/api/bookmarks/').view_name, 'manager:link_rest_api'
        )

    def test_api_bookmarks_detail_reverse(self):
        self.assertEqual(
            reverse('manager:link_rest_api_detail', kwargs={ 'id':1 }),
            '/api/bookmarks/1/'
        )

    def test_api_tags_reverse(self):
        self.assertEqual(reverse('manager:tag_rest_api'), '/api/tags/')

    def test_api_tags_resolve(self):
        self.assertEqual(
            resolve('/api/tags/').view_name, 'manager:tag_rest_api'
        )

    def test_api_tags_detail_reverse(self):
        self.assertEqual(
            reverse('manager:tag_rest_api_detail', kwargs={'id':1}),
            '/api/tags/1/'
        )

    def test_api_tags_detail_resolve(self):
        self.assertEqual(
            resolve('/api/tags/1/').view_name, 'manager:tag_rest_api_detail'
        )
