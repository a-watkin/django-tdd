from fabric.api import run
from fabric.context_managers import settings


def _get_manage_dot_py(host):
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'


def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    #  	Here’s the context manager that sets the host string, in the form user@server-address
    # (I’ve hardcoded my server username, elspeth, so adjust as necessary).
    with settings(host_string=f'awatkin@{host}'):
        run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'awatkin@{host}'):
        # Then, once we’re inside the context manager, we can just call
        # Fabric commands as if we’re in a fabfile.
        session_key = run(f'{manage_dot_py} create_session {email}')
    return session_key.strip()