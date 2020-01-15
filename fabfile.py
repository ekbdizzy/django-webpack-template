from fabric.api import local, run, sudo, env, cd
from fabric.contrib import files

env.hosts = [
    'root@167.172.145.174',
]


def install_packages():
    packages = [
        'python3-pip',
        'python3-dev',
        'python3-venv',
        'nginx',
        'git-core',
    ]
    sudo(f'apt-get install -y {" ".join(packages)}')


def create_venv():
    if not files.exists("/root/django-webpack-template/venv"):
        run('python3 -m venv /root/django-webpack-template/venv')


def install_project_code():
    if not files.exists('django-webpack-template/.git'):
        run('git clone https://github.com/ekbdizzy/django-webpack-template.git')
    else:
        with cd('django-webpack-template'):
            run('git pull')


def install_pip_requirements():
    with cd('django-webpack-template'):
        run('/root/django-webpack-template/venv/bin/pip3.6 install -r requirements.txt -U')


def configure_uwsgi():
    pass


def configure_nginx():
    pass


def migrate_database():
    pass


def restart_all():
    pass


def bootstrap():
    install_packages()
    create_venv()
    install_project_code()
    install_pip_requirements()
    configure_uwsgi()
    configure_nginx()
    migrate_database()
    restart_all()
