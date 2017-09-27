from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from requests import get
from json import loads
def get_data(url):
    return loads(get(url).text)
def book(request,id):
    url = "http://51dushu.zhuishushenqi.com/toc?view=summary&book="+id
    json_data = get_data(url)
    title_data = get_data("http://51dushu.zhuishushenqi.com/book/"+id)
    book_name = title_data['title']
    author = title_data['author']
    intro = title_data['longIntro']
    img_src = 'http://statics.zhuishushenqi.com'+title_data['cover']
    yuan_name = []
    book_url = []
    lastchapter = []
    yuan_id = []
    for info in json_data[1:]:
        yuan_name.append(info['name'])
        book_url.append(info['link'])
        lastchapter.append(info['lastChapter'])
        yuan_id.append(info['_id'])
    book_info = list(zip(yuan_name,yuan_id,book_url,lastchapter))
    context = {
        'book_info':book_info,
        'book_name':book_name,
        'author':author,
        'intro':intro,
        'img_src':img_src,
        'bookID':id,
    }
    return render(request,'book_info.html',context=context)
def catalog(request,id,book_id):
    book_name = request.GET.get('name')
    url = "http://51dushu.zhuishushenqi.com/toc/"+book_id+"?view=chapters"
    list_data = get_data(url)
    book_list = list_data['chapters']
    book_list_id = []
    for i in book_list:
        ind = book_list.index(i)
        book_list_id.append(ind)
    for i in range(len(book_list)):
        book_list[i]['titleID']=book_list_id[i]
    context = {
        'book_list':book_list,
        'book_id':book_id,
        'list_id':book_list_id,
        'id':id,
        'book_name':book_name,
    }
    return render(request, 'book.html', context=context)

def index(request):
    json_data = get_data("http://51dushu.zhuishushenqi.com/ranking/54d42d92321052167dfb75e3")
    books = json_data['ranking']['books'][:100]
    book_id = []
    book_name = []
    author = []
    img_src = []
    book_intro = []
    for i in books:
        book_id.append(i['_id'])
        book_name.append(i['title'])
        author.append(i['author'])
        img_src.append(("http://statics.zhuishushenqi.com"+i['cover']))
        book_intro.append(i['shortIntro'])
    book_info = list(zip(book_id,book_name,author,book_intro,img_src))
    context = {
        'book_info':book_info,
    }
    return render(request, 'index.html', context=context)

def read(request,id,book_id,titleID):
    url = "http://51dushu.zhuishushenqi.com/toc/" + book_id + "?view=chapters"
    book_list = get_data(url)
    title_link = book_list['chapters'][int(titleID)]['link']
    max_title = len(book_list['chapters'])-1
    title_link = title_link.replace(':','%3A').replace('/','%2F').replace('?','%3F').replace('&','%26').replace('=','%3D')
    data = get_data("http://chapterup.zhuishushenqi.com/chapter/"+title_link)
    body = data['chapter']['body']
    next_page = int(titleID)+1
    if next_page >= max_title:
        next_page = -99
    last_page = int(titleID)-1
    book_body = body.split("\n")
    context = {
        'body':book_body,
        'title':book_list['chapters'][int(titleID)]['title'],
        'max':max_title,
        'book_id':book_id,
        'next': next_page,
        'last':last_page,
        'id':id
    }
    return render(request,'raed.html',context=context)
def search(request):
    keyword = request.GET.get('keyword')
    data = get_data('http://api.zhuishushenqi.com/book/fuzzy-search?query='+keyword)
    return HttpResponse(data)