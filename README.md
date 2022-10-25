# Nginx Static Analysis

```
root@fb02a2c63394:/project# ./main.py directive server_name
+-------------------------------------------------+-----------------------------+------------------------------------------+
|                       File                      |            Values           |                Directives                |
+-------------------------------------------------+-----------------------------+------------------------------------------+
|      /etc/nginx/servers/example.com.conf:2      | example.com www.example.com | http -> include -> server -> server_name |
| /etc/nginx/servers/testalex.hypernode.io.conf:2 |    testalex.hypernode.io    | http -> include -> server -> server_name |
+-------------------------------------------------+-----------------------------+------------------------------------------+
```
