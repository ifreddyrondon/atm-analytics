import json
from functools import wraps

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect

from analytics_gui.analytics.models import Case
from analytics_gui.companies.models import XFSFormat


def format_for_xfs_files_required():
    """
    Custom permission to validate whether there are created at least
    one ATM formats in the case
    """

    def _decorator(func):
        def _closure(request, *args, **kwargs):
            case = get_object_or_404(Case, pk=kwargs['case_id'])
            company = case.bank.company
            atms = case.atms.all()
            can_parsed = 0

            for atm in atms:
                if XFSFormat.objects.filter(
                        company=company, hardware=atm.hardware, software=atm.software).count() == 0:
                    continue

                can_parsed += 1

            if can_parsed > 0:
                return func(request, *args, **kwargs)
            return redirect('analytics:no-format-available-2-analyze')

        return wraps(func)(_closure)

    return _decorator


def select_xfs_format_required():
    """
    Custom permission to redirect whether there are more than
    one format for a XFS file
    """

    def _decorator(func):
        def _closure(request, *args, **kwargs):
            case = get_object_or_404(Case, pk=kwargs['case_id'])
            atms_with_format = kwargs.get('atms_with_format', None)
            if atms_with_format:
                atms_with_format = [int(item[0]) for item in json.loads(atms_with_format)]
            company = case.bank.company
            atms = case.atms.all()

            for atm in atms:
                if XFSFormat.objects.filter(
                        company=company, hardware=atm.hardware, software=atm.software).count() > 1:
                    if atms_with_format and atm.id in atms_with_format:
                        continue
                    else:
                        return HttpResponseRedirect(reverse("analytics:select-xfs-format", args=[case.id]))

            return func(request, *args, **kwargs)

        return wraps(func)(_closure)

    return _decorator
