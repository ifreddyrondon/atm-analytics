import re
from datetime import datetime
from decimal import Decimal

from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view
from dateutil.parser import parse

from django.utils.translation import ugettext as _

from analytics_gui.analytics.models import AtmErrorXFS, AtmEventViewerEvent
from analytics_gui.analytics.utils import try_unicode
from analytics_gui.companies.models import XFSFormatEvent


def parse_date(date):
    # normalize date deleting extra spaces or strange characters
    date = date.replace(" \n", " ")
    date = date.replace("  ", " ")
    date = date.replace("*", " ")

    return str(parse(date))


def is_date_valid(date):
    try:
        date.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False
    else:
        return True


def parse_currency(currency_string):
    if currency_string == "":
        currency = 0
    else:
        # currency_string = ''.join(e for e in currency_string if e.isalnum())
        currency_string = re.sub(r'[^\d\-.]', '', currency_string)
        if currency_string[0] == ".":
            currency = Decimal(currency_string[1:])
        else:
            currency = Decimal(currency_string)

    return float(currency)


def parse_log_file(file_2_parse, atm_index, xfs_format):
    file_2_parse.open(mode='rb')
    data = file_2_parse.read()
    data = try_unicode(data)
    data = data.split(xfs_format.group_separator)

    traces = []
    meta = {
        "transactions_number": 0,
        "dates": {
            "min": None,
            "max": None,
            "all": [],
        },
        "amount": {
            "valid_transactions": 0,
            "critical_errors_transactions": 0,
            "important_errors_transactions": 0,
        },
        "errors": {
            "critics_number": 0,
            "names": []
        }
    }

    for item in data:
        meta["transactions_number"] += 1
        trace = {}

        # GET DATE
        match = re.search(r'{}'.format(xfs_format.date_pattern), item)
        if not match:
            continue
        trace["date"] = parse_date(match.group())
        # check is date is correct
        meta_date = datetime.strptime(trace["date"], '%Y-%m-%d %H:%M:%S')
        if not is_date_valid(meta_date):
            continue

        # min and max dates
        if not meta["dates"]["min"] or meta["dates"]["min"] > meta_date:
            meta["dates"]["min"] = meta_date
        if not meta["dates"]["max"] or meta["dates"]["max"] < meta_date:
            meta["dates"]["max"] = meta_date
        # save all dates
        if meta_date not in meta["dates"]["all"]:
            meta["dates"]["all"].append(meta_date)

        # GET AMOUNT
        match = re.search(r'{}.*'.format(xfs_format.total_amount_pattern), item)
        trace["amount"] = match.group() if match else ""
        trace["amount"] = parse_currency(trace["amount"])

        # GET ERRORS
        error = None
        event_type = None
        for event in XFSFormatEvent.objects.filter(xfs_format=xfs_format):
            match = re.search(r'{}.*'.format(event.pattern), item)
            if not match:
                continue
            error = match.group()
            event_type = event.type

        # if nothing to report continue
        if not error:
            continue

        # clean error
        error = error.strip()
        # track errors names
        if error not in meta["errors"]["names"]:
            meta["errors"]["names"].append(error)

        # type of event
        if event_type == XFSFormatEvent.EVENT_TYPE_CRITICAL_ERROR:
            color = AtmErrorXFS.ERROR_COLOR_RED
            event_type_name = _("Critical error")
            class_name = "red"
            meta["errors"]["critics_number"] += 1
            meta["amount"]["critical_errors_transactions"] += trace["amount"]
        elif event_type == XFSFormatEvent.EVENT_TYPE_IMPORTANT_ERROR:
            color = AtmErrorXFS.ERROR_COLOR_ORANGE
            event_type_name = _("Important error")
            class_name = "orange"
            meta["amount"]["important_errors_transactions"] += trace["amount"]
        elif event_type == XFSFormatEvent.EVENT_TYPE_NO_ERROR:
            color = AtmErrorXFS.ERROR_COLOR_GREEN
            event_type_name = _("No error")
            class_name = "green"
            meta["amount"]["valid_transactions"] += trace["amount"]

        trace.update({
            "has_errors": False if not error else True,
            "color": color,
            "className": class_name,
            "event_type": event_type_name,
            "error": error,
            "atm_index": atm_index,
        })
        traces.append(trace)

    meta["errors"]["names"] = set(meta["errors"]["names"])
    return traces, meta


def parse_window_event_viewer(atm):
    atm.microsoft_event_viewer.file.open(mode='rb')
    data = atm.microsoft_event_viewer.file.read()

    fh = FileHeader(data, 0x0)
    for xml_line, record in evtx_file_xml_view(fh):
        # get date
        match = re.search(r'<TimeCreated SystemTime=\".*\"', xml_line)
        if not match:
            continue
        match = re.search(r'\d{2,4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', match.group())
        if not match:
            continue
        date = match.group()
        # event record id
        match = re.search(r'<EventRecordID>\d*', xml_line)
        if not match:
            continue
        match = re.search(r'\d+', match.group())
        event_record_id = match.group()
        # event id
        match = re.search(r'<EventID Qualifiers="(\d+)?">\d+', xml_line)
        if not match:
            continue
        event_id = match.group().split(">")[1]
        context = xml_line
        AtmEventViewerEvent.objects.get_or_create(
            atm=atm,
            event_date=date,
            event_id=event_id,
            event_record_id=event_record_id,
            context=context
        )
