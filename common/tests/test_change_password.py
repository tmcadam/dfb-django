from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.urls import reverse

from common.forms import ChangePasswordForm
from common.views import change_password


class ChangePasswordFormTests(TestCase):
    """Test ChangePasswordForm functionality."""

    @tag("forms", "change_password")
    def test_form_has_expected_fields(self):
        """Test that the form has the expected password fields."""
        user = User.objects.create_user(
            username="testuser", password="oldpassword123"
        )
        form = ChangePasswordForm(user=user)
        self.assertIn("old_password", form.fields)
        self.assertIn("new_password1", form.fields)
        self.assertIn("new_password2", form.fields)

    @tag("forms", "change_password")
    def test_form_valid_data(self):
        """Test form validation with valid password change data."""
        user = User.objects.create_user(
            username="testuser", password="oldpassword123"
        )
        form = ChangePasswordForm(
            user=user,
            data={
                "old_password": "oldpassword123",
                "new_password1": "newpassword456",
                "new_password2": "newpassword456",
            },
        )
        self.assertTrue(form.is_valid())

    @tag("forms", "change_password")
    def test_form_invalid_old_password(self):
        """Test form rejection with incorrect old password."""
        user = User.objects.create_user(
            username="testuser", password="oldpassword123"
        )
        form = ChangePasswordForm(
            user=user,
            data={
                "old_password": "wrongpassword",
                "new_password1": "newpassword456",
                "new_password2": "newpassword456",
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("old_password", form.errors)

    @tag("forms", "change_password")
    def test_form_new_passwords_mismatch(self):
        """Test form rejection when new passwords don't match."""
        user = User.objects.create_user(
            username="testuser", password="oldpassword123"
        )
        form = ChangePasswordForm(
            user=user,
            data={
                "old_password": "oldpassword123",
                "new_password1": "newpassword456",
                "new_password2": "differentpassword",
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("new_password2", form.errors)

    @tag("forms", "change_password")
    def test_form_password_save_updates_user(self):
        """Test that saving the form updates the user password."""
        user = User.objects.create_user(
            username="testuser", password="oldpassword123"
        )
        form = ChangePasswordForm(
            user=user,
            data={
                "old_password": "oldpassword123",
                "new_password1": "newpassword456",
                "new_password2": "newpassword456",
            },
        )
        self.assertTrue(form.is_valid())
        form.save()
        user.refresh_from_db()
        self.assertTrue(user.check_password("newpassword456"))

    @tag("forms", "change_password")
    def test_form_password_too_common_is_rejected(self):
        """Test that common passwords are rejected by Django validators."""
        user = User.objects.create_user(
            username="testuser", password="oldpassword123"
        )
        form = ChangePasswordForm(
            user=user,
            data={
                "old_password": "oldpassword123",
                "new_password1": "password",
                "new_password2": "password",
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("new_password2", form.errors)


class ChangePasswordViewTests(TestCase):
    """Test ChangePassword view functionality."""

    @tag("views", "change_password")
    def test_change_password_requires_login(self):
        """Test that unauthenticated users are redirected to login."""
        url = reverse("password_change")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    @tag("views", "change_password")
    def test_change_password_get_returns_200(self):
        """Test that GET request returns 200 for authenticated users."""
        user = User.objects.create_user(
            username="testuser", password="oldpassword123"
        )
        self.client.login(username="testuser", password="oldpassword123")
        url = reverse("password_change")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @tag("views", "change_password")
    def test_change_password_get_contains_form(self):
        """Test that the response contains the change password form."""
        user = User.objects.create_user(
            username="testuser", password="oldpassword123"
        )
        self.client.login(username="testuser", password="oldpassword123")
        url = reverse("password_change")
        response = self.client.get(url)
        self.assertContains(response, "Change Password")
        self.assertContains(response, "Current Password")
        self.assertContains(response, "New Password")

    @tag("views", "change_password")
    def test_change_password_post_success_redirects(self):
        """Test that valid password change redirects after success."""
        user = User.objects.create_user(
            username="testuser", password="oldpassword123"
        )
        self.client.login(username="testuser", password="oldpassword123")
        url = reverse("password_change")
        response = self.client.post(
            url,
            {
                "old_password": "oldpassword123",
                "new_password1": "newpassword456",
                "new_password2": "newpassword456",
            },
        )
        self.assertEqual(response.status_code, 302)
        # Verify the password was changed
        user.refresh_from_db()
        self.assertTrue(user.check_password("newpassword456"))

    @tag("views", "change_password")
    def test_change_password_post_wrong_old_password(self):
        """Test that wrong old password shows form with errors."""
        user = User.objects.create_user(
            username="testuser", password="oldpassword123"
        )
        self.client.login(username="testuser", password="oldpassword123")
        url = reverse("password_change")
        response = self.client.post(
            url,
            {
                "old_password": "wrongpassword",
                "new_password1": "newpassword456",
                "new_password2": "newpassword456",
            },
        )
        self.assertEqual(response.status_code, 200)
        # Check that the form is invalid (old password error)
        self.assertFormError(response.context["form"], "old_password", "Your old password was entered incorrectly. Please enter it again.")

    @tag("views", "change_password")
    def test_change_password_post_passwords_dont_match(self):
        """Test that mismatched new passwords shows form with errors."""
        user = User.objects.create_user(
            username="testuser", password="oldpassword123"
        )
        self.client.login(username="testuser", password="oldpassword123")
        url = reverse("password_change")
        response = self.client.post(
            url,
            {
                "old_password": "oldpassword123",
                "new_password1": "newpassword456",
                "new_password2": "differentpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields didn’t match")

    @tag("views", "change_password")
    def test_change_password_url_resolves_to_custom_view(self):
        """Test that the password_change URL resolves to our custom view."""
        url = reverse("password_change")
        self.assertEqual(url, "/accounts/password_change/")
