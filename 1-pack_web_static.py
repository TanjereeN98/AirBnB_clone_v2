#!/usr/bin/python3
"""Create a .tgz archive from contents of the web_static"""
from fabric.api import local, task
from datetime import datetime


@task
def do_pack():
    """generates a .tgz archive from the contents of the web_static"""
    try:
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f'web_static_{current_time}.tgz'
        local('mkdir -p versions')
        local(f'tar -cvzf versions/{file_name} web_static')
        return f'versions/{file_name}'
    except Exception:
        return None
