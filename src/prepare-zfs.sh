#!/bin/bash

set -e
POOL=Z

zpool_is_online() {
    zpool status $POOL | grep -q 'state: ONLINE' 
}

if zpool_is_online
then
    exit 0
fi

echo re-importing $POOL
zpool export $POOL
zpool import $POOL

if zpool_is_online
then
    exit 0
fi

echo THIS IS BAD, failed to get pool online
exit 1
