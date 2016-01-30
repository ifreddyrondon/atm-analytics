from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from analytics_gui.companies.models import Company


@login_required(login_url='/login')
def config(request):
    user = request.user.dash_user
    company = Company.objects.get(in_charge=user)

    return render(request, 'base/config.html', {
        "company": company,
    })
