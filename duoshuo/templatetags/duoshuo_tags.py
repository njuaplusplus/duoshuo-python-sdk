# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.template import Library, Node

DUOSHUO_SHORT_NAME = getattr(settings, "DUOSHUO_SHORT_NAME", None)
DUOSHUO_SECRET = getattr(settings, "DUOSHUO_SECRET", None)
SSO_LOGIN_URL = getattr(settings, "SSO_LOGIN_URL", None)
SSO_LOGOUT_URL = getattr(settings, "SSO_LOGOUT_URL", None)

register = Library()

class DuoshuoCommentsNode(Node):
    def __init__(self, short_name=DUOSHUO_SHORT_NAME):
        self.short_name = short_name

    def render(self, context):
        code = '''<!-- Duoshuo Comment BEGIN -->
        <div class="ds-thread"></div>
        <script type="text/javascript">
        var duoshuoQuery = {short_name:"%s"};
        (function() {
            var ds = document.createElement('script');
            ds.type = 'text/javascript';ds.async = true;
            ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//static.duoshuo.com/embed.js';
            ds.charset = 'UTF-8';
            (document.getElementsByTagName('head')[0]
             || document.getElementsByTagName('body')[0]).appendChild(ds);
        })();
        </script>
        <!-- Duoshuo Comment END -->''' % self.short_name
        return code

@register.tag
def duoshuo_comments(parser, token):
    if DUOSHUO_SHORT_NAME:
        return DuoshuoCommentsNode(DUOSHUO_SHORT_NAME)
    else:
        try:
            tag_name, short_name = token.split_contents() # More robust than token.contents.split()
        except ValueError:
            raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

@register.simple_tag
def my_duoshuo_comments(data_thread_key, data_title, data_url):
    ''' 生成和通用代码一致的代码

    data_thread_key 文章在站点中的ID
    data_title      文章的标题
    data_url        文章的网址
    '''
    code = '''<!-- Duoshuo Comment BEGIN -->
    <div class="ds-thread" data-thread-key="%s" data-title="%s" data-url="%s"></div>
    <script type="text/javascript">
    var duoshuoQuery = {short_name:"%s"};
    (function() {
        var ds = document.createElement('script');
        ds.type = 'text/javascript';ds.async = true;
        ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//static.duoshuo.com/embed.js';
        ds.charset = 'UTF-8';
        (document.getElementsByTagName('head')[0]
         || document.getElementsByTagName('body')[0]).appendChild(ds);
    })();
    </script>
    <!-- Duoshuo Comment END -->''' % (data_thread_key, data_title, data_url, DUOSHUO_SHORT_NAME)
    return code

@register.simple_tag(takes_context=True)
def my_sso_duoshuo_comments(context, data_thread_key, data_title, data_url, next_url=None):
    ''' 生成和通用代码一致的代码

    data_thread_key 文章在站点中的ID
    data_title      文章的标题
    data_url        文章的网址
    next_url        用于返回登录前页面
    '''
    request = context['request']
    http_host = request.get_host()
    login_url = SSO_LOGIN_URL
    logout_url = SSO_LOGOUT_URL
    if next_url is not None and len(next_url) > 0:
        login_url = "http://%s/%s?next=%s" % (http_host, SSO_LOGIN_URL, next_url)
        logout_url = "http://%s/%s?next=%s" % (http_host, SSO_LOGOUT_URL, next_url)
    code = '''<!-- Duoshuo Comment BEGIN -->
    <div class="ds-thread" data-thread-key="%s" data-title="%s" data-url="%s"></div>
    <script type="text/javascript">
    var duoshuoQuery = {
        short_name:"%s",
        sso: {
            login: "%s",
            logout: "%s"
        }
    };
    (function() {
        var ds = document.createElement('script');
        ds.type = 'text/javascript';ds.async = true;
        ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//static.duoshuo.com/embed.js';
        ds.charset = 'UTF-8';
        (document.getElementsByTagName('head')[0] 
         || document.getElementsByTagName('body')[0]).appendChild(ds);
    })();
    </script>
    <!-- Duoshuo Comment END -->''' % (data_thread_key, data_title, data_url, DUOSHUO_SHORT_NAME, login_url, logout_url)
    return code

@register.simple_tag(takes_context=True)
def my_sso_duoshuo_login(context, next_url=None):
    ''' 生成和通用代码一致的代码

    next_url        用于返回登录前页面
    '''
    request = context['request']
    http_host = request.get_host()
    login_url = SSO_LOGIN_URL
    logout_url = SSO_LOGOUT_URL
    if next_url is not None and len(next_url) > 0:
        login_url = "http://%s/%s?next=%s" % (http_host, SSO_LOGIN_URL, next_url)
        logout_url = "http://%s/%s?next=%s" % (http_host, SSO_LOGOUT_URL, next_url)
    code = '''<!-- Duoshuo Comment BEGIN -->
    <div class="ds-login"></div>
    <script type="text/javascript">
    var duoshuoQuery = {
        short_name:"%s",
        sso: {
            login: "%s",
            logout: "%s"
        }
    };
    (function() {
        var ds = document.createElement('script');
        ds.type = 'text/javascript';ds.async = true;
        ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//static.duoshuo.com/embed.js';
        ds.charset = 'UTF-8';
        (document.getElementsByTagName('head')[0]
         || document.getElementsByTagName('body')[0]).appendChild(ds);
    })();
    </script>
    <!-- Duoshuo Comment END -->''' % (DUOSHUO_SHORT_NAME, login_url, logout_url)
    return code

@register.filter
def addstr(s1, s2):
    ''' Concatenate s1 and s2
    '''
    return str(s1).strip().replace('"','-')+str(s2).strip().replace('"','-')

# 生成remote_auth，使用JWT后弃用
# @register.filter
# def remote_auth(value):
#     user = value
#     duoshuo_query = ds_remote_auth(user.id, user.username, user.email)
#     code = '''
#     <script>
#     duoshuoQuery['remote_auth'] = '%s';
#     </script>
#     ''' % duoshuo_query
#     return code
# remote_auth.is_safe = True
