# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

import sys
sys.path.append("..")
from connections import check_connection


if __name__ == "__main__":

    service_name = sys.argv[1]
    check_connection(service_name)