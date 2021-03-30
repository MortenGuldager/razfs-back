#!/usr/bin/env python
import yaml
import logging
import subprocess
import os
import errno

def yaml_loadfile(filename):
    with open(filename) as stream:
        return yaml.load(stream, Loader=yaml.SafeLoader)

def log_multiline_message(msg, prefix=None, level='info'):
    try:
        msg = msg.decode()
    except (UnicodeDecodeError, AttributeError):
        pass
    for line in str(msg).split('\n'):
        line = line.strip()
        if line != '':
            line = ' ' + line
            if prefix:
                line = "%s:%s" % (prefix, line)
            getattr(logging, level)(line)

def system(cmd, env=None, silent=False):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)

    (o,e) = p.communicate()
    rc = p.returncode
    if silent:
        return rc

    if rc:
        logging.warn("%s return code: %s" % (cmd[0],rc))
    else:
        logging.info("%s return code: %s" % (cmd[0], rc))
    log_multiline_message(o, '   ', "info")
    log_multiline_message(e, '   ', "warn")

    return rc

def mkdir_if_not_exists(path):
    try:
        os.mkdir(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

