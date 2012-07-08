#!/bin/sh
rm coco.db
python manage.py syncdb
python manage.py initdb

