import os
from fabric.api import run, sudo, env, cd
from fabric.contrib import files

from fab_templates import fab_config as config

env.hosts = config.HOSTS
ROOT = config.ROOT
GIT_REPO = config.GIT_REPO
USER_NAME = config.USER_NAME
USER_EMAIL = config.USER_EMAIL

PROJECT_NAME = 'django-webpack-template'
PROJECT_PATH = os.path.join(ROOT, PROJECT_NAME)
VENV_PATH = os.path.join(PROJECT_PATH, 'venv')


def install_packages():
    packages = [
        'python3-pip',
        'python3-dev',
        'python3-venv',
        'nginx',
        'git-core',
        'npm',
    ]
    sudo(f'apt-get install -y {" ".join(packages)}')


def install_project_code():
    if not files.exists(ROOT):
        run(f'mkdir -p {ROOT}')
    if not files.exists(f'{PROJECT_PATH}/.gitignore'):
        with cd('/home/root'):
            run(f'git clone {GIT_REPO}')
    else:
        with cd(PROJECT_PATH):
            run('git pull')


def create_venv():
    with cd(ROOT):
        if not files.exists(VENV_PATH):
            run(f'python3 -m venv {VENV_PATH}')


def install_pip_requirements():
    with cd(PROJECT_PATH):
        run(f'{VENV_PATH}/bin/pip3.6 install -r requirements.txt -U')


def npm_install():
    with cd(PROJECT_PATH):
        sudo('npm install')


def npm_run_build():
    with cd(PROJECT_PATH):
        if files.exists('dist'):
            run('rm -r dist')
        run('npm run build')


def configure_uwsgi():
    sudo('python3 -m pip install uwsgi')
    sudo('mkdir -p /etc/uwsgi/sites')
    files.upload_template('fab_templates/uwsgi.ini', '/etc/uwsgi/sites/django-webpack-template.ini', use_sudo=True)
    files.upload_template('fab_templates/uwsgi.service', '/etc/systemd/system/uwsgi.service', use_sudo=True)


def configure_nginx():
    if files.exists('/etc/nginx/sites-enabled/default'):
        sudo('rm /etc/nginx/sites-enabled/default')
    files.upload_template('fab_templates/nginx.conf', '/etc/nginx/sites-enabled/django-webpack-template.conf')


def create_env_config():
    files.upload_template('project/env_sample.py', f'{PROJECT_PATH}/project/env.py')


def migrate_database():
    with cd(PROJECT_PATH):
        run(f'{VENV_PATH}/bin/python manage.py migrate')


def collectstatic():
    with cd(PROJECT_PATH):
        run(f'{VENV_PATH}/bin/python manage.py collectstatic -c -n')


def create_superuser():
    with cd(PROJECT_PATH):
        command = f'manage.py createsuperuser --username {USER_NAME} --email {USER_EMAIL}'
        run(f'{VENV_PATH}/bin/python {command}')


def restart_all():
    sudo('systemctl daemon-reload')
    sudo('systemctl reload nginx')
    sudo('systemctl restart uwsgi')


def bootstrap():
    install_packages()
    install_project_code()
    create_venv()
    install_pip_requirements()
    npm_install()
    npm_run_build()
    configure_uwsgi()
    configure_nginx()
    create_env_config()
    migrate_database()
    collectstatic()
    create_superuser()
    restart_all()
