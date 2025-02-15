from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from monitoring_genomic_mutations.settings import REMOTE_DB_HOST, REMOTE_DB_PORT, REMOTE_DB_NAME, REMOTE_DB_USER, \
    REMOTE_DB_PASSWORD
from user.models import UserData
from .forms import GettingDataForm
from .services.cardio_db_conn import pgsql_conn


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
def display_last(request):
    last_entry = UserData.objects.filter(user=request.user).order_by('-id').first()
    search_type = last_entry.search_type if last_entry else 0
    gene = last_entry.gene if last_entry else "Нет данных"

    return redirect("display_result", search_type=search_type, gene=gene)


@login_required(login_url='/accounts/login/')
def display_result(request, search_type, gene):
    conn = pgsql_conn(REMOTE_DB_HOST,
                      REMOTE_DB_PORT,
                      REMOTE_DB_NAME,
                      REMOTE_DB_USER,
                      REMOTE_DB_PASSWORD)
    df = conn.read_sql(f''' 
    SELECT  
        id  
    FROM crd_dmt.data_vcf 
    LIMIT 10
    ''')
    records = df.to_dict(orient="records")

    return render(
        request,
        "monitoring/display_data.html",
        context={
            "username": request.user.username,
            "search_type": search_type,
            "gene": gene,
            "records": records
        }
    )
