from datetime import datetime as dt
from django.conf import settings


def copyright_statement(request):

    year = str(dt.now().year)[-2:]
    return {
        "COPYRIGHT": f"2012-{year}",
    }

def environment(request):

    return {
        "ENVIRONMENT": settings.ENVIRONMENT
    }