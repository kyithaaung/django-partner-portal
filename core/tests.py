from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import InternalUserProfile, InventoryItem, Partner, PartnerUserProfile


class TenantIsolationTests(TestCase):
    def setUp(self):
        self.partner_a = Partner.objects.create(name="Partner A", code="partner-a")
        self.partner_b = Partner.objects.create(name="Partner B", code="partner-b")

        self.user_a = User.objects.create_user(username="pa", password="pass1234")
        PartnerUserProfile.objects.create(user=self.user_a, partner=self.partner_a)

        self.internal = User.objects.create_user(username="ms", password="pass1234")
        InternalUserProfile.objects.create(user=self.internal, role=InternalUserProfile.ROLE_MS)

        InventoryItem.objects.create(partner=self.partner_a, sku="A-1", name="Item A")
        InventoryItem.objects.create(partner=self.partner_b, sku="B-1", name="Item B")

    def test_partner_only_sees_own_items(self):
        self.client.login(username="pa", password="pass1234")
        response = self.client.get(reverse("portal-home"))
        self.assertContains(response, "A-1")
        self.assertNotContains(response, "B-1")

    def test_internal_sees_all_items(self):
        self.client.login(username="ms", password="pass1234")
        response = self.client.get(reverse("portal-home"))
        self.assertContains(response, "A-1")
        self.assertContains(response, "B-1")
