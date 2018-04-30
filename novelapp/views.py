from django.shortcuts import render
from django.http import HttpResponse


from requests import get
from json import loads

from .models import *

def get_data(url):
    '''
    获得json数据
    :param url:API_URL
    :return: json数据
    '''

    return loads(get(url).text)


def book(request,id):
    '''
    获得书籍的源列表
    :param request:
    :param id:书籍ID
    :return:
    '''

    # 拼接URL
    yuan_url = "https://api.zhuishushenqi.com/toc?view=summary&book="+id
    book_url = "https://api.zhuishushenqi.com/book/"+id

    # 获得数据
    json_data = get_data(yuan_url)
    book_data = get_data(book_url)

    # 处理数据
    book_name = book_data['title']
    author = book_data['author']
    intro = book_data['longIntro']
    yuan_name = []
    book_url = []
    lastchapter = []
    yuan_id = []
    for info in json_data[1:]:

        # 由于第一个源为VIP才能用所以直接去掉
        yuan_name.append(info['name'])

        book_url.append(info['link'])
        lastchapter.append(info['lastChapter'])
        yuan_id.append(info['_id'])

    # 整合数据
    book_info = list(zip(yuan_name, yuan_id, book_url, lastchapter))
    context = {
        'book_info':book_info,
        'book_name':book_name,
        'author':author,
        'intro':intro,
        'bookID':id,
    }

    return render(request, 'book_info.html', context=context)


def catalog(request,id,book_id):
    '''
    书籍的目录
    :param request:
    :param id:书籍id
    :param book_id:书籍源的id
    :return:
    '''

    # 获得书籍的名字
    book_name = request.GET.get('name')

    # 拼接URL
    url = "https://api.zhuishushenqi.com/toc/"+book_id+"?view=chapters"

    # 获得数据
    catalog_data = get_data(url)

    # 获得目录
    book_catalog = catalog_data['chapters']

    # 获得章节索引
    book_list_id = []
    for _title in book_catalog:
        _index = book_catalog.index(_title)
        book_list_id.append(_index)

    # 增加章节索引
    for _num in range(len(book_catalog)):
        book_catalog[_num]['titleID']=book_list_id[_num]

    # 定义context
    context = {
        'book_list':book_catalog,
        'book_id':book_id,
        'list_id':book_list_id,
        'id':id,
        'book_name':book_name,
    }

    return render(request, 'book.html', context=context)


def index(request):
    '''
    首页，展示排行前100的书籍
    :param request:
    :return:
    '''
    print(request.META.get('HTTP_USER_AGENT'))
    # 拼接URL
    url = "https://api.zhuishushenqi.com/ranking/54d42d92321052167dfb75e3"

    # 获得数据
    json_data = get_data(url)

    # 处理数据
    books = json_data['ranking']['books'][:100]
    book_id = []
    book_name = []
    author = []
    img_src = []
    book_intro = []

    # 整合数据
    for _index in books:
        book_id.append(_index['_id'])
        book_name.append(_index['title'])
        author.append(_index['author'])

        # 拼接书籍封面URL
        img_src.append(("https://statics.zhuishushenqi.com"+_index['cover']))

        # 只保留简介前50个字
        book_intro.append(_index['shortIntro'][:50]+"...")

    #整合数据
    book_info = list(zip(book_id,book_name,author,book_intro,img_src))
    context = {
        'book_info':book_info,
    }

    return render(request, 'index.html', context=context)


def read(request,id,book_id,titleID):
    '''
    阅读界面
    :param request:
    :param id:书籍ID
    :param book_id:源ID
    :param titleID: 章节ID
    :return:
    '''

    # 获得书名
    name = request.GET.get('name')

    # 拼接URL
    url = "https://api.zhuishushenqi.com/toc/" + book_id + "?view=chapters"

    # 获得数据
    book_list = get_data(url)

    # 处理数据
    titleID = int(titleID)
    title_link = book_list['chapters'][titleID]['link']

    # 获得最后一章
    max_title = len(book_list['chapters'])-1

    # 更换掉API链接的特殊字符
    title_link = title_link.replace(':','%3A').replace('/','%2F')\
        .replace('?','%3F').replace('&','%26').replace('=','%3D')

    # 获得章节内容
    content_url = "https://chapterup.zhuishushenqi.com/chapter/"+title_link
    content_data = get_data(content_url)
    content_body = content_data['chapter']['body']

    # 判断下一个和上一页
    next_page = int(titleID) + 1
    if next_page >= max_title:
        # 如果对-99有疑问请看html文件
        next_page = -99
    last_page = int(titleID) - 1

    # 保留文本格式
    book_body = content_body.split("\n")

    context = {
        'body':book_body,
        'title':book_list['chapters'][int(titleID)]['title'],
        'max':max_title,
        'book_id':book_id,
        'next': next_page,
        'last':last_page,
        'id':id,
        'name':name,
    }

    return render(request,'read.html',context=context)


def search(request):
    '''
    搜索
    :param request:
    :return:
    '''

    # 获得搜索关键字
    keyword = request.GET.get('keyword')
    # 拼接URL
    query_url = 'https://api.zhuishushenqi.com/book/fuzzy-search?query='+keyword

    # 数据处理
    data = get_data(query_url)
    books = data['books']
    for _book in books:
        _book['id'] = _book['_id']
        _book['cover'] = "https://statics.zhuishushenqi.com"+_book['cover']
        _book['shortIntro'] = _book['shortIntro'][:50] + "..."
        if len(_book['title'])>10:
            _book['title'] = _book['title'][:9]+'. . .'

    context = {
        'item':books,
        'keyword':keyword,
    }

    return render(request,'search.html',context=context)


def category(request):
    '''
    分类
    :param request:
    :return:
    '''

    # 获得类别
    type = request.GET.get('type')

    # 请求API
    url = "https://api.zhuishushenqi.com/book/by-categories?gender=male&type=hot&major="\
          +type+"&minor=&start=0&limit=20"
    data = get_data(url)

    # 处理数据
    data = data['books']
    for item in data:
        item['id']=item['_id']
        item['img_src']="https://statics.zhuishushenqi.com"+item['cover']
        item['shortIntro'] = item['shortIntro'][:50] + "..."

    context = {
        'book_info':data,
        'type':type
    }

    return render(request,'category.html',context=context)
