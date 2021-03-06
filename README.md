# 声明 (What's this)

对于 perchouli 的多说 django 部分进行了部分修改,

添加了 `data-thread-key` `data-title` `data-url` 以及 SSO 登录 的支持. 详见 [Django useage](#django-usage)

可以参考我的博客 [Django 遇见 duoshuo](http://njuaplusplus.com/post/duoshuo-in-django/)

![Banner](https://raw.github.com/perchouli/img/master/banner-772x250.png)

# Duoshuo Python SDK

多说Python SDK支持用Python语言开发的网站，对其提供[多说]插件的支持。使用中遇到的问题请[到多说开发者中心提问](http://dev.duoshuo.com/threads/500c9c58a03193c12400000c "多说开发者中心") 。

# Requirements

Python 2.6+

Django 1.6+ (如果在Django中使用)

# Install

    python setup.py install

# Index

[Python Useage](#python-usage)

[Django useage](#django-usage)


# Python Usage

作为Python models来使用

### Core (__init__.py)

sdk核心功能： 交换token，生成授权链接，调用api接口

#### 实例化duoshuoAPI

    from duoshuo import DuoshuoAPI

    api = DuoshuoAPI(short_name=YOUR_DUOSHUO_SHORT_NAME, secret=YOUR_DUOSHUO_SECRET)

    #例如要获取用户信息
    api.users.profile(user_id=1)


更多API可以查看[多说开发文档](http://dev.duoshuo.com/docs "多说开发文档") 。

#### 交换token
访问需要登录的接口时要先进行授权，采用OAuth2.0协议，Python SDK提供交换token的处理，实例化api后可以直接传入code来获取token：

    code = request.GET.get('code') #获得GET参数(以Django为例)

    token = api.get_token(code=code)


# Django Usage

作为Django app来使用

### 安装duoshuo插件

    # settings.py
    INSTALLED_APPS = (
        ...
        'duoshuo',
    )

    DUOSHUO_SECRET = '你的多说secret，在多说管理后台 - 设置 - 密钥'
    DUOSHUO_SHORT_NAME = '你的多说short name，比如你注册了example.duoshuo.com，short name就是example'

### 显示多说评论框

    {% load duoshuo_tags %}

    {% duoshuo_comments %}

    # 给多说评论框传递其他short name
    {% duoshuo_comments '其他short name' %}

### 我扩展的 tag

    {% my_duoshuo_comments data_thread_key data_title data_url %}
    {% my_sso_duoshuo_comments data_thread_key data_title data_url next_url(可选) %}
    {% my_sso_duoshuo_login next_url(可选) %}

其中 `next_url` 主要用于 SSO 登录之后的跳转, 可以不填.

对于 SSO 的设置, 在 settings.py 中加入这两行

    SSO_LOGIN_URL = 'http://127.0.0.1:8000/accounts/login/'
    SSO_LOGOUT_URL = 'http://127.0.0.1:8000/accounts/logout/'
