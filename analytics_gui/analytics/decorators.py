from functools import wraps

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
