from django.test import TestCase
from django.contrib.auth.models import User

from .models import Listing


class BrowseListingsTests(TestCase):
    def test_listings_page_displays_created_items(self):
        user = User.objects.create_user(username='seller', password='testpass123')
        Listing.objects.create(
            seller=user,
            title='Python Book',
            description='A useful book for students.',
            category='Book',
            condition='Good',
            price=250,
            exchange_type='Sell',
            is_available=True,
        )

        response = self.client.get('/listings/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.context)
        self.assertEqual(list(response.context['items'])[:1][0].title, 'Python Book')


class ContactSellerFlowTests(TestCase):
    def test_buyer_can_open_seller_conversation(self):
        seller = User.objects.create_user(username='seller', password='testpass123')
        buyer = User.objects.create_user(username='buyer', password='testpass123')
        item = Listing.objects.create(
            seller=seller,
            title='Java Book',
            description='A useful Java book.',
            category='Book',
            condition='New',
            price=300,
            exchange_type='Sell',
            is_available=True,
        )

        self.client.login(username='buyer', password='testpass123')

        response = self.client.get(f'/listings/{item.id}/contact/')

        self.assertRedirects(
            response,
            f'/listings/{item.id}/conversation/{seller.id}/'
        )

        conversation_response = self.client.get(
            f'/listings/{item.id}/conversation/{seller.id}/'
        )

        self.assertEqual(conversation_response.status_code, 200)


class DashboardTests(TestCase):
    def test_dashboard_shows_logged_in_users_listings(self):
        user = User.objects.create_user(username='seller2', password='testpass123')
        Listing.objects.create(
            seller=user,
            title='Laptop Stand',
            description='Portable desk stand.',
            category='Electronics',
            condition='Good',
            price=500,
            exchange_type='Sell',
            is_available=True,
        )

        self.client.login(username='seller2', password='testpass123')

        response = self.client.get('/dashboard/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('my_listings', response.context)
        self.assertEqual(list(response.context['my_listings'])[:1][0].title, 'Laptop Stand')
