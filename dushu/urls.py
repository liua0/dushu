"""dushu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from novelapp import views as novel
from syncBook import views as sync

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', novel.index,name="index"),
    url(r'^book/(.+)/', novel.book,name='book'),
    url(r'^catalog/(.+)/(.+)/', novel.catalog,name='catalog'),
    url(r'^read/(.+)/(.+)/([0-9]+)', novel.read,name='read'),
    url(r'^search/', novel.search,name='search'),
    url(r'^category/', novel.category,name='category'),
    url(r'^add_book', sync.test)
]
