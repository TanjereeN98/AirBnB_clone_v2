#!/usr/bin/python3
"""create a .tgz archive from contents of the web_static"""
from fabric.api import local, task, put, run, env
from datetime import datetime
import os

env.user = "ubuntu"
env.hosts = ['54.89.27.151', '18.209.225.187']


@task
def do_pack():
    """pack web_static folder"""
    try:
        cur_date = datetime.now().strftime('%Y%m%d%H%M%S')
        arch = f'web_static_{cur_date}.tgz'
        local('mkdir -p versions')
        local(f'tar -cvzf versions/{arch} web_static')
        return f'versions/{arch}'
    except Exception:
        return None


@task
def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    file_name = archive_path.split('/')[-1].split('.')[0]
    if not os.path.exists(archive_path):
        return False

    put(archive_path, '/tmp/')
    run(f'mkdir -p /data/web_static/releases/{file_name}/')
    run(f'tar -xzf /tmp/{file_name}.tgz -C /data/web_static/releases/{file_name}/')
    run(f'rm /tmp/{file_name}.tgz')
    run(f'mv /data/web_static/releases/{file_name}/web_static/* \
    /data/web_static/releases/{file_name}/')
    run(f'rm -rf /data/web_static/releases/{file_name}/web_static')
    run('rm -rf /data/web_static/current')
    run(f'ln -s /data/web_static/releases/{file_name}/ \
    /data/web_static/current')
    print('New version deployed!')
    return True
