import re


def parse_log_file(file_2_parse, separator="------"):
    file_2_parse.open(mode='rb')
    data = file_2_parse.read()
    data = data.decode("utf-16", "replace")
    data = data.split(separator)

    trace = []

    for item in data:
        item = item.replace("\r", "")
        # get date
        match = re.search(r'\d{2}/\d{2}/\d{2}( |  )\d{2}:\d{2}(:\d{2})?', item)
        date = match.group() if match else ""
        # get M- or R- errors
        match = re.search(r'M-\d*', item)
        errors_m = match.group() if match else ""
        # get R- errors
        match = re.search(r'R-\d*', item)
        errors_r = match.group() if match else ""
        lines = item.split("\n")
        # delete the lines that start with " " and empty lines
        lines = [x for x in lines if not x.startswith(" ") and x]
        # if last line start with number is error
        last_line = lines[-1] if lines[-1].split(" ")[0].isdigit() else ""
        trace.append({
            "date": date,
            "errors": {
                "M-": errors_m,
                "R-": errors_r,
                "last_line": last_line
            },
        })

    return trace
