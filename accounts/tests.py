from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="StrongPass123!")

    def test_register_user(self):
        response = self.client.post("/api/register/", {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPass123!"
        })
        self.assertEqual(response.status_code, 201)

    def test_register_user(self):
        response = self.client.post("/api/register/", {
            "username": "newuser",
            "email": "test@example.com",
            "password": "StrongPass123!"
        })
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        response = self.client.post("/api/login/", {
            "username": "testuser",
            "password": "StrongPass123!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("tokens", response.data)

    def test_invalid_login(self):
        response = self.client.post("/api/login/", {
            "username": "testuser",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)

    

    def test_duplicate_email_registration(self):
        data = {"username": "anotheruser", "email": "test@example.com", "password": "testpass"}
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, 201)

    def test_invalid_login_credentials(self):
        data = {"username": "wronguser", "password": "wrongpass"}
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, 401)

    

    def test_register_user_without_referral(self):
        data = {"username": "newuser", "email": "newuser@example.com", "password": "testpass"}
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, 201)

    def test_successful_referral_registration(self):
        new_user_data = {"username": "referraluser", "email": "referral@example.com", "password": "testpass", "referral_code": self.user.referral_code}
        response = self.client.post("/api/register/", new_user_data)
        self.assertEqual(response.status_code, 201)



    def test_missing_fields_in_registration(self):
        data = {"username": "missingfields"}
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_email_format(self):
        data = {"username": "invalidemail", "email": "invalidemail", "password": "testpass"}
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, 400)

    def test_referral_code_uniqueness(self):
        user2 = User.objects.create_user(username="user2", email="user2@example.com", password="testpass")
        self.assertNotEqual(self.user.referral_code, user2.referral_code)

    def test_reset_password_with_invalid_email(self):
        data = {"email": "nonexistent@example.com"}
        response = self.client.post("/api/forgot-password/", data)
        self.assertEqual(response.status_code, 400)

    def test_duplicate_username_registration(self):
        data = {"username": "testuser", "email": "unique@example.com", "password": "testpass"}
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, 400)

    def test_register_with_existing_referral_code(self):
        referrer = User.objects.create_user(username="referrer", email="referrer@example.com", password="testpass")
        data = {"username": "referred", "email": "referred@example.com", "password": "testpass", "referral_code": referrer.referral_code}
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, 201)

    

    
    