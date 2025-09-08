from urllib.parse import urljoin

from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render

from comments.forms import SubmitCommentForm
from comments.tasks import send_user_email, send_admin_email
from comments.models import Comment


def approve_link(request, comment):
    """Generate a app link for the agreement"""

    base_url = request.build_absolute_uri("/")
    approve_url = reverse("comments:approve_comment", args=[comment.approve_key])
    return urljoin(base_url, approve_url)


def submit_comment(request):
    if request.method == "POST":
        form = SubmitCommentForm(request.POST)
        if form.is_valid():
            if form.data["url"] == "":
                comment = form.instance
                comment.set_approve_key()
                comment.save()
                send_user_email.delay_on_commit(comment.id)
                send_admin_email.delay_on_commit(
                    comment.id, approve_link(request, comment)
                )
                data = {"status": "success"}
                status = 200
            else:
                data = {"status": "success_"}
                status = 200
        else:
            data = {"status": "data-error", "errors": form.errors.as_json()}
            status = 400
    else:
        data = {"status": "method-error"}
        status = 405

    return JsonResponse(data, status=status)


def approve_comment(request, approve_key):
    try:
        comment = Comment.objects.get(approve_key=approve_key)
        comment.approved = True
        comment.approve_key = None
        comment.save()
        context = {
            "heading": "Comment Approved",
            "message": "Thank you for approving the comment. It is now visible on the biography page.",
        }
    except Comment.DoesNotExist:
        context = {"heading": "Approval Failed", "message": "Invalid approval key."}

    return render(request, "comments/approve_result.html", context)
