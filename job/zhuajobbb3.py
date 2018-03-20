#coding=utf-8

import requests
import re
from lxml import etree
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

fs='http://www.mfengshen.com/'
play1='http://www.mfengshen.com/wapgame.php?sid=a630553b1827c84c16e9a48d4ae2625e'
play2='http://www.mfengshen.com/wapgame.php?sid=3a5471f442076c5978677d01b7f78f8c'
play3='http://www.mfengshen.com/wapgame.php?sid=8a83c871c3ddb6319078cd6dc868d3b5'
play4='http://www.mfengshen.com/wapgame.php?sid=a96b4191dfb3a279cb825b8238dd30e8'            #不问2914
play5='http://www.mfengshen.com/wapgame.php?sid=39f27ebaf9fe642c3d4142121e3e545d'            #不听133
play6='http://www.mfengshen.com/wapgame.php?sid=1e0532f360f9773973ff6d6109a2e6f9'            #不见260
play7='http://www.mfengshen.com/wapgame.php?sid=439f9b4e89691bdea972272815826975'
headers1={'Cookie':'__cfduid=d20b234861bd01d5177522544234cd5dd1519645825; community_url=http%3A%2F%2Fmpwap.cn; yjs_id=8e96627566eb6ec7060910726ea14423; ctrl_time=1; PHPSESSID=bp7622bakm3kjcprl48vbila51'}
headers2={'Cookie':'__cfduid=d881a7013fa50e872d87d847b23530dfa1519647681; community_url=http%3A%2F%2Fmpwap.cn; yjs_id=15589afa0f9c73b21265d9499e7629e9; ctrl_time=1; PHPSESSID=0tmu15i4dj6d7v1tnt3i56v8a3'}
headers3={'Cookie':'__cfduid=d40243c218679d894f9028cb16e50f13c1519647827; community_url=http%3A%2F%2Fmpwap.cn; yjs_id=56b48856607d35f1c77c4d742d0baaf9; ctrl_time=1; PHPSESSID=c0tu8vgfh4f09hqg27ujnffi97'}
headers4={'Cookie':'__cfduid=dffea663c5a3982bdcca5d25d4b85559e1519647744; community_url=http%3A%2F%2Fmpwap.cn; yjs_id=c738f3763bd9b9d90229830c233631c8; ctrl_time=1; PHPSESSID=udsefh1jfjesdmn0q745aeu2u7; monitor_count=16 __guid=219398303.2605231522356181000.1519647746372.664;'}
headers5={'Cookie':'__cfduid=d94a0eabb58a12e52788f1f4ce1323f161519818512; community_url=http%3A%2F%2Fmpwap.cn; yjs_id=2d87345504a06ca96bf76a43c162952f; ctrl_time=1; PHPSESSID=4vo2p21h4u6d0jdp8081hj5s75'}
headers6={'Cookie':'__cfduid=d4b5f1d57456fba8e82832539410c26f71519818684; community_url=http%3A%2F%2Fmpwap.cn; yjs_id=6de1c904c4b24c9978e2d9990b49c5e5; ctrl_time=1; PHPSESSID=59od1coe3hsnbhkue0mb2ordf4'}
#Chrome Firefox MicrosoftEdge 360se InternetExplorer Liebao

proxies={"http": "113.214.13.1:8000"}#长城宽带http://120.79.197.108:6666

zhandoumoney=0
experience=0
times=0
curetimes=0
global yuxinflag
yuxinflag=0
global realsl
realsl=0
global yuxin
yuxin=0
global jobmoney
jobmoney=0
global needcure
needcure=0

