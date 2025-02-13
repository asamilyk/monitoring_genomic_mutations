import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from authentication.models import UserData
from .forms import GettingDataForm


@login_required(login_url='/accounts/login/')
def get_data_form(request):
    if request.method == "POST":
        search_type = request.POST.get("search_type")
        gene = request.POST.get("gene")
        UserData.objects.create(user=request.user, search_type=search_type, gene=gene)
        return redirect("display_result", search_type=search_type, gene=gene)
    else:
        userform = GettingDataForm()
        username = request.user.username
        return render(request, "monitoring/get_data.html", {"form": userform, "name": username})


@login_required(login_url='/accounts/login/')
def display_result(request, search_type, gene):
    return render(
        request,
        "monitoring/display_data.html",
        context={
            "username": request.user.username,
            "search_type": search_type,
            "gene": gene
        }
    )


@login_required(login_url='/accounts/login/')
def display_last(request):
    last_entry = UserData.objects.filter(user=request.user).order_by('-id').first()
    search_type = last_entry.search_type if last_entry else "Нет данных"
    gene = last_entry.gene if last_entry else "Нет данных"
    return redirect("display_result", search_type=search_type, gene=gene)
