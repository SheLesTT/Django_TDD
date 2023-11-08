import random
import string
from dotenv import load_dotenv
from patchwork.files import exists, append
from fabric import Connection
from fabric import task
import inspect
import  os
if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

load_dotenv()

REPO_URL ="https://github.com/SheLesTT/Django_TDD"

@task
def deploy(c,user, host):


    def _create_directory_structure_if_nessesary(site_folder):
        for subfolder in ("static","database", "venv", "src",):
            conn.run(f"mkdir -p {site_folder}/{subfolder}")

    def _get_latest_source(source_folder    ):

        if exists(conn,path=source_folder + "/.git" ):
            print(source_folder)
            conn.run(f"cd {source_folder} && git fetch")
        else: conn.run(f"git clone {REPO_URL} {source_folder}")
        result  = conn.local(" git log -n 1 --format=%H",)
        current_commit = result.stdout
        conn.run(f"cd {source_folder} && git reset --hard {current_commit}")

    def replace_on_server(file_content, start_string, end_string, replacement):

        start_pos = file_content.find(start_string)
        if start_pos != -1:
            end_pos = file_content.find(end_string,start_pos)
            file_content = file_content[:start_pos] + replacement + file_content[end_pos+1:]
        else: file_content = file_content +  replacement
        return  file_content


    def _update_settings(source_folder):
        settings_path = source_folder +"/superlists/settings.py"
        file_content = conn.run(f" cat {settings_path}").stdout
        file_content.replace("DEBUG = True", "DEBUG = False")
        file_content = replace_on_server(file_content, "ALLOWED_HOSTS = [", "]",
                                         'ALLOWED_HOSTS = ["5.42.78.110", "localhost","http://lovtsevdenisdev.ru"]' )
        file_content = replace_on_server(file_content, "Tata", "]",
                                         "CSRF_TRUSTED_ORIGINS = ['http://lovtsevdenisdev.ru','http://*.127.0.0.1']")
        with open("tata.txt", "w") as f:
            f.write(r""+file_content)
        # conn.run(f'echo "{file_content}" > {settings_path}')
        secret_key_path = source_folder + "/superlists/secret_key.py"
        if not exists(conn, secret_key_path):
            key = "".join(random.choice(string.ascii_lowercase + string.digits))
            append(conn, secret_key_path, f"SECRET_KEY = {key}")
        append(conn, settings_path, "\nfrom .secret_key import SECRET_KEY")


    def _create_venv(site_folder):
        virtualenv_folder = site_folder + "/venv"
        if not exists(conn, virtualenv_folder + "/bin/pip"):
            conn.run(f"python3 -m venv {virtualenv_folder}")
        print(conn.run(f"{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt").stdout)

    def _update_static_files(source_folder):
        print(conn.run(f"cd {site_folder}/venv/bin && ls").stdout)
        print(conn.run(f"cd {source_folder} && ../venv/bin/python manage.py collectstatic --noinput").stdout)


    def _update_database(source_folder):
        print(conn.run(f"cd {source_folder} && ../venv/bin/python manage.py migrate --noinput").stdout)

    conn = Connection(host = os.environ.get("HOST"),connect_kwargs = {"password":os.environ.get("PASSWORD")} )
    conn.run("echo $SSH_TTY")
    site_folder = f"/home/{user}/sites/{host}"
    source_folder = site_folder +"/src"
    _create_directory_structure_if_nessesary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder)
    _create_venv(site_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)