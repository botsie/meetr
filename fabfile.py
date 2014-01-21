#!/usr/bin/env python

from fabric.api import *
from fabric.contrib import *

import os
import os.path
import datetime

env.gateway = 'zugzug2.bluehost.com:5190'
env.colorize_errors = True
env.hosts = ['sflow1.beta.unifiedlayer.com']
env.forward_agent = True

deploy_root = '/srv/meetr'
git_url = 'https://github.com/botsie/meetr.git'
time_stamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")

def deploy():
    pre_deploy()
    do_deploy()
    post_deploy()

def pre_deploy():
    create_deploy_directory_hierarchy()
    stop_application()

def do_deploy():
    deploy_code()
    link_shared_directories()
    promote_to_current()

def post_deploy():
    start_application()

def create_deploy_directory_hierarchy():
    with cd(deploy_root):
        if not files.exists(os.path.join(deploy_root,'releases')):
            for d in ['releases','shared', 'tmp']:
                run('mkdir -p ' + d)

def start_application():
    pass

def stop_application():
    pass

def deploy_code():
    tmp_dir = os.path.join(deploy_root,'tmp')
    release_dir = os.path.join(deploy_root,'releases',time_stamp)
    tmp_proj_dir = os.path.join(tmp_dir,os.path.basename(os.getcwd()))
    project.upload_project(os.getcwd(),tmp_dir)
    run("mv {0} {1}".format(tmp_proj_dir,release_dir))

def link_shared_directories():
    for directory in ['config', 'log']:
        new_dir = os.path.join(deploy_root, 'releases', time_stamp, directory)
        shared_dir = os.path.join(deploy_root, 'shared', directory)

        if not files.exists(shared_dir):
            run('cp -rav {0} {1}'.format(new_dir, shared_dir))

        run('rm -rf ' + new_dir)
        run('ln -s {0} {1}'.format(shared_dir, new_dir))

def promote_to_current():
    with cd(deploy_root):
        run('rm -f current')
        run('ln -s {0} current'.format(os.path.join('releases',time_stamp)))



