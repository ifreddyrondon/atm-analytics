import datetime
import hashlib
import os
import time

from django.conf import settings


def build_table(date, error, mount):
    table = []

    for i in range(0, len(date)):
        tmp_date = str(date[i])[:str(date[i]).rindex(" ")]
        tmp_date = datetime.datetime.strptime(tmp_date, "%a %b %d %Y %H:%M:%S")
        tmp_date = tmp_date.strftime("%a %d %Y %H:%M:%S")
        tmp_row = [tmp_date, error[i], mount[i]]
        table.append(tmp_row)

    return table


def create_file_element(filename):
    tmp = {}
    absolute_path = os.path.join(settings.BASE_DIR, 'media', filename)
    tmp['md5'] = hash_file_to_md5(absolute_path)
    tmp['sha1'] = hash_file_to_sha1(absolute_path)
    tmp['filename'] = os.path.basename(filename)
    date_str = time.ctime(os.path.getctime(absolute_path))
    date = datetime.datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
    tmp['date'] = date.strftime("%d-%m-%Y")
    return tmp


def hash_file_to_md5(file_path):
    block_size = 65536
    method = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            method.update(buf)
            buf = f.read(block_size)

    return method.hexdigest()


def hash_file_to_sha1(file_path):
    block_size = 65536
    method = hashlib.sha1()
    with open(file_path, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            method.update(buf)
            buf = f.read(block_size)
    return method.hexdigest()
