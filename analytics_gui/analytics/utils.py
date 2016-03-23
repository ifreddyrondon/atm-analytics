# coding=utf-8
import datetime
import hashlib
import math
import os
import time

import PyPDF2
from django.conf import settings

PIXELS_X_PAGE = 1657.9
ROWS_X_PAGE = 13


# PIXELS_X_PAGE = 1667.8

def build_table(date, error, mount, atm, atms):
    table = []

    for i in range(0, len(date)):
        locations = list(list(atms)[int(atm[i]) - 1].atm_location.all())
        location = "Sin dirección asociada"
        if len(locations) > 1:
            tmp = []
            for loc in locations:
                tmp.append(loc.address)
            location = tmp.join(", ")
        elif len(locations) == 1:
            location = locations[0].address
        tmp_date = str(date[i])[:str(date[i]).rindex(" ")]
        tmp_date = datetime.datetime.strptime(tmp_date, "%a %b %d %Y %H:%M:%S")
        tmp_date = tmp_date.strftime("%a %d %Y %H:%M:%S")
        tmp_row = [tmp_date, error[i], mount[i], atm[i], location]
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


def add_header_and_rotate_timeline(target, height, operations_height):
    header_root = os.path.join(settings.BASE_DIR, 'base', 'static', 'doc', 'header.pdf')
    result_root = os.path.join(settings.BASE_DIR, 'media', 'report.pdf')
    pdf_target = PyPDF2.PdfFileReader(open(target, 'rb'))
    pdf_header = PyPDF2.PdfFileReader(open(header_root, 'rb'))
    pdf_writer = PyPDF2.PdfFileWriter()

    total_pages = int(math.ceil(height / PIXELS_X_PAGE))
    total_pages_x_rows = int(math.ceil(operations_height / ROWS_X_PAGE))

    for page_num in range(pdf_target.getNumPages()):
        pdf_target.getPage(page_num).mergePage(pdf_header.getPage(0))

    for page_num in range(pdf_target.getNumPages()):
        page = pdf_target.getPage(page_num)
        if (page_num >= (4 + total_pages_x_rows)) \
                and (page_num <= (4 + total_pages_x_rows + total_pages)):
            page.rotateClockwise(-90)
        pdf_writer.addPage(page)

    result = open(result_root, 'wb')
    pdf_writer.write(result)
    result.close()


def get_size(filename):
    st = os.stat(filename)
    return st.st_size
