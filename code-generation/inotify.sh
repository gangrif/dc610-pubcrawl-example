#!/bin/bash

WD=`pwd`
GATE="6"
CODEFILE="$WD/../volumes/apache/flag/f"
LOGFILE="$WD/code.log"

while true
  do 
    $WD/codes-db.py -g $GATE -w > $CODEFILE
    inotifywait -e access $CODEFILE >> $LOGFILE 
done &

