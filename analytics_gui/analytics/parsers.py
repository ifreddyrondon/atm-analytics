import random
import re

from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view

from analytics_gui.analytics.models import AtmErrorXFS


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

    # return datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
    return date


def parse_log_file(file_2_parse, atm_index, separator="------"):
    file_2_parse.open(mode='rb')
    data = file_2_parse.read()
    data = data.decode("utf-16", "replace")
    data = data.split(separator)

    traces = []

    for item in data[0:-1]:
        trace = {}
        item = item.replace("\r", "")
        # get date
        match = re.search(r'\d{2}/\d{2}/\d{2,4}( |  |\*| \n)\d{2}:\d{2}(:\d{2})?', item)
        if not match:
            continue
        trace["date"] = parse_date(match.group())
        errors = []
        # get M- or R- errors
        match = re.search(r'M-\d*', item)
        if match:
            errors.append(match.group())
        # get R- errors
        match = re.search(r'R-\d*', item)
        if match:
            errors.append(match.group())
        lines = item.split("\n")
        # delete the lines that start with " " and empty lines
        lines = [x for x in lines if not x.startswith(" ") and x]
        # if last line start with number is error
        if lines[-1].split(" ")[0].isdigit():
            errors.append(lines[-1])
        # get amount
        match = re.search(r'RETIRO:.*', item)
        trace["amount"] = match.group().split(":")[1].strip() if match else ""

        color = AtmErrorXFS.ERROR_COLOR_GREEN if len(errors) == 0 else random.choice(
            [AtmErrorXFS.ERROR_COLOR_ORANGE, AtmErrorXFS.ERROR_COLOR_RED])

        event_type = "Sin error"
        class_name = "green"
        if color == AtmErrorXFS.ERROR_COLOR_ORANGE:
            event_type = "Error importante"
            class_name = "orange"
        elif color == AtmErrorXFS.ERROR_COLOR_RED:
            event_type = "Error critico"
            class_name = "red"

        if len(errors) == 0:
            errors.append("Sin Errores")

        trace.update({
            "has_errors": False if len(errors) == 0 else True,
            "color": color,
            "className": class_name,
            "event_type": event_type,
            "errors": errors,
            "atm_index": atm_index,
        })
        traces.append(trace)

    return traces


def parse_window_event_viewer(file_2_parse):
    file_2_parse.open(mode='rb')
    data = file_2_parse.read()

    traces = []

    fh = FileHeader(data, 0x0)
    for xml_line, record in evtx_file_xml_view(fh):
        trace = {}
        # get date
        match = re.search(r'<TimeCreated SystemTime=\".*\"', xml_line)
        if not match:
            continue
        match = re.search(r'\d{2,4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', match.group())
        if not match:
            continue
        trace["date"] = match.group()
        # event record id
        match = re.search(r'<EventRecordID>\d*', xml_line)
        if not match:
            continue
        match = re.search(r'\d+', match.group())
        trace["record_id"] = match.group()
        trace["context"] = xml_line
        traces.append(trace)

    return traces
