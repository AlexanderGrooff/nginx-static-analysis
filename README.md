# Nginx Static Analysis

[![nginx-static-analysis](https://img.shields.io/pypi/v/nginx-static-analysis)](https://pypi.org/project/nginx-static-analysis/)

Parse Nginx configurations on your host and filter for directives/values.

Largely powered by [Crossplane](https://github.com/nginxinc/crossplane).

## Installation

You're able to find the `nginx-static-analysis` binary in the following places:

```bash

# Pip
pip install nginx-static-analysis

# Arch
yay -S nginx-static-analysis
```

## Analysing your Nginx configuration

You can list any directive within your Nginx configuration. For example, show all `listen` directives:
```
app@wifbtb-testalex-magweb-cmbl:~$ nginx-static-analysis -d listen
+-------------------------------------------------+--------------------+-------------------------------------+
|                       File                      |       Values       |              Directives             |
+-------------------------------------------------+--------------------+-------------------------------------+
|      /etc/nginx/servers/example.com.conf:3      |         80         | http -> include -> server -> listen |
|      /etc/nginx/servers/example.com.conf:4      |        443         | http -> include -> server -> listen |
|      /etc/nginx/servers/example.com.conf:5      |        8080        | http -> include -> server -> listen |
|      /etc/nginx/servers/example.com.conf:6      |        8888        | http -> include -> server -> listen |
| /etc/nginx/servers/testalex.hypernode.io.conf:3 | 80 default_server  | http -> include -> server -> listen |
| /etc/nginx/servers/testalex.hypernode.io.conf:4 | 443 default_server | http -> include -> server -> listen |
+-------------------------------------------------+--------------------+-------------------------------------+
```

Filtering also works for values, like showing all `location` blocks with value `/`.
This shows you the tree leading up to the filtered values, and all children under the filter:
```
app@wifbtb-testalex-magweb-cmbl:~$ nginx-static-analysis -f location=/
+-------------------------------------------------+-----------------------+-----------------------------------------------------+
|                       File                      |         Values        |                      Directives                     |
+-------------------------------------------------+-----------------------+-----------------------------------------------------+
|             /etc/nginx/nginx.conf:10            |                       |                         http                        |
|             /etc/nginx/nginx.conf:87            |  /etc/nginx/servers/* |                   http -> include                   |
|      /etc/nginx/servers/example.com.conf:1      |                       |              http -> include -> server              |
|      /etc/nginx/servers/example.com.conf:8      |           /           |        http -> include -> server -> location        |
|      /etc/nginx/servers/example.com.conf:9      | http://localhost:8003 | http -> include -> server -> location -> proxy_pass |
| /etc/nginx/servers/testalex.hypernode.io.conf:1 |                       |              http -> include -> server              |
| /etc/nginx/servers/testalex.hypernode.io.conf:6 |           /           |        http -> include -> server -> location        |
| /etc/nginx/servers/testalex.hypernode.io.conf:7 |          403          |   http -> include -> server -> location -> return   |
+-------------------------------------------------+-----------------------+-----------------------------------------------------+
```

If you only want to show the filtered values, or any children under the filtered values, simply specify that
you want to show that directive:
```
app@wifbtb-testalex-magweb-cmbl:~$ nginx-static-analysis -f location=/ -d return -d location
+--------------------------------------------------+---------+-------------------------------------------------+
|                       File                       |  Values |                    Directives                   |
+--------------------------------------------------+---------+-------------------------------------------------+
| /etc/nginx/servers/testalex.hypernode.io.conf:6  |    /    |      http -> include -> server -> location      |
| /etc/nginx/servers/testalex.hypernode.io.conf:7  |   403   | http -> include -> server -> location -> return |
| /etc/nginx/servers/testalex.hypernode.io.conf:10 | /banaan |      http -> include -> server -> location      |
| /etc/nginx/servers/testalex.hypernode.io.conf:11 |   404   | http -> include -> server -> location -> return |
|      /etc/nginx/servers/example.com.conf:8       |    /    |      http -> include -> server -> location      |
+--------------------------------------------------+---------+-------------------------------------------------+
```

By default it parses `/etc/nginx/nginx.conf` and all includes, but you can specify the starting file:
```
app@wifbtb-testalex-magweb-cmbl:~$ nginx-static-analysis -f /some/other/nginx.conf -d location
...
```

## Feeding logs into the analysis

You can feed access/error logs into the analysis by piping it into stdin:
```
app@wifbtb-testalex-magweb-cmbl:~$ tail /var/log/nginx/access.log -n1 | nginx-static-analysis d location
+----------------------------------------------------+--------+------------------------------------------+
|                        File                        | Values |                Directives                |
+----------------------------------------------------+--------+------------------------------------------+
|            /etc/nginx/testsite.conf:18             |   /    |  http -> include -> server -> location   |
| /etc/nginx/sites/http.testalex.hypernode.io.conf:8 |   /    |            server -> location            |
|            /etc/nginx/magento2.conf:17             |   /    | server -> include -> include -> location |
+----------------------------------------------------+--------+------------------------------------------+
```

The analysis creates filters based on the incoming loglines. Those filters are combined with the arguments given
to the `nginx-static-analysis` command.

## Development

This package is using Python >=3.7. Simply `pip install -r requirements/base.txt` into your local venv to install the dependencies.

### Testing

This package uses `pytest` for testing. You can run the tests with `pytest`, which will invoke an Nginx container with some sample configs.
If not present, it'll be built automatically.

### Build

This package can be build locally:

```bash
# Arch
pip install -r requirements/development.txt
makepkg -sCf  # Include -i to install the package locally
```
