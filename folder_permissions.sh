#!/bin/bash
chown -R www-data:www-data .
chmod -R 755 .
chmod 755 uploads/
chmod 755 cache/
chmod 755 static/audio
chmod 744 app.py