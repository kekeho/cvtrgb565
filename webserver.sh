#!/usr/bin/env bash
cd webfront
mkdir files
gunicorn webfront.wsgi --log-file -