#!/usr/bin/env bash
cd webfront
gunicorn webfront.wsgi --log-file -