from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from celery import shared_task

from comments.models import Comment


@shared_task
def send_user_email(comment_id):
    # Send email to user who submitted the comment

    comment = Comment.objects.get(id=comment_id)

    text_message = render_to_string(
        "comments/emails/comment_email.txt", {"comment": comment}
    )
    html_message = render_to_string(
        "comments/emails/comment_email.html", {"comment": comment}
    )

    send_mail(
        subject="New comment received",
        message=text_message,
        html_message=html_message,
        from_email=settings.COMMENT_EMAIL_FROM,
        recipient_list=[comment.email],
        fail_silently=False,
    )


@shared_task
def send_admin_email(comment_id, approve_link_url):
    # Send email to user who submitted the comment

    comment = Comment.objects.get(id=comment_id)

    text_message = render_to_string(
        "comments/emails/admin_comment_email.txt",
        {"comment": comment, "approve_link": approve_link_url},
    )
    html_message = render_to_string(
        "comments/emails/admin_comment_email.html",
        {"comment": comment, "approve_link": approve_link_url},
    )

    send_mail(
        subject="New comment received",
        message=text_message,
        html_message=html_message,
        from_email=settings.COMMENT_EMAIL_FROM,
        recipient_list=settings.COMMENT_EMAIL_RECIPIENTS.split(","),
        fail_silently=False,
    )
