#!/usr/bin/env python

import sqlite3 as lite
import sys
import argparse

con = None
uniqueCode = None

db = "./codes.db"


parser = argparse.ArgumentParser(description="Derby Code Generator")
parser.add_argument("-g","--gate", help='Specify the gate to gen a code for.  like -g 1 or --gate 1')
parser.add_argument("-w","--web", help='Output for web, optional', action="store_true")
parser.add_argument("-s","--staticonly", help='Output only the static gate code', action="store_true")
args = parser.parse_args()


if args.gate:
    gate = args.gate
else:
    print("You must specify a gate with -g #")
    sys.exit(1)



try:
    con = lite.connect(db)

    cur = con.cursor()

    if args.staticonly is False:
      cur.execute('SELECT code FROM codes LIMIT 1')
      uniqueCode = cur.fetchone()


    cur.execute("SELECT code FROM gate_id WHERE id = ? LIMIT 1", gate)
    gateId = cur.fetchone()

    if gateId is None:
        print "The gate id does not exist"
        sys.exit(2)
    if uniqueCode is not None:
      cur.execute("DELETE FROM codes WHERE code = ?", uniqueCode)

    if args.web:
        print "Content-type: text/html\n\n"
    if uniqueCode is not None:
      print "%s-%s" % (gateId[0], uniqueCode[0])
    else:
      print "%s" % gateId[0]

except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(3)

finally:
    if con:
        con.commit()
        con.close()
