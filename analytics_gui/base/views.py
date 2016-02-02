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

    if user.position == UserDashboard.POSITION_ADMIN:
        create_analyst_form = CreateAnalystForm()
        company = Company.objects.get(in_charge=user)

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
                    user_dashboard = UserDashboard.objects.create(
                            user=user,
                            position=UserDashboard.POSITION_ANALYST
                    )
                    company.users.add(user_dashboard)

                    return JsonResponse({}, status=200)
                else:
                    return JsonResponse(create_analyst_form.errors, status=400)

        return render(request, 'base/admin_dashboard.html', {
            "company": company,
            "create_analyst_form": create_analyst_form,
        })
    elif user.position == UserDashboard.POSITION_ANALYST:
        company = Company.objects.get(users=user)
        cases = Case.objects.all().order_by('number')

        return render(request, 'base/analyst_dashboard.html', {
            "company": company,
            "cases": cases,
        })
