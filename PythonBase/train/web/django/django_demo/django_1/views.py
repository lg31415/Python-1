#-*- coding:utf-8 -*-
from django.shortcuts import render

# 这里编写函数
# Create your views here.
from  django.http import HttpResponse

'''
	无参函数
'''
def hello(request):
	return HttpResponse('2x2322!')


'''
	带参函数
'''
html='''
    <form method="post" action="/add/">
    <input type="text" name='a',value='%d' />+
	<input type="text" name='b',value='%d' />
	<input type="submit" value="="/>
	<input type="text" value="%d" />'''

def add(request):
	if request.POST.has_key('a'):
		a=int(request.POST['a'])
		b=int(request.POST['b'])
	else:
		a=0
		b=0
	return HttpResponse(html%(a,b,a+b))

'''
	模板函数
'''
from django.shortcuts import render_to_response
address=[
{'name':'zhou','address':u'上海'},
{'name':'zhang','address':u'北京'}
]

 #这里的address不是字典列表，而是元组列表
def addressbook(request):
    return render_to_response('addreslist.html',{'address':address})

'''
	文件保存
'''
from django.template import loader,Context
def output(request, filename):
    response = HttpResponse() #mimetype='text/csv')	# 创建response对象
    response['Content-Disposition'] = 'attachment; filename =%s.csv' % filename  #修改response对象的属性
    t = loader.get_template('csv.html')   # 生成templete对象
    c = Context({'data':address})	      # 生成Context对象
    response.write(t.render(c))			  # 渲染模板
    return response						  # 返回response对象


'''
	交互数据库
'''
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader,Context
from models import Wiki

def index(request,pagename=''):
    '''显示一半页面，对页面内容做链接处理'''
    if pagename:
    #如果提供了页面的名字，则查找页面是否已经存在
        pages = Wiki.objects.filter(pagename=pagename)
        if pages:
            #如果页面已存在，则调用模板来显示
            return process('wiki/page.html', pages[0])
        else:
            #如果页面不存在，则进入编辑界面
            return render_to_response('wiki/edit.html', {'pagename':pagename})
    else:
        #如果没有提供页面的名字，则显示首页
        page = Wiki.objects.get(pagename='FrontPage')
        return process('wiki/page.html', page)

def edit(request, pagename):
    '''显示编辑页面'''
    page = Wiki.objects.get(pagename=pagename)
    return render_to_response('wiki/edit.html', {'pagename':pagename, 'content':page.content})

def save(request, pagename):
    '''保存页面内容并转到更新后的页面，如果页面已存在则更新它的内容，
    如果页面不存在，则新建这个页面'''
    content = request.POST['content']
    pages = Wiki.objects.filter(pagename=pagename)

    if pages:
        pages[0].content = content
        pages[0].save()
    else:
        page = Wiki(pagename=pagename, content=content)
        page.save()
    return HttpResponseRedirect('/wiki/%s' % pagename)


import re
r = re.compile(r'\b(([A-Z]+[a-z]+){2,})\b')
def process(template, page):
    '''处理页面链接，并将换行符转换为</br>'''
    t = loader.get_template(template)
    content = r.sub(r'<a href="/wiki/\1">\1</a>', page.content)
    content = re.sub(r'[\n\r]+', '<br/>', content)
    c = Context({'pagename':page.pagename, 'content':content})
    return HttpResponse(t.render(c))