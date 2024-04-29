from rest_framework.test import APITestCase
from . import models
from users.models import User


# /api/v1/tweets: Test GET and POST methods
class TestTweets(APITestCase):
    URL = "http://127.0.0.1:8000/api/v1/tweets/"
    PAYLOAD = "Tweet Test"
    USERNAME = "TestUser"
    EMAIL = "TestEmail"
    PASSWORD = "TestPassword"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
            email=self.EMAIL,
        )
        user.set_password(self.PASSWORD)
        user.save()
        models.Tweet.objects.create(
            payload=self.PAYLOAD,
            user=user,
        )

    def test_get_method(self):
        response = self.client.get(self.URL)
        json = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        self.assertEqual(
            json["ok"],
            True,
        )
        self.assertIsInstance(
            json["data"],
            list,
        )
        self.assertEqual(
            len(json["data"]),
            1,
        )
        self.assertEqual(
            json["data"][0]["user"],
            {
                "username": self.USERNAME,
                "email": self.EMAIL,
            },
        )
        self.assertEqual(
            json["data"][0]["payload"],
            self.PAYLOAD,
        )

    def test_post_method(self):
        ######## START TEST WITHOUT LOGIN ########
        response = self.client.post(
            self.URL,
            data={
                "payload": self.PAYLOAD,
            },
        )
        json = response.json()

        self.assertEqual(
            response.status_code,
            401,
            "Status code isn't 401.",
        )
        self.assertEqual(
            json["ok"],
            False,
        )
        self.assertEqual(
            json["error"],
            "Please login first",
        )
        ######## END TEST WITHOUT LOGIN ########

        ######## START TEST WITH LOGIN ########
        self.client.login(username=self.USERNAME, password=self.PASSWORD)
        response = self.client.post(
            self.URL,
            data={
                "payload": self.PAYLOAD,
            },
        )
        json = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        self.assertEqual(
            json["ok"],
            True,
        )
        self.assertEqual(
            json["data"]["user"]["username"],
            self.USERNAME,
        )
        self.assertEqual(
            json["data"]["payload"],
            self.PAYLOAD,
        )
        self.assertIsInstance(
            json["data"]["likes"],
            list,
        )
        ######## END TEST WITH LOGIN ########


# /api/v1/tweets/<int:pk>: Test GET, PUT and DELETE methods
class TestTweet(APITestCase):
    URL = "http://127.0.0.1:8000/api/v1/tweets/1"
    PAYLOAD = "Tweet Test"
    PAYLOAD_2 = "CHANGED"
    USERNAME = "TestUser"
    EMAIL = "TestEmail"
    PASSWORD = "TestPassword"
    USERNAME_2 = "TestUser_2"
    EMAIL_2 = "TestEmail_2"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
            email=self.EMAIL,
        )
        user.set_password(self.PASSWORD)
        user.save()
        user_2 = User.objects.create(
            username=self.USERNAME_2,
            email=self.EMAIL_2,
        )
        user_2.set_password(self.PASSWORD)
        user_2.save()
        models.Tweet.objects.create(
            payload=self.PAYLOAD,
            user=user,
        )

    def test_get_method(self):
        response = self.client.get(self.URL)
        json = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        self.assertEqual(
            json["ok"],
            True,
        )
        self.assertEqual(
            json["data"]["user"]["username"],
            self.USERNAME,
        )
        self.assertEqual(
            json["data"]["payload"],
            self.PAYLOAD,
        )
        self.assertIsInstance(
            json["data"]["likes"],
            list,
        )

    def test_put_method(self):
        ######## START TEST WITHOUT LOGIN ########
        response = self.client.put(
            self.URL,
            data={"payload": self.PAYLOAD_2},
        )
        json = response.json()
        self.assertEqual(
            response.status_code,
            401,
            "Status code isn't 401.",
        )
        self.assertEqual(
            json["ok"],
            False,
        )
        self.assertEqual(
            json["error"],
            "Please login first",
        )
        ######## END TEST WITHOUT LOGIN ########

        ######## START TEST WITH OTHER USER'S LOGIN ########
        self.client.login(username=self.USERNAME_2, password=self.PASSWORD)
        response = self.client.put(
            self.URL,
            data={"payload": self.PAYLOAD_2},
        )
        json = response.json()
        self.assertEqual(
            response.status_code,
            403,
            "Status code isn't 403.",
        )
        self.assertEqual(
            json["ok"],
            False,
        )
        self.assertEqual(
            json["error"],
            "You can only edit your own tweets",
        )
        self.client.logout()
        ######## END TEST WITH OTHER USER'S LOGIN ########

        ######## START TEST WITH CORRECT LOGIN ########
        self.client.login(username=self.USERNAME, password=self.PASSWORD)
        response = self.client.put(
            self.URL,
            data={"payload": self.PAYLOAD_2},
        )
        json = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        self.assertEqual(
            json["ok"],
            True,
        )
        self.assertEqual(
            json["data"]["payload"],
            self.PAYLOAD_2,
        )
        ######## END TEST WITH CORRECT LOGIN ########

    def test_delete_method(self):
        ######## START TEST WITHOUT LOGIN ########
        response = self.client.delete(self.URL)
        json = response.json()
        self.assertEqual(
            response.status_code,
            401,
            "Status code isn't 401.",
        )
        self.assertEqual(
            json["ok"],
            False,
        )
        self.assertEqual(
            json["error"],
            "Please login first",
        )
        ######## END TEST WITHOUT LOGIN ########

        ######## START TEST WITH OTHER USER'S LOGIN ########
        self.client.login(username=self.USERNAME_2, password=self.PASSWORD)
        response = self.client.delete(self.URL)
        json = response.json()
        self.assertEqual(
            response.status_code,
            403,
            "Status code isn't 403.",
        )
        self.assertEqual(
            json["ok"],
            False,
        )
        self.assertEqual(
            json["error"],
            "You can only delete your own tweets",
        )
        self.client.logout()
        ######## END TEST WITH OTHER USER'S LOGIN ########

        ######## START TEST WITH CORRECT LOGIN ########
        self.client.login(username=self.USERNAME, password=self.PASSWORD)
        response = self.client.delete(self.URL)
        json = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        self.assertEqual(
            json["ok"],
            True,
        )
        self.assertEqual(
            json["data"],
            "The Tweet is deleted successfully",
        )
        ######## END TEST WITH CORRECT LOGIN ########
