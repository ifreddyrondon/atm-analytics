import os
import time

import datetime
from django.conf import settings


def build_table(date, error, mount):
    table = []

    for i in range(0, len(date)):
        tmp_row = [date[i], error[i], mount[i]]
        table.append(tmp_row)

    return table


def create_file_element(filename):
    tmp = {}
    absolute_path = os.path.join(settings.BASE_DIR, 'media', filename);
    tmp['filename'] = os.path.basename(filename)
    date_str = time.ctime(os.path.getctime(absolute_path))
    date = datetime.datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
    tmp['date'] = date.strftime("%d-%m-%Y")
    return tmp
