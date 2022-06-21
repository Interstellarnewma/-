import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
result={
    '新闻标题':[],
    '发布时间':[],
    '发布内容':[]
}#建立一个字典类型
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}
url='https://news.163.com/'
page_text=requests.get(url=url,headers=headers).content
#需要在首页中解析----实例化
soup=BeautifulSoup(page_text,'lxml')
li_list=soup.select('.hidden > div')
#寻找网页的详细地址url
for li in li_list:
        detail_url = li.a['href']#将网页的详细地址一一取出
        if 'data' in detail_url:#独家栏目中的的页面布局不同
            detal_page_data_text = requests.get(url=detail_url, headers=headers).text
            tree2=etree.HTML(detal_page_data_text)
            title2 = tree2.xpath('//div[@class="main-a clearfix"]/div[@class="left"]/h1/text()')[0]
            result['新闻标题'].append(title2)
            time2 = tree2.xpath('//div[@class="main-a clearfix"]/div[@class="left"]/div[@class="main-info"]/p[1]/text()')[0]
            result['发布时间'].append(time2)
            content2 =tree2.xpath('//div[@class="main-content"]/div/p/text()')
            content2_detail = " ".join(content2)
            result['发布内容'].append(content2_detail)

        else:
            detal_page_text = requests.get(url=detail_url, headers=headers).text#对网站的详情地址进行访问
            tree = etree.HTML(detal_page_text)
            title = tree.xpath('//div[@class="post_main"]/h1[@class="post_title"]/text()')#通过xpath进行访问
            if len(title) > 0:#防止出现错误
                title = title[0]
                result['新闻标题'].append(title)
            time = tree.xpath('//div[@class="post_main"]/div[@class="post_info"]/text()')
            if len(time) > 0:
                time = time[0].strip()
                time_need = time[0:19]#仅取出那些我们需要的时间
                result['发布时间'].append(time_need)
            detail_content = tree.xpath('//div[@class="post_main"]/div[@class="post_content"]/div[@class="post_body"]/p/text()')
            content = " ".join(detail_content)#将那些列表中的正文内容取出
            result['发布内容'].append(content)
print('已获取')
df =pd.DataFrame.from_dict(result, orient='index')
df.to_csv("news.csv", encoding="utf_8_sig")  # 进行持久化存储
print('存储成功')



