from django.core.urlresolvers import reverse, resolve

from test_plus.test import TestCase


class TestManagerUrls(TestCase):

    def setup(self):
        self.user = self.make_user()

    def test_list_reverse(self):
        self.assertEqual(reverse('manager:home'), '/')

    def test_list_resolve(self):
        self.assertEqual(resolve('/').view_name, 'manager:home')

    def test_list_by_tag_reverse(self):
        self.assertEqual(reverse('manager:list_by_tag', args=[23]), '/list/23/')

    def test_list_by_tag_resolve(self):
        self.assertEqual(resolve('/list/23/').view_name,'manager:list_by_tag')
