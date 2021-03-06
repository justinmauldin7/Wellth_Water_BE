from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Users, Entries, Transactions
from .serializers import UsersSerializer, EntriesSerializer, TransactionsSerializer
from IPython import embed
import pdb

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_user(name="", email=""):
        if name != "" and email != "":
            return Users.objects.create(name=name, email=email)

    @staticmethod
    def create_entry(user, amount=0, drinktype=""):
        if drinktype != "" and user != "" and amount != "":
            Entries.objects.create(user=user, amount=amount, drinktype=drinktype)

    @staticmethod
    def create_transaction(user, amount=0):
        if amount != "":
            Transactions.objects.create(user=user, amount=amount)

    def setUp(self):
        user_with_entries = self.create_user("bob", "bob@gmail.com")
        another_user = self.create_user("Mike", "bobo@gmail.com")
        self.create_user("bobby", "bobby@gmail.com")
        self.create_entry(user_with_entries, 560, "coffee")
        self.create_entry(user_with_entries, 590, "coffee")
        self.create_entry(another_user, 590, "coffee")
        self.__class__.test_user = user_with_entries
        self.create_entry(user_with_entries, 300, "tea")
        self.create_entry(user_with_entries, 540, "beer")
        self.create_transaction(user_with_entries, 1400)

class GetAllUsersTest(BaseViewTest):
    def test_get_all_users(self):
        response = self.client.get(
            reverse("users-all", kwargs={"version": "v1"})
        )
        expected = Users.objects.all()
        serialized = UsersSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetAllEntriesTest(BaseViewTest):
    def test_get_all_entries(self):
        response = self.client.get(
            reverse("entries-all", kwargs={"version": "v1"})
        )
        expected = Entries.objects.all()
        serialized = EntriesSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PostEntryTest(BaseViewTest):
    def test_post_entry(self):
        user = self.__class__.test_user
        self.assertEqual(len(Entries.objects.filter(user=user)), 4)
        response = self.client.post(
            reverse("entries-create", kwargs={"version": "v1", "user_id": user.id, "drinktype": "coffee", "amount": 450})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Entries.objects.filter(user=user)), 5)

class GetUserEntriesTest(BaseViewTest):
    def test_get_all_entries(self):
        user = self.__class__.test_user
        response = self.client.get(
            reverse("user-entries", kwargs={"version": "v1", "user_id": user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

class GetAllTransactionsTest(BaseViewTest):
    def test_get_all_transactions(self):
        response = self.client.get(
            reverse("transactions-all", kwargs={"version": "v1"})
        )
        expected = Transactions.objects.all()
        serialized = TransactionsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
