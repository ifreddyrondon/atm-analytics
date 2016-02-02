from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from analytics_gui.companies.forms import ConfigForm
from analytics_gui.companies.models import Company


@login_required(login_url='/login')
def config(request):
    user = request.user.dash_user
    company = Company.objects.get(in_charge=user)

    config_form = ConfigForm(instance=company)

    return render(request, 'companies/config.html', {
        "company": company,
        "form": config_form,
    })
