#! /usr/bin/sh
celery -A core worker -l info -Q main-queue -B
celery -Q main-queue purge