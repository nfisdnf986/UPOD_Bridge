#!/bin/bash

# DB launcher script
# Copyright (C) 2016 Arduino UPOD
# Author: Sunil <suba5417@colorado.edu>

PIDFILE=./data/db.pid
LOGFILE=./data/db.log

function db_start() {
    echo "starting db"
    mongod --config mongod.config > $LOGFILE &
    echo $! > $PIDFILE
}

function db_stop() {
    if [ -f $PIDFILE ]; then
    	echo "stopping db"
    	kill -15 $(cat "$PIDFILE") && rm -f "$PIDFILE" && rm -f "$LOGFILE"
    fi
}

case "$1" in
    start)
	db_start
	;;

    stop)
	db_stop
	;;

    restart)
	db_stop
	db_start
	;;

    status)
	if [ -f $PIDFILE ]; then
	    echo "Db server already running"
	else
	    echo "Db server not running"
	fi
	;;

    *)
	echo $"Usage: $0 {start|stop|restart|status}"
	exit 1
esac
