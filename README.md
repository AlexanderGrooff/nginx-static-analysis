# Nginx Static Analysis

[![nginx-static-analysis](https://img.shields.io/pypi/v/nginx-static-analysis)](https://pypi.org/project/nginx-static-analysis/)

Parse Nginx configurations on your host and filter for directives/values.

Largely powered by [Crossplane](https://github.com/nginxinc/crossplane).

## Analysing your Nginx configuration

You can list any directive within your Nginx configuration. For example, show all `listen` directives:
```
app@wifbtb-testalex-magweb-cmbl:~$ nginx-static-analysis directive listen
+------------------------------------------------------+----------------------------------------+------------------+
|                         File                         |                 Values                 |    Directives    |
+------------------------------------------------------+----------------------------------------+------------------+
|  /etc/nginx/sites/http.testalex.hypernode.io.conf:4  |     127.0.0.1:1337 default_server      | server -> listen |
| /etc/nginx/sites/http.testalex.hypernode.io.conf:16  |          8888 default_server           | server -> listen |
| /etc/nginx/sites/https.testalex.hypernode.io.conf:6  | 127.0.0.1:443 ssl http2 default_server | server -> listen |
| /etc/nginx/sites/https.testalex.hypernode.io.conf:22 |     8443 ssl http2 default_server      | server -> listen |
+------------------------------------------------------+----------------------------------------+------------------+
```

Filtering also works for values, like showing all `location` blocks with value `/`:
```
app@wifbtb-testalex-magweb-cmbl:~$ nginx-static-analysis directive location --values /
+----------------------------------------------------+--------+------------------------------------------+
|                        File                        | Values |                Directives                |
+----------------------------------------------------+--------+------------------------------------------+
|            /etc/nginx/testsite.conf:18             |   /    |  http -> include -> server -> location   |
| /etc/nginx/sites/http.testalex.hypernode.io.conf:8 |   /    |            server -> location            |
|            /etc/nginx/magento2.conf:17             |   /    | server -> include -> include -> location |
+----------------------------------------------------+--------+------------------------------------------+
```

You can search for multiple directives, as long as you specify >=n-1 values to directives. F.e., find the `server_name`s and `location`s that match with `location=/static/`:
```
app@wifbtb-testalex-magweb-cmbl:~$ nginx-static-analysis directive location server_name --value /static/
+------------------------------------------------------+-----------------------+------------------------------------------+
|                         File                         |         Values        |                Directives                |
+------------------------------------------------------+-----------------------+------------------------------------------+
|             /etc/nginx/monitoring.conf:5             |       localhost       | http -> include -> server -> server_name |
|              /etc/nginx/testsite.conf:5              |         magweb        | http -> include -> server -> server_name |
| /etc/nginx/sites/https.testalex.hypernode.io.conf:21 | testalex.hypernode.io |          server -> server_name           |
|             /etc/nginx/magento2.conf:23              |        /static/       | server -> include -> include -> location |
+------------------------------------------------------+-----------------------+------------------------------------------+
```

By default it parses `/etc/nginx/nginx.conf` and all includes, but you can specify the starting file:
```
app@wifbtb-testalex-magweb-cmbl:~$ nginx-static-analysis -f /some/other/nginx.conf directive location
...
```
