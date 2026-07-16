from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory

from odd.views import OddRoleRequestViewSet


class OddRoleRequestViewSetTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_anonymous_user_get_queryset_returns_empty(self):
        request = self.factory.get('/api/odd/role-requests/')
        request.user = AnonymousUser()

        view = OddRoleRequestViewSet()
        view.request = request

        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 0)



