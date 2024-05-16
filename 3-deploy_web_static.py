#!/usr/bin/python3
"""Distributes an archive to my web servers"""
from fabric.api import local, task, put, run, env
from datetime import datetime

env.user = "ubuntu"
env.hosts = ['100.26.165.9', '107.23.177.92']


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
    """Distributes an archive to my web servers"""
    try:
        file_name = archive_path.split('/')[-1].split('.')[0]
        put(archive_path, '/tmp/')
        run(f'mkdir -p /data/web_static/releases/{file_name}/')
        print(f'{file_name}')
        run(f'tar -xzf /tmp/{file_name}.tgz \
            -C /data/web_static/releases/{file_name}/')
        print(f'{file_name}')
        run(f'rm /tmp/{file_name}.tgz')
        run(f'mv /data/web_static/releases/{file_name}/web_static/* \
            /data/web_static/releases/{file_name}/')
        run(f'rm -rf /data/web_static/releases/{file_name}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s /data/web_static/releases/{file_name}/ \
            /data/web_static/current')
        print('New version deployed!')
        return True
    except Exception:
        return False


@task
def deploy():
    """creates and distributes an archive to my web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
