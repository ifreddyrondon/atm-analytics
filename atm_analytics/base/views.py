from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import translation
from django.utils.translation import check_for_language

from atm_analytics.analytics.models import Case
from atm_analytics.authentication.forms import CreateAnalystForm
from atm_analytics.authentication.models import UserDashboard
from atm_analytics.companies.models import Company, XFSFormat


def set_language(request):
    next_page = request.GET.get('next', None)
    if not next_page:
        next_page = request.META.get('HTTP_REFERER', None)
    if not next_page:
        next_page = '/'
    response = HttpResponseRedirect(next_page)
    if request.method == 'GET':
        lang_code = request.GET.get('lang', None)
        if lang_code and check_for_language(lang_code):
            translation.activate(lang_code)
            if hasattr(request, 'session'):
                request.session[translation.LANGUAGE_SESSION_KEY] = lang_code

    return response


@login_required(login_url='/login')
def dashboard(request):
    if request.user.is_superuser:
        return redirect('/admin/')

    user = request.user.dash_user
    company = Company.objects.get(users=user)

    if user.charge == UserDashboard.POSITION_ADMIN:
        create_analyst_form = CreateAnalystForm()
        xfs_formats = XFSFormat.objects.filter(company=company)

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
            "xfs_formats": xfs_formats,
            "users": company.users.filter(charge=UserDashboard.POSITION_ANALYST),
            "create_analyst_form": create_analyst_form,
        })
    elif user.charge == UserDashboard.POSITION_ANALYST:
        cases = Case.objects.filter(analyst=user).order_by('number')

        return render(request, 'base/analyst_dashboard.html', {
            "company": company,
            "cases": cases,
        })
