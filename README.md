最近各证书签发商缩短了免费证书的签发时间,免费的SSL 证书只能签发 90 天了，还有一堆签发数量的限制，故此开源免费的 acme.sh 成了大家签发 ssl 证书的最佳选择。但是acme.sh 基于命令行签发，签发证书需要手动配置DNS 解析，非常的麻烦繁琐。因此开发了这个项目，用于在浏览器界面中一键快速签发SSL 证书。

<h3 id="ujcqG">一、项目依赖环境</h3>
```shell
Linux 系统
Python 3.9 + 
Mysql 
Redis 
NodeJS(可选)
acme.sh 
```

<h3 id="ZP97j">二、项目部署说明</h3>
自行安装 Python3,Mysql,Redis 环境，这里不详细描述, 建议使用[宝塔面板](https://www.bt.cn)一键快速高效安装 

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726204490519-b0932192-41b3-460b-805f-4ec93e9b93a3.png)

从github 下载 acme.sh ，下载地址: [github 下载](https://github.com/acmesh-official/acme.sh/archive/refs/heads/master.zip) [镜像下载](https://cdn.iw3c.com.cn/acme.sh-master.zip)

从 github 中 clone 本项目

```shell
git clone https://github.com/sang8052/acme_autossl.git
```

将下载的acme.sh 解压到 本项目目录下，并重命名成 acme.sh ,此时文件夹结构如下

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726204833018-3fcd27b7-5b27-4af6-893f-d016ccf0e8eb.png)

前往 acme.sh 文件夹下 ，使用自己的邮箱预初始化 acme.sh 

```shell
./acme.sh --register-account -m your@email.com
```

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726204987249-03524cf3-e0d8-4d9d-8cf0-9fa325c27a4f.png)

安装 Python 的依赖环境 

```shell
pip3 install -r requirement.ini
```

如下图所示，安装依赖环境成功

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726205301331-84301404-b671-49a6-aa8a-699192fea6e0.png)

将项目目录下的 auto_ssl.sql 导入到你的 Mysql 数据库中

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726205454021-41854ac6-2ec3-4fe6-8bd1-eb18725365f2.png)

修改项目目录下的config.json ，填写你 Mysql ，Redis 的配置信息 ，参考下图

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726205536112-54febcb6-c397-4bb4-b88a-78010c427b53.png)

配置完成后,启动项目，默认情况下项目端口号为 18443 ,可在config.json 中修改

```shell
python3 main.py
```

出现如图所示界面，即表示项目启动成功，此时可访问 http://{服务器ip}:18443 (需要放行防火墙和安全组)

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726205655535-fd9c752c-1564-41aa-bf0f-5d9ef2c76c42.png)

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726205753465-fc980e54-42e5-45c5-a74a-4fbe4add57e9.png)

此时项目部署成功。

注意：此时项目没有运行在后台，关闭命令行窗口会导致项目退出！

可以按下 Ctrl+C 终止项目运行，输入以下命令将项目挂入到后台运行

```shell
nohup python3 main.py > run.log 
```

<h3 id="GNf5z">三、项目配置说明</h3>
<h4 id="RopmO">1.配置邮件服务器，用于证书签发成功后发送邮件通知</h4>
可以参考这篇博文《[如何开启qq邮箱的smtp功能](https://blog.szhcloud.cn/blog/2019/09/23/%e5%a6%82%e4%bd%95%e5%bc%80%e5%90%afqq%e9%82%ae%e7%ae%b1%e7%9a%84smtp%e5%8a%9f%e8%83%bd/)》开启QQ 邮箱的smtp 功能

参考下图填写 你的SMTP 服务器的配置

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726207163903-a9a51f6e-34f8-41c3-9eec-49f554ca9420.png)

<font style="color:#DF2A3F;">记得点右上角的保存配置！</font>

