from personal_python_collections.networking import *
from personal_python_collections.BeautifulSoup_utility import *
from personal_python_collections.regexp_string import *
from personal_python_collections.file_manager import *

help_string = """
----------------- START -------------------
type             -> <class 'bs4.element.Tag'>
name             -> div
attrs            -> {'class': ['center']}
string           -> Center text
text             -> Center text
contents         -> ['Center text']
children         -> <list_iterator object at 0x10347d710>
descendants      -> <generator object descendants at 0x10343cf68>
parent           -> <class 'bs4.element.Tag'>
parents          -> <class 'generator'>
next_sibling     ->

previous_sibling ->

next_element     -> Center text
previous_element ->

-----------------  END  -------------------
"""


def game_sky():
    # 获取网页文本
    url = "http://sx.gamersky.com/Soft/tv/xbox360/0-0-0-0-0-0-0-00.html"
    web_text = Networking(url).get().response.text

    # 开始分析
    if len(web_text):

        # 初始化并查询固定的数据
        soup_manager = BeautifulSoupManager(web_text)
        for item in soup_manager.find_all('div', 'class = download_content'):

            # 开始查找所有的子节点
            for data in item.descendants:

                # 确保是Tag对象
                if BeautifulSoupElement(data).is_Tag:

                    # 找到了div class="download_title"的Tag
                    if BeautifulSoupElement(data).is_match('div', 'class = download_title'):
                        print("网页名字：%s" % data.string)

                    # 找到了div class="download_pic"的Tag
                    if BeautifulSoupElement(data).is_match('div', 'class = download_pic'):
                        print("下载地址：%s" % data.a['href'])
                        print("图片地址：%s" % data.a.img['src'])

                    # 找到span class="short_title"的Tag
                    if BeautifulSoupElement(data).is_match('span', 'class = short_title'):
                        print("%s%s" % (data.string, data.next_sibling.string))

            print()
            print()


def pu_jia():
    # 获取网页文本
    url = "http://www.pujia8.com/library/category/psp/?page=1#comments"
    web_text = Networking(url).get().response.text

    # 开始分析
    if len(web_text):

        # 初始化并查询固定的数据
        soup_manager = BeautifulSoupManager(web_text)
        for item in soup_manager.find_all('div', 'class = game_list'):

            # 开始查找当前以下的一级子节点
            count = 0
            for data in item.contents:

                # 找出所有Tag对象
                if BeautifulSoupElement(data).is_Tag:

                    if count == 0:
                        print("标题: " + data['title'])
                        print("链接: " + "http://www.pujia8.com" + data['href'])
                        print("图片: " + "http://www.pujia8.com" + data.div.img['src'])

                    if count == 1:
                        print("语言: " + data.string)

                    if count == 2:
                        print("名字: " + data.string)

                    count += 1

            print()


def cn_blog():
    # 获取网页文本
    url = "http://www.cnblogs.com/yufeihlf/"
    web_text = Networking(url).get().response.text

    # 开始分析
    if len(web_text):

        # 初始化并查询固定的数据
        soup_manager = BeautifulSoupManager(web_text)
        for item in soup_manager.find_all('div', 'class = day'):

            # 开始查找当前以下的一级子节点
            count = 0
            for data in item.contents:

                # 找出所有Tag对象
                if BeautifulSoupElement(data).is_Tag:

                    if BeautifulSoupElement(data).is_match('div', 'class = postTitle'):
                        count += 2
                        print("标题   : " + data.a.text)
                        print("链接   : " + data.a['href'])

                    if BeautifulSoupElement(data).is_match('div', 'class = postCon'):
                        count += 1
                        print("摘要   : " +
                              RegExpString(data.div.text)
                              .search_with_pattern(r'(?<=摘要: ).+(?=阅读全文)')
                              .search_result)

                    if BeautifulSoupElement(data).is_match('div', 'class = postDesc'):
                        count += 1

                        # print("信息   : " + data.text)
                        source_str = data.text
                        time_str = RegExpString(source_str) \
                            .search_with_pattern(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}') \
                            .search_result
                        print("时间   : " + time_str)

                        read_count_str = RegExpString(source_str).search_with_pattern(r'(?<=阅读.)\d+').search_result
                        print("阅读   : " + read_count_str)

                        comment_str = RegExpString(source_str).search_with_pattern(r'(?<=评论.)\d+').search_result
                        print("评论   : " + comment_str)

                        author_str = RegExpString(source_str).search_with_pattern(r'(?<=:\d\d ).+(?= 阅读)').search_result
                        print("作者   : " + author_str)

                    if count % 4 == 0:
                        print()


