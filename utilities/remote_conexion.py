from fabric import Connection, task

SERVERS = [
    {"host": "192.168.1.10", "user": "usuario1", "password": "clave1", "port": 22},
    {"host": "192.168.1.11", "user": "usuario2", "password": "clave2", "port": 2222},
    {"host": "192.168.1.12", "user": "usuario3", "password": "clave3", "port": 22},
]
for server in SERVERS:
    conn = Connection(
        host=server["host"],
        user=server["user"],
        port=server["port"],
        connect_kwargs={"password": server["password"]}
    )
    # set environ password
    conn.run('TAC_PASSWORD=<password_encrypt>')
