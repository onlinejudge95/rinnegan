#!/bin/sh

gunicorn --bind 0.0.0.0:$PORT manage:app
