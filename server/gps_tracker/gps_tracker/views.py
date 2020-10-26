from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .helpers import is_panic, set_panic_mode


def login(request):
    return render(request, "login.html", {})


# @login_required  # TODO: Move to main
def show_map(request):
    return render(request, "map.html", {})


@login_required
def switch_panic(request):
    mode = not is_panic()
    set_panic_mode(mode)
    return JsonResponse({"panic": mode})
