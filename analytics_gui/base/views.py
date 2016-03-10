from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from analytics_gui.analytics.models import Case
from analytics_gui.authentication.forms import CreateAnalystForm
from analytics_gui.authentication.models import UserDashboard
from analytics_gui.companies.models import Company


@login_required(login_url='/login')
def dashboard(request):
    if request.user.is_superuser:
        return redirect('/admin/')

    user = request.user.dash_user
    company = Company.objects.get(users=user)

    if user.charge == UserDashboard.POSITION_ADMIN:
        create_analyst_form = CreateAnalystForm()

        if request.method == 'POST':
            if 'add-user' in request.POST:
                create_analyst_form = CreateAnalystForm(request.POST)
                if create_analyst_form.is_valid():
                    user = User.objects.create_user(
                            username=create_analyst_form.cleaned_data.get('username'),
                            password=create_analyst_form.cleaned_data.get('password'),
                            email=create_analyst_form.cleaned_data.get('email'),
                            first_name=create_analyst_form.cleaned_data.get('first_name'),
                            last_name=create_analyst_form.cleaned_data.get('last_name'),
                    )
                    UserDashboard.objects.create(
                            user=user,
                            charge=UserDashboard.POSITION_ANALYST,
                            company=company,
                    )

                    return JsonResponse({}, status=200)
                else:
                    return JsonResponse(create_analyst_form.errors, status=400)

        return render(request, 'base/manager_dashboard.html', {
            "company": company,
            "users": company.users.filter(charge=UserDashboard.POSITION_ANALYST),
            "create_analyst_form": create_analyst_form,
        })
    elif user.charge == UserDashboard.POSITION_ANALYST:
        cases = Case.objects.filter(analyst=user).order_by('number')

        return render(request, 'base/analyst_dashboard.html', {
            "company": company,
            "cases": cases,
        })
