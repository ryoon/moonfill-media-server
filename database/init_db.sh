#!/bin/sh

rm -f media-server.sqlite3
sqlite3 -init init_db.sql media-server.sqlite3 ""

