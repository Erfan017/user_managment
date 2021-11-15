from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class UserRegister(APITestCase):
    url = reverse('register')

    # fixtures = ['camerafixtures.json']
    # def setUp(self):
    #     User.objects.create(username="admin1", password="123456", user_access=1)
    #     User.objects.create(username="admin2", password="123456", user_access=2)
    #     User.objects.create(username="admin3", password="123456", user_access=3)
    #     User.objects.create(username="admin4", password="123456", user_access=4)

    def test_register(self):
        headers = {"Content-Type": "application/json"}
        response = self.client.post(self.url,
                                    data={"username": "admin1", "password": "12345678", "password_2": "12345678"},
                                    **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_false_data_count(self):
#         self.url = reverse('add_category', kwargs={'pk': 999})
#         headers = {"Content-Type": "application/json"}
#         response = self.client.get(self.url, **headers)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#
# class CameraAddCategoryPUT(APITestCase):
#     url = reverse('add_category_to_cam', kwargs={'pk': 1})
#
#     fixtures = ['camerafixtures.json']
#
#     def test_add_new_category_to_camera(self):
#         headers = {"Content-Type": "application/json"}
#         response = self.client.put(self.url, {'category': [2]}, **headers)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         self.url = reverse('add_category_to_cam', kwargs={'pk': 1})
#         response = self.client.get(self.url, **headers)
#         self.assertEqual(response.json()['data']['category'][0]['id'], 2)
#         # check if database has changed
#
#     def test_add_new_false_category_to_camera(self):
#         self.url = reverse('add_category_to_cam', kwargs={'pk': 999})
#         headers = {"Content-Type": "application/json"}
#         response = self.client.put(self.url, {'category': [2]}, **headers)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
