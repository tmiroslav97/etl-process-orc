#!/bin/bash

psql -h 127.0.0.1 -d dw_database -U olapuser -w -f /config/setup.sql