# 时光网数据抓取
def m_time():

    # 存储抓取的对象
    obj_list = []

    def analysis_web_text(text, count=None):

        # 开始分析
        if len(text):

            # 初始化并查询固定的数据
            soup_manager = BeautifulSoupManager(text)
            for item in soup_manager.find_all('ul', 'id = newslist'):

                for data in item.contents:

                    # 抓取的对象
                    obj_dic = {}
                    if BeautifulSoupElement(item).is_Tag:

                        # debug
                        if 0:
                            print("链接 : " + data.div.a['href'])
                            print("图片 : %s " % RegExpString("%s" % data.div.a.img)
                                  .search_with_pattern(r'(?<=src=")http.+?(?=")')
                                  .search_result)
                            print("标题 : %s " % data.div.h4.a.text)
                            print("介绍 : %s " % data.div.p.a.text)
                            print("时间 : %s " % data.div.span.text)
                            print()

                        obj_dic['href'] = data.div.a['href']
                        obj_dic['pic'] = RegExpString("%s" % data.div.a.img).search_with_pattern(
                            r'(?<=src=")http.+?(?=")') \
                            .search_result
                        obj_dic['title'] = data.div.h4.a.text
                        obj_dic['des'] = data.div.p.a.text
                        obj_dic['time'] = data.div.span.text
                        obj_list.append(obj_dic)

            print("成功抓取第%s页!" % count)

    # 所有要抓取的网页列表
    url_list = list()
    url_list.append('http://news.mtime.com')
    for i in range(2, 11):
        url_list.append('http://news.mtime.com/index-%s.html' % i)

    # 获取网页文本
    page_count = 0
    for tmp_url in url_list:

        page_count += 1
        web_text = Networking(tmp_url).get().response.text
        analysis_web_text(web_text, page_count)

    # 如果成功抓取了数据
    if len(obj_list):
        replace_str = """
                <div class="box">
                <div class="child">

                    <div class="fixedimage">
                        <img src="#image#">
                    </div>

                    <p title="title">
                        <a href="#href#">#title#</a>
                    </p>

                    <p title="subtitle">
                        #subtitle#
                    </p>

                </div>
            </div>
        """

        total_str = ""

        for obj_data in obj_list:
            tmp_str = replace_str
            tmp_str = RegExpString(tmp_str).replace_with_pattern(r'#image#', obj_data['pic']).replace_result
            tmp_str = RegExpString(tmp_str).replace_with_pattern(r'#href#', obj_data['href']).replace_result
            tmp_str = RegExpString(tmp_str).replace_with_pattern(r'#subtitle#', obj_data['des']).replace_result
            tmp_str = RegExpString(tmp_str).replace_with_pattern(r'#title#', obj_data['title']).replace_result
            total_str += tmp_str

        # 打开本地pattern.html模板
        all_the_data = open(File.path(suffix_path='mtime_pattern.html'), 'rb').read().decode('utf-8')
        all_the_data = RegExpString(all_the_data).replace_with_pattern(r'##########', total_str).replace_result

        # 开始写文件
        file = open(File.path(suffix_path='mtime.html'), 'w')
        file.write(all_the_data)
        file.close()

        print("生成的网页在 %s ,直接打开即可." % File.path(suffix_path='mtime.html'))


m_time()
