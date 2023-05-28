"""
WSGI config for brecommend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
# 模块里导入函数，返回一个sdgi可调用对象，处理http请求
from django.core.wsgi import get_wsgi_application
# 设置要使用的django设置模块breconmend.settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brecommend.settings')
# 将函数get_wsgi_application返回的wsgi应用程序分配给application变量
application = get_wsgi_application()
