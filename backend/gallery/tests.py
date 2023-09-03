import json

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from datetime import datetime, timedelta

from .models import Gallery
from .views import convertDate
from .serializers import GallerySerializer


class GetArchiveTestCase(APITestCase):
    def setUp(self):
        self.today = datetime.now().today().date()
        self.gallery1 = Gallery.objects.create(
            date=self.today - timedelta(days=1),
            title='test image 1',
            explanation='Explanation 1',
            image_url='https://example.com/image1.jpg'
        )
        self.gallery2 = Gallery.objects.create(
            date=self.today - timedelta(days=2),
            title='test image 2',
            explanation='Explanation 2',
            image_url='https://example.com/image2.jpg'
        )

    def test_get_archive(self):
        url = reverse('get_archive')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertTrue(response.data[0]['date'] > response.data[1]['date'])

    def tearDown(self):
        self.gallery1.delete()
        self.gallery2.delete()
      
        
class GetTodayExistingPictureTestCase(APITestCase):
    def setUp(self):
        self.today = datetime.now().today().date()
        self.gallery = Gallery.objects.create(
            date=self.today,
            title='test image',
            explanation='Explanation',
            image_url='https://exmaple.com/image.jpg'
        )

    def test_get_today_existing_picture(self):
        url = reverse('get_today_picture')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = GallerySerializer(self.gallery)
        self.assertEqual(response.data, serializer.data)

    def tearDown(self):
        self.gallery.delete()
        

class GetTodayNewPictureTestCase(APITestCase):
    def setUp(self):
        self.today = datetime.now().today().date()

    def test_get_today_new_picture(self):
        url = reverse('get_today_picture')
        response = self.client.get(url)
        
        data = json.loads(response.content)
        entryDate = convertDate(data['date'])
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(entryDate, self.today)
        
        
class LikeImageTestCase(APITestCase):
    def setUp(self):
        self.today = datetime.now().today().date()
        self.gallery = Gallery.objects.create(
            date=self.today,
            title='test image',
            explanation='Explanation',
            image_url='https://example.com/image.jpg'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_like_image(self):
        url = reverse('like_image')
        data = {
            'date': str(self.today),
            'username': 'testuser'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        data = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': 'Image liked successfully!'})
        self.assertTrue(self.user in self.gallery.liked_by_users.all())

    def test_like_image_already_liked(self):
        url = reverse('like_image')
        data = {
            'date': str(self.today),
            'username': 'testuser'
        }
        self.gallery.liked_by_users.add(self.user)
        self.gallery.update_likes()
        self.gallery.save()
        
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        data = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': 'Image liked successfully!'})
        self.assertEqual(self.gallery.image_likes_count, 1)

    def test_like_image_invalid_date(self):
        url = reverse('like_image')
        data = {
            'date': '2022-01-01',
            'username': 'testuser'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content.decode('utf-8'), 'Image not found!')

    def test_like_image_invalid_user(self):
        url = reverse('like_image')
        data = {
            'date': str(self.today),
            'username': 'invaliduser'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content.decode('utf-8'), 'Image not found!')

    def tearDown(self):
        self.gallery.delete()
        self.user.delete()


class UnlikeImageTestCase(APITestCase):
    def setUp(self):
        self.today = datetime.now().today().date()
        self.gallery = Gallery.objects.create(
            date=self.today,
            title='test image',
            explanation='Explanation',
            image_url='https://example.com/image.jpg'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.gallery.liked_by_users.add(self.user)
        self.gallery.save()

    def test_unlike_image(self):
        url = reverse('unlike_image')
        data = {
            'date': str(self.today),
            'username': 'testuser'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        data = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': 'Image unliked successfully!'})
        self.assertFalse(self.user in self.gallery.liked_by_users.all())

    def test_unlike_image_not_liked(self):
        url = reverse('unlike_image')
        data = {
            'date': str(self.today),
            'username': 'testuser'
        }
        self.gallery.liked_by_users.remove(self.user)
        self.gallery.update_likes()
        self.gallery.save()
        
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        data = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': 'Image unliked successfully!'})

    def test_unlike_image_invalid_date(self):
        url = reverse('unlike_image')
        data = {
            'date': '2022-01-01',
            'username': 'testuser'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content.decode('utf-8'), 'Image not found!')

    def test_unlike_image_invalid_user(self):
        url = reverse('unlike_image')
        data = {
            'date': str(self.today),
            'username': 'invaliduser'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content.decode('utf-8'), 'Image not found!')

    def tearDown(self):
        self.gallery.delete()
        self.user.delete()


class SearchTestCase(APITestCase):
    def setUp(self):
        self.today = datetime.now().today().date()
        self.gallery1 = Gallery.objects.create(
            date=self.today,
            title='test image 1',
            explanation='Explanation 1',
            image_url='https://example.com/image1.jpg'
        )
        self.gallery2 = Gallery.objects.create(
            date=self.today,
            title='test image 2',
            explanation='Explanation 2',
            image_url='https://example.com/image2.jpg'
        )

    def test_search(self):
        url = reverse('search', args=['Explanation'])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'test image 1')
        self.assertEqual(response.data[1]['title'], 'test image 2')

    def test_search_no_results(self):
        url = reverse('search', args=['invalidquery'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def tearDown(self):
        self.gallery1.delete()
        self.gallery2.delete()


class GetSortedArchiveTestCase(APITestCase):
    def setUp(self):
        self.today = datetime.now().today().date()
        self.gallery1 = Gallery.objects.create(
            date=self.today - timedelta(days=1),
            title='test image 1',
            explanation='Explanation 1',
            image_url='https://example.com/image1.jpg',
            image_likes_count=2
        )
        self.gallery2 = Gallery.objects.create(
            date=self.today,
            title='test image 2',
            explanation='Explanation 2',
            image_url='https://example.com/image2.jpg',
            image_likes_count=2
        )

    def test_get_sorted_archive(self):
        url = reverse('get_sorted_archive')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(response.data[0]['image_likes_count'] >= response.data[1]['image_likes_count'])

    def tearDown(self):
        self.gallery1.delete()
        self.gallery2.delete()


class GetFavouritesArchiveTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.today = datetime.now().today().date()
        self.gallery1 = Gallery.objects.create(
            date=self.today - timedelta(days=1),
            title='test image 1',
            explanation='Explanation 1',
            image_url='https://example.com/image1.jpg'
        )
        self.gallery2 = Gallery.objects.create(
            date=self.today,
            title='test image 2',
            explanation='Explanation 2',
            image_url='https://example.com/image2.jpg'
        )
        self.gallery1.liked_by_users.add(self.user)

    def test_get_favourites_archive(self):
        url = reverse('get_favourites_archive', args=['testuser'])
        self.client.force_login(self.user)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'test image 1')
        self.assertEqual(response.data[0]['image_is_liked'], True)

    def test_get_favourites_archive_no_entries(self):
        url = reverse('get_favourites_archive', args=['testuser'])
        self.client.force_login(self.user)
        self.gallery1.liked_by_users.remove(self.user)
        self.gallery2.liked_by_users.remove(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def tearDown(self):
        self.user.delete()
        self.gallery1.delete()
        self.gallery2.delete()
