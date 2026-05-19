from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from common.forms import ChangePasswordForm


@login_required
def change_password(request):
    """Custom change password view matching the login form style."""
    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("pages:home")
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, "registration/change_password.html", {"form": form})
