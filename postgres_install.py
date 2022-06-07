"""PGInstaller."""
import time
import threading
import os
import sys
import subprocess

PG_FILE = "postgresql-9.6.4-1-linux-x64-binaries.tar.gz"
# PG_URL = "https://get.enterprisedb.com/\
PG_URL = "http://192.168.0.38:8888/\
postgresql/"+PG_FILE

PG_ROOT = '/opt/postgresql'
PG_DATA_ROOT = PG_ROOT + '/data'
PG_DIR = '/opt/pgsql'
PG_EXEC = PG_DIR + '/bin'

os.chdir('/opt')
# instalando
pgsql_valid = os.path.isdir(PG_DIR) and os.path.exists(PG_DIR)
if not pgsql_valid:
    subprocess.call("wget "+PG_URL, shell=True)
    subprocess.call('tar -zxvf '+PG_FILE, shell=True)
    subprocess.call('rm -r '+PG_FILE, shell=True)

valid = os.path.isdir(PG_ROOT) and os.path.exists(PG_DATA_ROOT)

up = False


def iniciar_postgres():
    """Method up postgres."""
    global up
    try:
        inicio = PG_EXEC+'/postgres'
        chamada = inicio, ' -D ', PG_DATA_ROOT
        chamada = "{0}".format(chamada)
        p = subprocess.Popen(
            ['su', '-c', chamada, '/bin/sh', 'postgres'],
            stdin=subprocess.PIPE,
            shell=False
        )
        time.sleep(1)
        up = True
        p.communicate(input=b'\n')
    except Exception as ex:
        print(ex)


t1 = threading.Thread(target=iniciar_postgres, name='t_postgres')

if not valid:
    os.mkdir(PG_ROOT)
    os.mkdir(PG_DATA_ROOT)
    subprocess.call(PG_EXEC+'/initdb ' + PG_DATA_ROOT, shell=True)
    time.sleep(2)
    t1.start()
    while not up:
        pass
    subprocess.call(PG_EXEC+'/createuser postgres', shell=True)
    subprocess.call(PG_EXEC+'/createdb millenium', shell=True)
    sys.exit(1)
else:
    t1.start()
    sys.exit(1)