def login(player):
    lg0=requests.get(player,headers=headers3,proxies=proxies).content
    #print lg0.decode('utf-8')
    lg0=etn(lg0)
    #print lg0.xpath('string(//body)').decode('utf-8')      #显示页面内容，后期删除
    url0=searchurl(lg0,'封妖师OL一区-奇迹世界')
    #print url0

    lg1=requests.get(url0,headers=headers3,proxies=proxies).content
    #print lg1.decode('utf-8')
    if re.search('欢迎回家',lg1):
        print re.search(r'(欢迎回家,.*!)<br />',lg1).group(1).decode('utf-8')
        lg1=etn(lg1)
        #print lg1.xpath('string(//body)').decode('utf-8')      #显示页面内容，后期删除
        url1=searchurl(lg1,'我回来了')

        lg2=requests.get(url1,headers=headers3,proxies=proxies).content
        #print lg2.decode('utf-8')
        lg2=etn(lg2)
        #print lg2.xpath('string(//body)').decode('utf-8')      #显示页面内容，后期删除
        gameurl=searchurl(lg2,'进入游戏')

        if gameurl:
            print u'您已登录成功！'
        return gameurl

    elif re.search('刷新',lg1):
        print u'您仍在线！'
        lg1=etn(lg1)
        gameurl=searchurl(lg1,'刷新')

        return gameurl

    elif re.search('进入游戏',lg1):
        print u'您仍在线！'
        lg1=etn(lg1)
        gameurl=searchurl(lg1,'进入游戏')

        return gameurl

    elif re.search('主人,现在的情况是:',lg1):
        print u'您正处于战斗状态！'
        lg1=etn(lg1)
        print lg1.xpath('string(//body)').decode('utf-8')
        url1=fs+'fengshen/'+lg1.xpath('//body//a/@href')[0]
        gameurl=zhandou(url1)

        html=requests.get(gameurl,headers=headers3,proxies=proxies).content
        html=etn(html)
        gameurl=searchurl(html,'返回游戏')

        return gameurl

    else:
        print 'Something wrong!!!'

def job(gurl):
    html=requests.get(gurl,headers=headers3,proxies=proxies).content

    if re.search(r'这里有<a href="(.*)" title=".*</a><br />请选择你的行走方向:',html):
        gurl=fs+'fengshen/'+re.search(r'这里有<a href="(.*)" title=".*</a><br />请选择你的行走方向:',html).group(1)
    else:
        while 1:
            print u'这没有妖怪！！！'
            time.sleep(0.5)

    html=requests.get(gurl,headers=headers3,proxies=proxies).content
    if re.search('任务妖怪',html):
        print u'你找到了任务妖怪~~~'
        html=etn(html)
        gurl=searchurl(html,'任务妖怪')
    else:
        while 1:
            print u'这儿没有你的任务妖怪！！！'
            time.sleep(0.5)

    html=requests.get(gurl,headers=headers3,proxies=proxies).content
    while 1:
        if re.search(r'♀.*性格:保守 特性:蜕皮<br />属性:',html):
            name=re.search(r'继续寻找</a><br />(.*)<br /> <img',html).group(1).decode('utf-8')
            html=etn(html)
            gurl=searchurl(html,'挑战')
            html=requests.get(gurl,headers=headers3,proxies=proxies).content
            while 1:
                print u'你找到了一只保守蜕皮的'+name+u'！！！快快抓住！！！'
                time.sleep(0.5)
        elif re.search(r'♀.*性格:胆小 特性:蜕皮<br />属性:',html):
            name=re.search(r'继续寻找</a><br />(.*)<br /> <img',html).group(1).decode('utf-8')
            html=etn(html)
            gurl=searchurl(html,'挑战')
            html=requests.get(gurl,headers=headers3,proxies=proxies).content
            while 1:
                print u'你找到了一只胆小蜕皮的'+name+u'！！！快快抓住！！！'
                time.sleep(0.5)
        else:
            print u'你遇到了一只'+re.search(r'性格:(.*) 特性:.*<br />属性:',html).group(1).decode('utf-8')+re.search(r'性格:.* 特性:(.*)<br />属性:',html).group(1).decode('utf-8')+u'的'+re.search(r'继续寻找</a><br />(.*)<br /> <img',html).group(1).decode('utf-8')
            html=etn(html)
            gurl=searchurl(html,'继续寻找')
            html=requests.get(gurl,headers=headers3,proxies=proxies).content

def etn(html):      #etree化字符串，同时将<br>标签转换为换行符
    html=re.sub('<br>','\n',html)
    html=re.sub('<br />','\n',html)
    html=etree.HTML(html)
    return html

def searchurl(html,st):      #在html中寻找st字符串对应的url
    for a in html.xpath('//body//a'):
        if re.search(st,a.xpath('text()')[0].encode('utf-8')):
            if re.search('/',a.xpath('@href')[0].encode('utf-8')):            #首页进入下层链接
                return fs+a.xpath('@href')[0]
            else:                                            #其余页面就在首页进入的下层链接的该层进行跳转
                return fs+'fengshen/'+a.xpath('@href')[0]

def main():
    gurl=login(play3)
    job(gurl)

if __name__ == '__main__':
    main()
