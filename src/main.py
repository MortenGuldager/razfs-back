import yaml
import util
import random
from exclusive_yaml import exclusive_yaml
import os.path
import time
import logging

cfg = util.yaml_loadfile('etc/config.yml')
logging.basicConfig(
    level = getattr(logging, cfg['logging']['level']), 
    format = '%(asctime)s %(levelname)s %(message)s'
)

def list_all_jobs():
    all = []
    for node in cfg['nodes']:
        for fs in node['fs']:
            job_key = node['name'] + '¤' + fs
            all.append({"job_key": job_key, "node": node, "fs": fs})
    random.seed()
    random.shuffle(all)
    return all

def run_backup(job):
    node = job["node"]
    fs = job["fs"]

    logging.info("%s : %s" % (node["name"], fs))
    
    cmd = [ '/usr/bin/rsync' ] 
    cmd.extend(cfg['rsync']['opts'])

    if 'port' in node:
        cmd.append('--port=%s' % node['port'])

    src = "{user}@{host}::{path}".format(
      user=node['rsync']['user'],
      host=node['host'],
      path=fs
    )
    logging.debug("src: %s" % src)
    cmd.append(src)

    dst = os.path.join(cfg['paths']['data'], node['name'])
    util.mkdir_if_not_exists(dst)
    
    dst = os.path.join(dst, fs )
    logging.debug("dst: %s" % dst)
    cmd.append(dst)

    env={'RSYNC_PASSWORD':node['rsync']['pass']}

    rc =  util.system(cmd,env)
    if rc == 0:
        return 'ok'
    else:
        return 'fail'

def job_control(job):
    yamlfile = os.path.join(cfg["paths"]["status"], job["job_key"]) + ".yml"

    try:    
        ey = exclusive_yaml(yamlfile)
    except exclusive_yaml.Locked:
        logging.info("locked: " + yamlfile)
        return
    job_status = ey.load()

    try:
        succes_t = job_status["succes_t"]
    except KeyError:
        succes_t = 0

    if time.time() > succes_t + 3600*20:
        result = run_backup(job)
        t = time.time()
        if result == "ok":
            job_status["succes_t"] = t
        else:
            job_status["fail_t"] = t
        job_status["result"] = result

        ey.save(job_status)
        logging.info("--------")


for job in list_all_jobs():
    job_control(job)
