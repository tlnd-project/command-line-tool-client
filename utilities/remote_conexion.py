from fabric import Connection, task

SERVERS = [
    {"host": "192.168.1.10", "user": "usuario1", "password": "clave1", "port": 22, "password_tac_encrypt": "f3434g545t4t45t23"},
    {"host": "192.168.1.11", "user": "usuario2", "password": "clave2", "port": 2222, "password_tac_encrypt": "f34f34f34dvbvobocvb"},
    {"host": "192.168.1.12", "user": "usuario3", "password": "clave3", "port": 22, "password_tac_encrypt": "f3434g09908ddfgregr3"},
]
for server in SERVERS:
    conn = Connection(
        host=server["host"],
        user=server["user"],
        port=server["port"],
        connect_kwargs={"password": server["password"]}
    )
    # set environ password
    conn.run(f'TAC_PASSWORD={server["password_tac_encrypt"]}')
