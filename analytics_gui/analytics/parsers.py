
import random
import re
from decimal import Decimal

from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view
from datetime import datetime

from analytics_gui.analytics.models import AtmErrorXFS, AtmEventViewerEvent


def parse_date(date):
    # normalize date deleting extra spaces or strange characters
    date = date.replace(" \n", " ")
    date = date.replace("  ", " ")
    date = date.replace("*", " ")

    just_date = date.split(" ")[0]
    hour = date.split(" ")[1]
    # if seconds is missing append it
    if len(hour) == 5:
        hour += ":00"

    # if year is incomplete, complete it
    day = just_date.split("/")[0]
    month = just_date.split("/")[1]
    year = just_date.split("/")[2]

    if len(year) == 4:
        date = "{}/{}/{} {}".format(month, day, year, hour)
    if len(year) == 3:
        year = "20{}".format(year[1:])
        date = "{}/{}/{} {}".format(day, month, year, hour)
    if len(year) == 2:
        year = "20{}".format(year)
        date = "{}/{}/{} {}".format(day, month, year, hour)

    return date


def parse_currency(currency_string):
    if currency_string == "":
        currency = 0
    else:
        currency_string = re.sub(r'[^\d\-.]', '', currency_string)
        if currency_string[0] == ".":
            currency = Decimal(currency_string[1:])
        else:
            currency = Decimal(currency_string)

    return float(currency)


def parse_log_file(file_2_parse, atm_index, separator="------"):
    file_2_parse.open(mode='rb')
    data = file_2_parse.read()
    data = data.decode("utf-16", "replace")
    data = data.split(separator)

    traces = []
    meta = {
        "transactions_number": 0,
        "dates": {
            "min": None,
            "max": None,
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

    for item in data[0:-1]:
        meta["transactions_number"] += 1
        trace = {}
        item = item.replace("\r", "")
        # GET DATE
        match = re.search(r'\d{2}/\d{2}/\d{2,4}( |  |\*| \n)\d{2}:\d{2}(:\d{2})?', item)
        if not match:
            continue
        trace["date"] = parse_date(match.group())
        # min and max dates
        meta_date = datetime.strptime(trace["date"], '%d/%m/%Y %H:%M:%S')
        if not meta["dates"]["min"] or meta["dates"]["min"] > meta_date:
            meta["dates"]["min"] = meta_date
        if not meta["dates"]["max"] or meta["dates"]["max"] < meta_date:
            meta["dates"]["max"] = meta_date
        # GET AMOUNT
        match = re.search(r'RETIRO:.*', item)
        trace["amount"] = match.group().split(":")[1].strip() if match else ""
        # check is consult
        if trace["amount"] == "":
            match = re.search(r'CONSULTA', item)
            if not match:
                continue
        trace["amount"] = parse_currency(trace["amount"])
        # GET ERRORS
        error = None
        # delete the lines that start with " " and empty lines
        lines = item.split("\n")
        lines = [x for x in lines if not x.startswith(" ") and x]
        # if last line start with number is error
        if lines[-1].split(" ")[0].isdigit():
            error = lines[-1]
        # if there are no errors of last line, find M- and R- errors
        if error is None:
            match = re.search(r'M-\d+.*', item)
            if match:
                error = match.group()
        # get R- errors
        if error is None:
            match = re.search(r'R-\d+.*', item)
            if match:
                error = match.group()
        # clean error
        if error:
            error = error.strip()
        # track errors names
        if error and error not in meta["errors"]["names"]:
            meta["errors"]["names"].append(error)

        color = AtmErrorXFS.ERROR_COLOR_GREEN if not error else random.choice(
            [AtmErrorXFS.ERROR_COLOR_ORANGE, AtmErrorXFS.ERROR_COLOR_RED])

        event_type = "Sin error"
        class_name = "green"
        if color == AtmErrorXFS.ERROR_COLOR_ORANGE:
            event_type = "Error importante"
            class_name = "orange"
            meta["amount"]["important_errors_transactions"] += trace["amount"]
        elif color == AtmErrorXFS.ERROR_COLOR_RED:
            event_type = "Error critico"
            class_name = "red"
            meta["errors"]["critics_number"] += 1
            meta["amount"]["critical_errors_transactions"] += trace["amount"]

        if not error:
            meta["amount"]["valid_transactions"] += trace["amount"]

        trace.update({
            "has_errors": False if not error else True,
            "color": color,
            "className": class_name,
            "event_type": event_type,
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
