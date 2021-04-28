#!/bin/bash

cd /docker-entrypoint-initdb.d

psql -U postgres --single-transaction -f init.sql

psql -U postgres