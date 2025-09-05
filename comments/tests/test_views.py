import re
from django.test import TransactionTestCase, tag, override_settings
from django.urls import reverse
from django.core import mail

from comments.models import Comment
from comments.views import approve_link
from biographies.tests.factories import BiographyFactory

from bs4 import BeautifulSoup as bs

class CommentsViewsTests(TransactionTestCase):


    def  test_submit_comment_saves_comment_with_valid_data(self):
        bio1 = BiographyFactory.create(title="Bio 1")
        url = reverse('comments:submit_comment')

        valid_form_data = {
            "biography": bio1.id,
            "name": "Tom",
            "email": "tom@blah.com",
            "comment": "A test comment",
            "url": ""
        }
        response = self.client.post(url, valid_form_data)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["status"], "success")
        self.assertEqual(bio1.comments.count(), 1)

    @override_settings(COMMENT_EMAIL_FROM="test@test.com",
                       COMMENT_EMAIL_RECIPIENTS="joe@joe.com")
    def  test_submit_comment_sends_email_to_end_user(self):
        bio1 = BiographyFactory.create(title="Bio 1")
        url = reverse('comments:submit_comment')

        valid_form_data = {
            "biography": bio1.id,
            "name": "Tom",
            "email": "tom@blah.com",
            "comment": "A test comment",
            "url": ""
        }
        response = self.client.post(url, valid_form_data)
        self.assertEqual(bio1.comments.count(), 1)

        # Check that two emails were sent
        self.assertEqual(len(mail.outbox), 2)

        # get the first email from the outbox
        message1 = mail.outbox[0]

        # check the email sent to user
        self.assertIn("Dear Tom,", message1.body)
        self.assertEqual(message1.to, ["tom@blah.com"])
        self.assertEqual(message1.subject, "New comment received")
        self.assertEqual(message1.from_email, "test@test.com")
        self.assertIn("Thank you for submitting a comment to the Dictionary of Falklands Biography.", message1.body)
        self.assertIn("Bio 1", message1.body)
        self.assertIn("A test comment", message1.body)

        # check html alternative of email sent to user
        self.assertEqual(message1.alternatives[0][1], "text/html")
        soup = bs(message1.alternatives[0][0], "html.parser")
        self.assertIsNotNone(soup.find("p", string="Dear Tom,"))
        self.assertIsNotNone(soup.find("p", string=re.compile("Thank you for submitting a comment to the Dictionary of Falklands Biography.")))
        self.assertIsNotNone(soup.find("h4", string="Bio 1"))
        self.assertIsNotNone(soup.find("p", string=re.compile("A test comment")))

    @override_settings(COMMENT_EMAIL_FROM="test@test.com",
                       COMMENT_EMAIL_RECIPIENTS="joe@joe.com")
    def  test_submit_comment_sends_email_to_admins(self):
        bio1 = BiographyFactory.create(title="Bio 1")
        url = reverse('comments:submit_comment')

        valid_form_data = {
            "biography": bio1.id,
            "name": "Tom",
            "email": "tom@blah.com",
            "comment": "A test comment",
            "url": ""
        }
        response = self.client.post(url, valid_form_data)
        self.assertEqual(bio1.comments.count(), 1)

        # Check that two emails were sent
        self.assertEqual(len(mail.outbox), 2)

        # get the second email from the outbox
        message2 = mail.outbox[1]
        self.assertEqual(message2.to, ["joe@joe.com"])
        self.assertEqual(message2.from_email, "test@test.com")
        self.assertEqual(message2.subject, "New comment received")

        # check the email sent to admins
        self.assertIn("Dear DFB Admin,", message2.body)
        self.assertIn("A new comment has been received on the Dictionary of Falklands Biographies web site.", message2.body)
        self.assertIn("Please go to the admin site to approve the comment.", message2.body)
        self.assertIn("A test comment", message2.body)

        # check html alternative of email sent to admins
        self.assertEqual(message2.alternatives[0][1], "text/html")
        soup = bs(message2.alternatives[0][0], "html.parser")
        self.assertIsNotNone(soup.find("p", string="Dear DFB Admin,"))
        self.assertIsNotNone(soup.find("p", string=re.compile("A new comment has been received on the Dictionary of Falklands Biographies web site.")))
        self.assertIsNotNone(soup.find("h4", string="Bio 1"))
        self.assertIsNotNone(soup.find("p", string=re.compile("A test comment")))

        self.assertIsNotNone(soup.find('a').find('span', string='Approve Comment'))
        approve_link = soup.find("a")["href"]
        self.assertIn("/comments/approve/", approve_link)


    @tag("comments_views")
    def  test_submit_comment_does_not_save_comment_if_url_populated(self):
        bio1 = BiographyFactory.create()
        url = reverse('comments:submit_comment')

        valid_form_data = {
            "biography": bio1.id,
            "name": "Tom",
            "email": "tom@blah.com",
            "comment": "A test comment",
            "url": "a bot filled the form"
        }
        response = self.client.post(url, valid_form_data)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["status"], "success_")
        self.assertEqual(bio1.comments.count(), 0)


    @tag("comments_views")
    def  test_submit_comment_returns400_if_field_missing(self):
        bio1 = BiographyFactory.create()
        url = reverse('comments:submit_comment')

        valid_form_data = {
            "biography": bio1.id,
            "name": "Tom",
            "comment": "A test comment",
            "url": "a bot filled the form"
        }
        response = self.client.post(url, valid_form_data)
        response_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["status"], "data-error")
        self.assertEqual(bio1.comments.count(), 0)


    @tag("comments_views")
    def  test_submit_comment_returns405_if_not_POST(self):
        bio1 = BiographyFactory.create()
        url = reverse('comments:submit_comment')

        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response_data["status"], "method-error")
        self.assertEqual(bio1.comments.count(), 0)


    @tag("comments_views")
    def  test_approve_comment_approves_comment_with_valid_key(self):
        bio1 = BiographyFactory.create()
        comment = Comment.objects.create(biography=bio1, approved=False)
        comment.set_approve_key()
        comment.save()
        url = reverse('comments:approve_comment', args=[comment.approve_key])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        comment.refresh_from_db()

        self.assertTrue(comment.approved)
        self.assertIsNone(comment.approve_key)

        soup = bs(response.content, "html.parser")
        self.assertIsNotNone(soup.find("h3", string="Comment Approved"))
        self.assertIsNotNone(soup.find("p", string=re.compile("Thank you for approving the comment. It is now visible on the biography page.")))


    @tag("comments_views")
    def  test_approve_comment_shows_error_with_invalid_key(self):
        url = reverse('comments:approve_comment', args=["invalidkey"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        soup = bs(response.content, "html.parser")
        self.assertIsNotNone(soup.find("h3", string="Approval Failed"))
        self.assertIsNotNone(soup.find("p", string=re.compile("Invalid approval key.")))


    @tag("comments_views")
    def test_generate_approve_link(self):
        bio1 = BiographyFactory.create()
        comment = Comment.objects.create(biography=bio1, approved=False)
        comment.set_approve_key()
        comment.save()

        class RequestStub:
            def build_absolute_uri(self, path):
                return f"http://testserver{path}"
        request = RequestStub()

        url = approve_link(request, comment)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

