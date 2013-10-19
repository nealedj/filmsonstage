from django.core.urlresolvers import resolve


def add_url_name(request):
    return {
        "current_url":resolve(request.path_info).url_name
    }
