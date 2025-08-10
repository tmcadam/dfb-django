from comments.forms import SubmitCommentForm
from django.http import JsonResponse


def submit_comment(request):

    if request.method == "POST":
        form = SubmitCommentForm(request.POST)
        if form.is_valid():
            if form.data["url"] == "":
                form.save()
                data = {"status": "success"} 
                status=200
            else:
                data = {"status": "success_"} 
                status=200
        else:
            data = {"status": "data-error", "errors": form.errors.as_json()}
            status=400
    else:
        data = {"status": "method-error"}
        status=405

    return JsonResponse(data, status=status)