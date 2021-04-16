#!/usr/bin/env python
# -*- coding: utf-8 -*-
from re import search as grep
import requests
from html.parser import HTMLParser
from yaml import safe_load

from enum import Enum
class Status(Enum):
    error   = 0
    work    = 1
    no_work = 2
    holiday = 3

regName = r"^'[A-z]+\.[A-z]+.[A-z]+'$"
regStatus = r'^[A-z-]*-icon'
parser = HTMLParser()
config = safe_load(open("config.yml"))

def eltex_get_employee_status(find_name):
    names, status = __eltex_get_people_list()
    if find_name in names:
        idx = names.index(find_name)
        return status[idx];
    else:
        return Status.error


def __eltex_get_people_list(url = config['defconfig']['eltex_host']) -> list:
    names = []
    status = []
    page = requests.get(url).text.split()
    for item in page:
            guess = parser.unescape(item)
            if (grep(regName, guess) is not None):
                    names.append(guess[1:-1])
            if (grep(regStatus, guess) is not None):
                    st = guess[0:-len('-icon')]
                    if 'no-job' in st:
                        status.append(Status.no_work)
                    elif 'job' in st:
                        status.append(Status.work)
                    elif 'holiday' in st:
                        status.append(Status.holiday)
    return names, status
