#!/bin/bash
python manage.py migrate
python manage.py initadmin --username $2 --password $3
xvfb-run --auto-servernum --server-num=1 --server-args='-screen 0, 1440x900x24' python manage.py runserver 0.0.0.0:$1 --noreload
