#!/usr/bin/env python
import time
import datetime
from pprint import pprint
import re
import subprocess
import util

zfs_bin = "/usr/sbin/zfs"

def recreate_zfs_snapshot():
    snapshot=time.strftime('Z/BA@snap-%Y-%m-%d')
    util.system([zfs_bin, 'destroy', snapshot], silent=True)
    util.system([zfs_bin, 'snapshot', snapshot])

def list_snapshots():
    l = []
    snaps = subprocess.check_output([zfs_bin, 'list', '-t', 'snapshot'])
    try:
        snaps = snaps.decode()
    except (UnicodeDecodeError, AttributeError):
        pass
    for snap_line in snaps.split("\n"):
        m = re.search("(.+(\d{4}-\\d\d-\d\d))", snap_line)
        if m:
            snapname = m.group(1) 
            snapdate = datetime.datetime.strptime(m.group(2), "%Y-%m-%d")
            l.append((snapname, snapdate))
    return l


def it_should_be_destroyed(age, day):
    keep_table = (14, 31, 90, 180, 365)
    d = 1
    for k in keep_table:
        if age < k:
            return bool(day % d)
        d <<= 1

def list_and_evaluate():
    epoch_date = datetime.datetime.utcfromtimestamp(0)
    today = datetime.datetime.now()
    
    for (snapname, snapdate) in list_snapshots():
            
            abs_day = (snapdate - epoch_date).days
            age_days = (today - snapdate).days
            if it_should_be_destroyed(age_days, abs_day):
                print("Destroy", snapname)
                subprocess.check_call([zfs_bin, 'destroy', snapname])
                
            else:
                print("Keep", snapname)


recreate_zfs_snapshot()
list_and_evaluate()