<h4 id="ES0Hh">配置 ACME 的路径用于自动签发证书</h4>
在命令行下打开项目文件下的acme.sh ，输入命令 pwd 查看当前的路径地址

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726207301737-db5868e9-7313-4ec6-8250-5bfbc1dad1da.png)

把这个地址粘贴到系统中的这个界面即可 

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726207332806-f3b85518-89a9-4c76-b361-083e7ae6140a.png)

<font style="color:#DF2A3F;">记得点右上角的保存配置！</font>

<h3 id="l0wv9">四、添加 DNS 秘钥，这里以阿里云为例</h3>
您可以直接填写阿里云的根秘钥（**<font style="color:#DF2A3F;">安全风险警告!根秘钥具有阿里云全局最高操作权限，不建议如此操作</font>**）

我们建议您按照下面的步骤,添加仅授权 DNS 管理的子账户秘钥



<h4 id="BcyRu">1.打开阿里云控制面板,鼠标移动到右上角的头像处，下拉选择访问控制</h4>
![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726207592798-d2c4e354-0d78-499a-aaaa-9aef20f388e4.png)

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726207638072-715dd4ba-f158-40de-9c52-1b68e5741838.png)



<h4 id="srtWK">2.在RAM 子用户处新建一个子用户，用户名随意，用于标识授权的dns 权限账号</h4>
注意勾选下面的OpenAPI 调用访问 ![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726207711768-696fbe90-02f0-42b9-b2e0-288a9f175650.png)

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726207789387-ceeab99f-e34c-4d54-bc41-2ea859cbbbf4.png)

<h4 id="ERCHH">3.复制创建成功的AK，SK</h4>
![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726207956347-eda25082-d6fd-4040-9ec4-c77aab1e2154.png)

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726207995623-b9b7ab13-6ea0-4ad7-8850-1807e8b7a82a.png)

<h4 id="GjX6G">4.在阿里云给予刚刚创建的用户 DNS 权限</h4>
![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726208055508-a66d1682-510b-4cc2-8534-6e60c0ec7576.png)



![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726208103648-fb1d0150-d977-4eeb-8fad-bf6c9620c7a5.png)

勾选 AliyunDNSFullAccess

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726208172838-bc959447-8fdd-46d0-8979-8bc79c95e213.png)



<h3 id="dEbJi">五、添加需要签发的域名</h3>
<font style="color:#DF2A3F;">注意: 阿里云账户需要对签发的域名具有DNS管辖权限哦!</font>

我的阿里云账号下有 域名 iw3c.top , 所以我需要将 域名添加到 对应的DNS 密钥下面

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726208324026-5ee4746e-c5cb-44f4-a7ba-c3453d61b367.png)



<h3 id="vlTXq">六、签发证书 </h3>
1.假设需要签发域名为 iw3c.top 的证书，请在子域名的输入框中输入_

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726208397267-b65a97e5-3204-41e0-b5c9-18693f65effe.png)

2.假设需要签发 *.ssl.iw3c.top 的泛域名证书，请在子域名输入 *.ssl 

如果你的配置都没有问题的话，就开始自动签发证书了哦... 证书签发过程中可以关掉浏览器，签发完成后会邮件通知你，也可以过一会刷新网页下载

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726208564263-f0a09eb6-285e-4be7-9d05-bd5e199fe489.png)

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726209241669-bab8e625-2ea1-4db8-9285-2ae8335299d8.png)

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726209256499-36291f52-dc10-4d02-b900-b9380d621086.png)

![](https://cdn.nlark.com/yuque/0/2024/png/2484069/1726209301576-e8f58063-f40a-40de-a75d-40c32528acf7.png)

<h3 id="ZP97j">七、开发者说明</h3>

项目目录下的 /web 文件夹中为 本项目的 前端代码,编译后需要拷贝到 ./www 目录中方可正常被加载  

前端项目使用 Tdesign 框架开发，基于 Vue2。需要 yarn 环境才能正常开发。



