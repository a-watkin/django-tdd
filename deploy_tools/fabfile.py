from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/a-watkin/django-tdd.git'  

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):

        # run is the most common Fabric command. It says "run this shell
        # command on the server". The run commands in this chapter will
        # replicate many of the commands we did manually in the last two.
        
        #  mkdir -p is a useful flavor of mkdir, which is better in two ways:
        # it can create directories several levels deep, and it only creates
        # them if necessary. So, mkdir -p /tmp/foo/bar will create the
        # directory bar but also its parent directory foo if it needs to. It
        # also won’t complain if bar already exists.[1]
        run(f'mkdir -p {site_folder}/{subfolder}')


# pulls down the latest version of the source code from git
def _get_latest_source(source_folder):
    # exists checks whether a directory or file already exists on the server.
    # We look for the .git hidden folder to check whether the repo has already
    # been cloned in that folder.
    if exists(source_folder + '/.git'): 
        # starts with cd because fabric doesn't remember state
        
        # git fetch inside an existing repository pulls down all the latest
        # commits from the Web (it’s like git pull, but without immediately
        # updating the live source tree).
        run(f'cd {source_folder} && git fetch') 
    else:
        run(f'git clone {REPO_URL} {source_folder}')  

    # log invocation to get the id of the current commit that’s on your local
    # PC. That means the server will end up with whatever code is currently
    # checked out on your machine (as long as you’ve pushed it up to the
    # server).
    current_commit = local("git log -n 1 --format=%H", capture=True)  

    # We reset --hard to that commit, which will blow away any current
    # changes in the server’s code directory.
    run(f'cd {source_folder} && git reset --hard {current_commit}')


    # For this script to work, you need to have done a git push of your
    # current local commit, so that the server can pull it down and reset to
    # it. If you see an error saying Could not parse object, try doing a git
    # push.


# updates settings.py
def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    # string substitution: True becomes False
    sed(settings_path, "DEBUG = True", "DEBUG = False")  
    sed(settings_path,
        # And here it is adjusting ALLOWED_HOSTS, using a regex to match the right line.
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )
    # generates a new secret key, and replaced the current key with it
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):  
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')

    # append just adds a line to the end of a file. (It’s clever enough not to
    # bother if the line is already there, but not clever enough to
    # automatically add a newline if the file doesn’t end in one. Hence the
    # back-n.)

    # using a relative import (from .secret_key instead of from
    # secret_key) to be absolutely sure we’re importing the local module,
    # rather than one from somewhere else on sys.path.
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')  


# Next we create or update the virtualenv
def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    # checks if a venv already exists and creates it if it does not
    if not exists(virtualenv_folder + '/bin/pip'):  
        run(f'python3.6 -m venv {virtualenv_folder}')
    # installs required packages
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt') 


# Updating static files is a single command:
def _update_static_files(source_folder):
    run(
        # You can split long strings across multiple lines like this in
        # Python, they concatenate to a single string. It’s a common source of
        # bugs when what you actually wanted was a list of strings, but you
        # forgot a comma!
        f'cd {source_folder}'  
        # We use the virtualenv binaries folder whenever we need to run a
        # Django manage.py command, to make sure we get the virtualenv version
        # of Django, not the system one.
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'  
    )


# Migrating the database if necessary
# The --noinput removes any interactive yes/no confirmations that fabric would
# find hard to deal with.
def _update_database(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )


def deploy():
    # env.user will contain the username you’re using to log in to the server.
    # env.host will contain the address of the server we’ve specified at the command line
    site_folder = f'/home/{env.user}/sites/{env.host}'

    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)  
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

