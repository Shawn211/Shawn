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
play4='http://www.mfengshen.com/wapgame.php?sid=a96b4191dfb3a279cb825b8238dd30e8'			#不问2914
play5='http://www.mfengshen.com/wapgame.php?sid=39f27ebaf9fe642c3d4142121e3e545d'			#不听133
play6='http://www.mfengshen.com/wapgame.php?sid=1e0532f360f9773973ff6d6109a2e6f9'			#不见260
play7='http://www.mfengshen.com/wapgame.php?sid=439f9b4e89691bdea972272815826975'
headers1={'Cookie':'__cfduid=d20b234861bd01d5177522544234cd5dd1519645825; community_url=http%3A%2F%2Fmpwap.cn; yjs_id=8e96627566eb6ec7060910726ea14423; ctrl_time=1; PHPSESSID=bp7622bakm3kjcprl48vbila51'}
headers2={'Cookie':'__cfduid=d881a7013fa50e872d87d847b23530dfa1519647681; community_url=http%3A%2F%2Fmpwap.cn; yjs_id=15589afa0f9c73b21265d9499e7629e9; ctrl_time=1; PHPSESSID=0tmu15i4dj6d7v1tnt3i56v8a3'}
headers3={'Cookie':'__cfduid=d40243c218679d894f9028cb16e50f13c1519647827; community_url=http%3A%2F%2Fmpwap.cn; yjs_id=56b48856607d35f1c77c4d742d0baaf9; ctrl_time=1; PHPSESSID=c0tu8vgfh4f09hqg27ujnffi97'}
headers4={'Cookie':'__cfduid=dffea663c5a3982bdcca5d25d4b85559e1519647744; community_url=http%3A%2F%2Fmpwap.cn; yjs_id=c738f3763bd9b9d90229830c233631c8; ctrl_time=1; PHPSESSID=udsefh1jfjesdmn0q745aeu2u7; monitor_count=16 __guid=219398303.2605231522356181000.1519647746372.664;'}
headers5={'Cookie':'__cfduid=d94a0eabb58a12e52788f1f4ce1323f161519818512; community_url=http%3A%2F%2Fmpwap.cn; yjs_id=2d87345504a06ca96bf76a43c162952f; ctrl_time=1; PHPSESSID=4vo2p21h4u6d0jdp8081hj5s75'}
headers6={'Cookie':'__cfduid=d4b5f1d57456fba8e82832539410c26f71519818684; community_url=http%3A%2F%2Fmpwap.cn; yjs_id=6de1c904c4b24c9978e2d9990b49c5e5; ctrl_time=1; PHPSESSID=59od1coe3hsnbhkue0mb2ordf4'}
#Chrome Firefox MicrosoftEdge 360se InternetExplorer Liebao

proxies={"http": ""}#长城宽带http://120.79.197.108:6666

zhandoumoney=0
experience=0
times=0
curetimes=0
global realsl
realsl=0
global jobmoney
jobmoney=0
global jobfwm
jobfwm=0
global jobkr
jobkr=0
global jobdan
jobdan=0

def login(player):
	lg0=requests.get(player,headers=headers2,proxies=proxies).content
	#print lg0.decode('utf-8')
	lg0=etn(lg0)
	#print lg0.xpath('string(//body)').decode('utf-8')      #显示页面内容，后期删除
	url0=searchurl(lg0,'封妖师OL一区-奇迹世界')
	#print url0

	lg1=requests.get(url0,headers=headers2,proxies=proxies).content
	#print lg1.decode('utf-8')
	if re.search('欢迎回家',lg1):
		print re.search(r'(欢迎回家,.*!)<br />',lg1).group(1).decode('utf-8')
		lg1=etn(lg1)
		#print lg1.xpath('string(//body)').decode('utf-8')      #显示页面内容，后期删除
		url1=searchurl(lg1,'我回来了')

		lg2=requests.get(url1,headers=headers2,proxies=proxies).content
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

		return gameurl

	else:
		print 'Something wrong!!!'

def job(gurl):
	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	if re.search(r'北 山间小路↑.*南 山路↓',html):
		gurl=searchurl(etn(html),'北 山间小路↑')
		html=requests.get(gurl,headers=headers2,proxies=proxies).content

		gurl=searchurl(etn(html),'确定进入')
		html=requests.get(gurl,headers=headers2,proxies=proxies).content

		if re.search(r'你遇到了.*杨百万',html):
			print u'你成功进入了山间小路副本！请开始你的表演！'
			gurl=searchurl(etn(html),'刷新')
		else:
			while 1:
				print u'你来到了哪了啊你，赶紧的上山啦！'
				time.sleep(0.5)

	if re.search('山间小路 ',html):
		gurl=checkbb(gurl)

	while 1:
		html=requests.get(gurl,headers=headers2,proxies=proxies).content

		if re.search('山间小路 ',html):

			print '---------------------'
			print u'山间小路'
			print u'蜿蜒曲折的山路通往深山之中,有一名道士装扮的隐士在路边站着。'
			print u'你遇到了杨百万'
			print u'肥头大耳的商人,眼睛眯成了一条线,脸上的肉堆得像“油团”。随身携带着几只厉害的妖怪。'
			print u'身上带有70级地狼,72级青牛,74级开明兽,76级陆吾,78级诸犍'
			print u'杨百万对你说:唉,山上的七个妖怪抢了我的货物,你能帮我剿灭妖怪吗？'
			print '---------------------'

			gurl=searchurl(etn(html),'杨百万')
			html=requests.get(gurl,headers=headers2,proxies=proxies).content

			if not re.search('挑战',html):
				gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
				html=requests.get(gurl,headers=headers2,proxies=proxies).content

			gurl=searchurl(etn(html),'挑战')
			print u'挑战山间小路杨百万！(土、动、日土、风仙、雷动)'
			gurl=zhandou(gurl)
			gurl=checkgim(gurl)
			gurl=checkjob(gurl)
			gurl=checkjob(gurl)
			gurl=relaxbb(gurl)

			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')

		elif re.search('石桥 ',html):

			print '---------------------'
			print u'石桥'
			print u'巨石天然形成的拱桥,长满了青苔。'
			print u'你遇到了山贼'
			print u'落草为寇的山贼,盘踞在梅山山脚抢劫来往路人。'
			print u'身上带有58级战牛,60级瞑蛟,62级天狐,64级黑蓝虎,66级室火猪'
			print u'山贼对你说:嗨,小子！此山是我开,此树是我栽,要想从此过,留下买路财！'
			print '---------------------'

			gurl=searchurl(etn(html),'刷新')
			gurl=checkgim(gurl)

			gurl=walk(gurl,'w')
			html=requests.get(gurl,headers=headers2,proxies=proxies).content

			#若很多拦路者，可将此设置到walk函数
			if not re.search('三潭飞瀑 ',html):
				gurl=searchurl(etn(html),'北 三潭飞瀑↑')
				html=requests.get(gurl,headers=headers2,proxies=proxies).content

				gurl=searchurl(etn(html),'挑战山贼')

				gurl=zhandou(gurl)
				gurl=checkgim(gurl)

				gurl=walk(gurl,'w')
				gurl=walk(gurl,'d')

			elif re.search('三潭飞瀑 ',html):
				gurl=searchurl(etn(html),'东 三潭飞瀑→')

			gurl=walk(gurl,'d')
			gurl=walk(gurl,'d')
			gurl=walk(gurl,'d')

			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')

		elif re.search('云门 ',html):

			print '---------------------'
			print u'云门'
			print u'通往山顶的必经之路,四周云气氤氲,宛如天幕；云海翻滚,瞬息万变。'
			print u'你遇到了无头行者'
			print u'无头尸身,吸收日月精华,成为僵尸。'
			print u'身上带有60级猪不戒,62级凤,64级必方,66级神辉,68级大风'
			print u'无头行者对你说:吼～'
			print '---------------------'

			gurl=searchurl(etn(html),'刷新')

			gurl=walk(gurl,'a')

		elif re.search('柏树林 ',html):
			#寻找常昊
			while not re.search(r'你遇到了.*常昊',html):
				gurl=searchurl(etn(html),'刷新')
				html=requests.get(gurl,headers=headers2,proxies=proxies).content

				while re.search('南 柏树林↓',html):
					gurl=walk(gurl,'s')
					html=requests.get(gurl,headers=headers2,proxies=proxies).content

				if re.search(r'柏树林 .*北 柏树林↑.*东 柏树林→.*南 松树林↓',html):
					gurl=walk(gurl,'d')

				elif re.search(r'柏树林 .*北 柏树林↑.*西 柏树林←.*东 云门→',html):
					gurl=walk(gurl,'a')

				else:
					print u'看来已经找到常昊了，我们好好教训教训他吧！'
					gurl=searchurl(etn(html),'刷新')

			print '---------------------'
			print u'柏树林'
			print u'山顶的柏树林,柏树雄伟苍劲、巍峨挺拔、四季长青,使高山仿佛都充满了灵气。'
			print u'你遇到了常昊'
			print u'青面獠牙,口吐毒烟,全身长有奇异斑纹。'
			print u'身上带有70级眼镜蛇,72级巨蟒,74级应龙,76级翼火蛇,78级钩蛇'
			print u'常昊对你说:据说大荒内存在着一只山海异兽,可吸取天地金气碎金斩石,其名为吼。'
			print '---------------------'

			gurl=searchurl(etn(html),'常昊')
			html=requests.get(gurl,headers=headers2,proxies=proxies).content

			if not re.search('挑战',html):
				gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
				html=requests.get(gurl,headers=headers2,proxies=proxies).content

			gurl=searchurl(etn(html),'挑战')
			print u'挑战柏树林常昊！(木、木动、水雷、火、木)'
			gurl=zhandou(gurl)
			gurl=checkgim(gurl)

			#寻找出口
			html=requests.get(gurl,headers=headers2,proxies=proxies).content
			while not re.search(r'柏树林 .*北 上十八盘↑.*西 松树林←.*东 柏树林→.*南 柏树林↓',html):
				gurl=searchurl(etn(html),'刷新')
				html=requests.get(gurl,headers=headers2,proxies=proxies).content

				while re.search('北 柏树林↑',html):
					gurl=walk(gurl,'w')
					html=requests.get(gurl,headers=headers2,proxies=proxies).content

				if re.search(r'柏树林 .*西 柏树林←.*东 柏树林→.*南 柏树林↓',html):
					gurl=walk(gurl,'a')

				elif re.search(r'柏树林 .*西 柏树林←.*南 柏树林↓',html):
					gurl=walk(gurl,'a')

				else:
					print u'看来已经找到出口了，我们接着前行吧！'
					gurl=searchurl(etn(html),'刷新')

			gurl=walk(gurl,'w')
			gurl=walk(gurl,'d')
			gurl=walk(gurl,'w')

		elif re.search('云海 ',html):

			print '---------------------'
			print u'云海'
			print u'流云奔涌、群山浮动,宏伟壮观,宛如仙境。'
			print u'你遇到了朱子真'
			print u'肥头大耳、膀大腰圆,浑身长满了黑色鬓毛,喜吃,口有恶臭。'
			print u'身上带有70级仔猪,72级野猪,74级并封,76级室火猪,78级猪不戒'
			print u'朱子真对你说:听说人肉很好吃？'
			print '---------------------'

			gurl=searchurl(etn(html),'朱子真')
			html=requests.get(gurl,headers=headers2,proxies=proxies).content

			if not re.search('挑战',html):
				gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
				html=requests.get(gurl,headers=headers2,proxies=proxies).content

			gurl=searchurl(etn(html),'挑战')
			print u'挑战朱子真！(妖、妖、日妖、火、妖)'
			gurl=zhandou(gurl)
			gurl=checkgim(gurl)

			gurl=walk(gurl,'a')
			gurl=walk(gurl,'a')
			gurl=walk(gurl,'a')
			gurl=walk(gurl,'w')

		elif re.search('长蛇洞 ',html):

			print '---------------------'
			print u'长蛇洞'
			print u'漆黑的山洞,洞内曲曲折折,阴森可怕。'
			print u'你遇到了吴龙'
			print u'穿着紫色盔甲,手持双刀,身躯被黑雾包裹的蜈蚣精。'
			print u'身上带有70级商羊,72级参水猿,74级轸水蚓,76级魑魅,78级柃柃'
			print u'吴龙对你说:本圣的黑雾剧毒无比,谁人可敌？哈哈哈……'
			print '---------------------'

			gurl=searchurl(etn(html),'吴龙')
			html=requests.get(gurl,headers=headers2,proxies=proxies).content

			if not re.search('挑战',html):
				gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
				html=requests.get(gurl,headers=headers2,proxies=proxies).content

			gurl=searchurl(etn(html),'挑战')
			print u'挑战长蛇洞吴龙！(水、水、水、月、水)'
			gurl=zhandou(gurl)
			gurl=checkgim(gurl)

			gurl=walk(gurl,'s')
			gurl=walk(gurl,'d')
			gurl=walk(gurl,'d')
			gurl=walk(gurl,'d')
			gurl=walk(gurl,'d')
			gurl=walk(gurl,'d')
			gurl=walk(gurl,'d')
			gurl=walk(gurl,'w')

		elif re.search('白猿洞 ',html):

			print '---------------------'
			print u'白猿洞'
			print u'山岩间一大片绿茵茵的青藤直垂下来,遮着一个洞门,神秘幽静。'
			print u'你遇到了袁洪'
			print u'梅山七圣之首,千年猿猴,修炼有成、神通广大。'
			print u'身上带有70级傲因,72级孙小圣,74级凿齿,76级参水猿,78级山臊'
			print u'袁洪对你说:吾虽为妖,必为妖王！'
			print '---------------------'

			gurl=searchurl(etn(html),'袁洪')
			html=requests.get(gurl,headers=headers2,proxies=proxies).content

			if not re.search('挑战',html):
				gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
				html=requests.get(gurl,headers=headers2,proxies=proxies).content

			gurl=searchurl(etn(html),'挑战')
			print u'挑战白猿洞袁洪！(人、仙、人、水、土)'
			gurl=zhandou(gurl)
			gurl=checkgim(gurl)

			gurl=walk(gurl,'s')
			gurl=walk(gurl,'a')
			gurl=walk(gurl,'a')
			gurl=walk(gurl,'a')
			gurl=walk(gurl,'w')

		elif re.search('梅花亭 ',html):

			print '---------------------'
			print u'梅花亭'
			print u'八角梅花亭,上铺琉璃瓦。亭旁蹲着四只妖兽石像。'
			print u'你遇到了金大升'
			print u'长有一对金色的牛角,口吐牛黄,力大无穷。'
			print u'身上带有70级战牛,72级小牛魔王,74级牛头鬼,76级牛金牛,78级那父'
			print u'金大升对你说:力拔山兮气盖世,说的正是本大圣！'
			print '---------------------'

			gurl=searchurl(etn(html),'金大升')
			html=requests.get(gurl,headers=headers2,proxies=proxies).content

			if not re.search('挑战',html):
				gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
				html=requests.get(gurl,headers=headers2,proxies=proxies).content

			gurl=searchurl(etn(html),'挑战')
			print u'挑战梅花亭金大升！(金、金妖、妖、金、金)'
			gurl=zhandou(gurl)
			gurl=checkgim(gurl)

			gurl=walk(gurl,'w')

		elif re.search('梅山顶 ',html):

			print '---------------------'
			print u'梅山顶'
			print u'梅山山顶,云海翻腾。极目远望,梅山风貌,尽收眼底。'
			print u'你遇到了戴礼'
			print u'身高一米,长有四颗尖牙,能口吐红珠,百步伤人。'
			print u'身上带有70级棱犬,72级哮天犬,74级娄金狗,76级狍鄂,78级吼'
			print u'戴礼对你说:听说各种宝石是好东西啊,能增加妖怪的合成的成功率,看来得下山去搞点。'
			print '---------------------'

			gurl=searchurl(etn(html),'戴礼')
			html=requests.get(gurl,headers=headers2,proxies=proxies).content

			if not re.search('挑战',html):
				gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
				html=requests.get(gurl,headers=headers2,proxies=proxies).content

			gurl=searchurl(etn(html),'挑战')
			print u'挑战梅山顶戴礼！(火、动、金、妖、金)'
			gurl=zhandou(gurl)
			gurl=checkgim(gurl)

			gurl=walk(gurl,'w')

		elif re.search('七圣观 ',html):

			print '---------------------'
			print u'七圣观'
			print u'梅山七圣为自己建造的庙宇,阴森诡异。'
			print u'你遇到了杨显'
			print u'满头白发,留着一撮山羊胡,眯着双眼,透露着丝丝邪气。'
			print u'身上带有70级羊羔,72级山羊,74级鬼金羊,76级羊丞相,78级山魈'
			print u'杨显对你说:山下那个杨百万居然想诛杀我梅山七圣,可恶！'
			print '---------------------'

			gurl=searchurl(etn(html),'杨显')
			html=requests.get(gurl,headers=headers2,proxies=proxies).content

			if not re.search('挑战',html):
				gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
				html=requests.get(gurl,headers=headers2,proxies=proxies).content

			gurl=searchurl(etn(html),'挑战')
			print u'挑战杨显！(日、日、金、人日、妖)'
			gurl=zhandou(gurl)
			gurl=checkgim(gurl)
			gurl=checkjob(gurl)
			gurl=checkjob(gurl)
			gurl=checkbb(gurl)

			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')

		else:
			print u'你不存在于梅山山间小路，也不存在于小客栈。你不存在于我给你创造的世界。'

def checkjob(gurl):
	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	if re.search('有没有兴趣',html):
		gurl=fs+'fengshen/'+re.search(r'对你说:.*<a href="(.*)" title="查看">查看</a><br />请选择你的行走方向:',html).group(1)

		html=requests.get(gurl,headers=headers2,proxies=proxies).content
		html=etn(html)

		gurl=searchurl(html,'接受任务')

		html=requests.get(gurl,headers=headers2,proxies=proxies).content
		if re.search(r'你接受了.*任务!',html):
			print re.search(r'你接受了.*任务!',html).group(0).decode('utf-8')

		elif re.search(r'副本限额,无法接受!',html):
			while 1:
				print re.search(r'副本限额,无法接受!',html).group(0).decode('utf-8')
				time.sleep(0.5)

		html=etn(html)
		gurl=searchurl(html,'返回游戏')

		return gurl

	elif re.search('快来领奖吧! ',html):
		while re.search('快来领奖吧! ',html):
			gurl=fs+'fengshen/'+re.search(r'快来领奖吧! <a href="(.*)" title="领奖">领奖</a><br />请选择你的行走方向:',html).group(1)

			html=requests.get(gurl,headers=headers2,proxies=proxies).content

			if re.search('背包已满,无法领奖!',html):
				print u'背包已满,无法领奖!'
				html=etn(html)
				gurl=searchurl(html,'返回游戏')

				gurl=fullbag(gurl)

				html=requests.get(gurl,headers=headers2,proxies=proxies).content
			else:
				while not re.search('返回游戏',html):
					html=etn(html)
					gurl=fs+'fengshen/'+html.xpath('//body//a/@href')[0]
					html=requests.get(gurl,html).content

				global jobmoney
				if re.search(r'。<br />你获得了.*枚铜板。<br />',html):
					jobmoney=jobmoney+int(re.search(r'。<br />你获得了(\d*)枚铜板。<br />',html).group(1))
					print re.search(r'。<br />(你获得了\d*枚铜板)。<br />',html).group(1).decode('utf-8')+u'！'
					print u'\n你获得任务赏金共'+str(jobmoney)+u'枚铜板。\n'

				if re.search('副本金钱已达到每日限额',html):
					print u'副本金钱已达到每日限额！！！'
					print u'副本金钱已达到每日限额！！！'
					print u'副本金钱已达到每日限额！！！'
					print u'\n你获得任务赏金共'+str(jobmoney)+u'枚铜板。\n'

				global jobfwm
				if re.search(r'。<br />你获得了.*个蜂王蜜。<br />',html):
					jobfwm=jobfwm+int(re.search(r'。<br />你获得了(\d*)个蜂王蜜。<br />',html).group(1))
					print re.search(r'。<br />(你获得了\d*个蜂王蜜。)。<br />',html).group(1).decode('utf-8')+u'！'
					print u'\n你获得任务奖励共'+str(jobfwm)+u'个蜂王蜜。\n'

				global jobkr
				if re.search(r'。<br />你获得了.*块烤肉。<br />',html):
					jobkr=jobkr+int(re.search(r'。<br />你获得了(\d*)块烤肉。<br />',html).group(1))
					print re.search(r'。<br />(你获得了\d*块烤肉。)。<br />',html).group(1).decode('utf-8')+u'！'
					print u'\n你获得任务奖励共'+str(jobkr)+u'块烤肉。\n'

				global jobdan
				if re.search(r'。<br />你获得了.*颗含有15000点经验的经验内丹。<br />',html):
					jobdan=jobdan+int(re.search(r'。<br />你获得了(\d*)颗含有15000点经验的经验内丹。<br />',html).group(1))
					print re.search(r'。<br />(你获得了\d*颗含有15000点经验的经验内丹。)。<br />',html).group(1).decode('utf-8')+u'！'
					print u'\n你获得任务奖励共'+str(jobdan)+u'颗含有15000点经验的经验内丹。\n'

				html=etn(html)
				gurl=searchurl(html,'返回游戏')
				html=requests.get(gurl,headers=headers2,proxies=proxies).content

		html=etn(html)
		gurl=searchurl(html,'刷新')

		return gurl

	else:
		html=etn(html)
		return searchurl(html,'刷新')

def checkgim(gurl):
	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	while re.search(r'地上有',html):
		gurl=fs+'fengshen/'+re.search(r'地上有<a href="(.*)" title=".*">.*</a><br />请选择你的行走方向:',html).group(1)

		html=requests.get(gurl,headers=headers2,proxies=proxies).content

		if re.search('你在找什么东西?',html):
			print u'你看都没看清，gimgim宝贝就被人家捡走了~'
			gurl=searchurl(etn(html),'返回游戏')
			html=requests.get(gurl,headers=headers2,proxies=proxies).content

		while not re.search('刷新',html):
			html=etn(html)

			gurl=fs+'fengshen/'+html.xpath('//body//a/@href')[0]
			html=requests.get(gurl,headers=headers2,proxies=proxies).content

			if re.search(r'(你获得了.*)。<br>.*刷新',html):
				print u'你被广播捡到gimgim宝贝了！！！'
				print u'你被广播捡到gimgim宝贝了！！！'
				print u'你被广播捡到gimgim宝贝了！！！'
				print re.search(r'(你获得了.*)。.*刷新',html).group(1).decode('utf-8')+u'！！！\n'
				print re.search(r'(你获得了.*)。.*刷新',html).group(1).decode('utf-8')+u'！！！\n'
				print re.search(r'(你获得了.*)。.*刷新',html).group(1).decode('utf-8')+u'！！！'

			elif re.search(r'(你获得了.*)。<br />.*刷新',html):
				print re.search(r'(你获得了.*)。.*刷新',html).group(1).decode('utf-8')+u'！！！\n'
				print re.search(r'(你获得了.*)。.*刷新',html).group(1).decode('utf-8')+u'！！！\n'
				print re.search(r'(你获得了.*)。.*刷新',html).group(1).decode('utf-8')+u'！！！'

			elif re.search(r'你要捡的东西已经不在这里了。',html):
				print u'你差一点就捡到gimgim宝贝了，可惜被别人抢先一步了~'

		if re.search('抱歉,您的背包已满。',html):
			print u'背包已满，捡不起gimgim宝贝！'

			html=etn(html)
			gurl=searchurl(html,'刷新')

			gurl=fullbag(gurl)

			html=requests.get(gurl,headers=headers2,proxies=proxies).content

	html=etn(html)
	gurl=searchurl(html,'刷新')

	return gurl

def checkbb(gurl):#设置bb和bb血量
	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'宠物')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'翼火蛇')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content

	nowhp=int(re.search(r'生命:(\d\d?\d?\d?)/\d\d?\d?\d?\+?\d?\d?\d?\d? 忠诚度:',html).group(1))

	if re.search(r'\+',re.search(r'生命:\d\d?\d?\d?/\d\d?\d?\d?\+?\d?\d?\d?\d? 忠诚度:',html).group(0)):
		hp=int(re.search(r'生命:\d\d?\d?\d?/(\d\d?\d?\d?)\+?\d?\d?\d?\d? 忠诚度:',html).group(1))+int(re.search(r'生命:\d\d?\d?\d?/\d\d?\d?\d?\+?(\d?\d?\d?\d?) 忠诚度:',html).group(1))
	else:
		hp=int(re.search(r'生命:\d\d?\d?\d?/(\d\d?\d?\d?) 忠诚度:',html).group(1))

	while nowhp < (hp-85):
		gurl=searchurl(etn(html),'喂食药品')

		html=requests.get(gurl,headers=headers2,proxies=proxies).content
		gurl=searchurl(etn(html),'续命丹')

		html=requests.get(gurl,headers=headers2,proxies=proxies).content
		gurl=searchurl(etn(html),'返回上级')

		html=requests.get(gurl,headers=headers2,proxies=proxies).content

		nowhp=int(re.search(r'生命:(\d\d?\d?\d?)/\d\d?\d?\d?\+?\d?\d?\d?\d? 忠诚度:',html).group(1))

		if re.search(r'\+',re.search(r'生命:\d\d?\d?\d?/\d\d?\d?\d?\+?\d?\d?\d?\d? 忠诚度:',html).group(0)):
			hp=int(re.search(r'生命:\d\d?\d?\d?/(\d\d?\d?\d?)\+?\d?\d?\d?\d? 忠诚度:',html).group(1))+int(re.search(r'生命:\d\d?\d?\d?/\d\d?\d?\d?\+?(\d?\d?\d?\d?) 忠诚度:',html).group(1))
		else:
			hp=int(re.search(r'生命:\d\d?\d?\d?/(\d\d?\d?\d?) 忠诚度:',html).group(1))

	gurl=fs+'fengshen/'+etree.HTML(html).xpath('//body//a/@href')[-5]

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'凫水')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'设为默认法术')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'返回游戏')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'宠物')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'宠物排序')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'角木蛟')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	if re.search(r'请选择第\d只出场的宠物:',html):
		gurl=searchurl(etn(html),'翼火蛇')
		html=requests.get(gurl,headers=headers2,proxies=proxies).content

	while re.search(r'请选择第\d只出场的宠物:',html):
		gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
		html=requests.get(gurl,headers=headers2,proxies=proxies).content

	gurl=searchurl(etn(html),'角木蛟')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'喂食药品')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'小还丹')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	if re.search(r'出窍',html):
		if int(re.search(r'出窍</a>\((\d*)/10\)',html).group(1)) < 4:
			gurl=searchurl(etn(html),'出窍')

		elif int(re.search(r'出窍</a>\((\d*)/10\)',html).group(1)) == 0:
			gurl=searchurl(etn(html),'出窍')

			html=requests.get(gurl,headers=headers2,proxies=proxies).content
			gurl=searchurl(etn(html),'返回上级')

			html=requests.get(gurl,headers=headers2,proxies=proxies).content
			gurl=searchurl(etn(html),'喂食药品')

			html=requests.get(gurl,headers=headers2,proxies=proxies).content
			gurl=searchurl(etn(html),'小还丹')

			html=requests.get(gurl,headers=headers2,proxies=proxies).content
			gurl=searchurl(etn(html),'出窍')
	else:
		while 1:
			print u'你的角木蛟宝宝尚未学习出窍！快教他~'
			time.sleep(0.5)

	gurl=searchurl(etn(html),'返回游戏')

	return gurl

def relaxbb(gurl):#设置bb和bb血量
	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'宠物')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'翼火蛇')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content

	nowhp=int(re.search(r'生命:(\d\d?\d?\d?)/\d\d?\d?\d?\+?\d?\d?\d?\d? 忠诚度:',html).group(1))

	if re.search(r'\+',re.search(r'生命:\d\d?\d?\d?/\d\d?\d?\d?\+?\d?\d?\d?\d? 忠诚度:',html).group(0)):
		hp=int(re.search(r'生命:\d\d?\d?\d?/(\d\d?\d?\d?)\+?\d?\d?\d?\d? 忠诚度:',html).group(1))+int(re.search(r'生命:\d\d?\d?\d?/\d\d?\d?\d?\+?(\d?\d?\d?\d?) 忠诚度:',html).group(1))
	else:
		hp=int(re.search(r'生命:\d\d?\d?\d?/(\d\d?\d?\d?) 忠诚度:',html).group(1))

	while nowhp < (hp-200):
		gurl=searchurl(etn(html),'喂食药品')

		html=requests.get(gurl,headers=headers2,proxies=proxies).content
		gurl=searchurl(etn(html),'续命丹')

		html=requests.get(gurl,headers=headers2,proxies=proxies).content
		gurl=searchurl(etn(html),'返回上级')

		html=requests.get(gurl,headers=headers2,proxies=proxies).content

		nowhp=int(re.search(r'生命:(\d\d?\d?\d?)/\d\d?\d?\d?\+?\d?\d?\d?\d? 忠诚度:',html).group(1))

		if re.search(r'\+',re.search(r'生命:\d\d?\d?\d?/\d\d?\d?\d?\+?\d?\d?\d?\d? 忠诚度:',html).group(0)):
			hp=int(re.search(r'生命:\d\d?\d?\d?/(\d\d?\d?\d?)\+?\d?\d?\d?\d? 忠诚度:',html).group(1))+int(re.search(r'生命:\d\d?\d?\d?/\d\d?\d?\d?\+?(\d?\d?\d?\d?) 忠诚度:',html).group(1))
		else:
			hp=int(re.search(r'生命:\d\d?\d?\d?/(\d\d?\d?\d?) 忠诚度:',html).group(1))

	gurl=fs+'fengshen/'+etree.HTML(html).xpath('//body//a/@href')[-5]

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'火龙')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'设为默认法术')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'返回游戏')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'宠物')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'宠物排序')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	gurl=searchurl(etn(html),'翼火蛇')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	if re.search(r'请选择第\d只出场的宠物:',html):
		gurl=searchurl(etn(html),'角木蛟')
		html=requests.get(gurl,headers=headers2,proxies=proxies).content

	while re.search(r'请选择第\d只出场的宠物:',html):
		gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
		html=requests.get(gurl,headers=headers2,proxies=proxies).content

	gurl=searchurl(etn(html),'返回游戏')

	return gurl

def fullbag(gurl):						#设置满包处理
	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	html=etn(html)
	gurl=searchurl(html,'物品')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	if not re.search('经验内丹',html):
		if re.search('下—页',html):
			html=etn(html)
			gurl=searchurl(html,'下—页')
			html=requests.get(gurl,headers=headers2,proxies=proxies).content

			if not re.search('经验内丹',html):
				while 1:
					print u'背包已满！塞不下任务经验丹奖励了！！！'
					time.sleep(0.5)
		else:
			while 1:
				print u'背包已满！塞不下任务经验丹奖励了！！！'
				time.sleep(0.5)

	html=etn(html)
	gurl=searchurl(html,'经验内丹')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	html=etn(html)
	gurl=searchurl(html,'使用物品')

	html=requests.get(gurl,headers=headers2,proxies=proxies).content
	html=etn(html)
	gurl=fs+'fengshen/'+html.xpath('//body//a/@href')[4]	#吃丹第几位

	html=requests.get(gurl,headers=headers2,proxies=proxies).content

	if re.search('你的.*已经满级了',html):
		while 1:
			print re.search('你的.*已经满级了',html).group(0).decode('utf-8')+u'！请换吃丹位！！！'

	pet=re.search(r'\n    (.*)获得了.*点经验',html).group(1).decode('utf-8')
	neidanjingyan=re.search(r'获得了(.*)点经验',html).group(1).decode('utf-8')
	shengjijingyan=re.search(r'下次升级还要.*经验',html).group(0).decode('utf-8')
	print u'由于您的背包已满,无法领奖，'+pet+u'偷偷吃了一颗'+neidanjingyan+u'经验内丹！'+shengjijingyan+u'！'

	if re.search('升级了',html):
		print u'哈哈哈哈哈哈！'+re.search(r'下次升级.*经验。<br />(.*升级了!)',html).group(1).decode('utf-8')
		print re.search(r'(等级:\d\d?\d? → \d\d?\d?)<br>',html).group(1).decode('utf-8')
		print re.search(r'(等级:\d\d?\d? → \d\d?\d?)<br>',html).group(1).decode('utf-8')
		print re.search(r'(等级:\d\d?\d? → \d\d?\d?)<br>',html).group(1).decode('utf-8')

	html=etn(html)
	gurl=searchurl(html,'返回游戏')

	return gurl

def walk(gurl,d):
	if d == 'w':
		html=requests.get(gurl,headers=headers2,proxies=proxies).content

		if re.search(r'>北 .*↑</a>',html):
			html=etn(html)
			gurl=searchurl(html,'北 ')

			#需设置首位宠物快捷技能
			html=requests.get(gurl,headers=headers2,proxies=proxies).content
			if re.search(r'你被.*偷袭了!',html):
				gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
				gurl=zhandou(gurl)
				gurl=checkgim(gurl)

			return gurl

		else:
			print u'此处没有北行走方向'
			html=etn(html)
			gurl=searchurl(html,'刷新')
			return gurl

	elif d == 'a':
		html=requests.get(gurl,headers=headers2,proxies=proxies).content

		if re.search(r'>西 .*←</a>',html):
			html=etn(html)
			gurl=searchurl(html,'西 ')

			#需设置首位宠物快捷技能
			html=requests.get(gurl,headers=headers2,proxies=proxies).content
			if re.search(r'你被.*偷袭了!',html):
				gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
				gurl=zhandou(gurl)
				gurl=checkgim(gurl)

			return gurl

		else:
			print u'此处没有西行走方向'
			html=etn(html)
			gurl=searchurl(html,'刷新')
			return gurl

	elif d == 'd':
		html=requests.get(gurl,headers=headers2,proxies=proxies).content

		if re.search(r'>东 .*→</a>',html):
			html=etn(html)
			gurl=searchurl(html,'东 ')

			#需设置首位宠物快捷技能
			html=requests.get(gurl,headers=headers2,proxies=proxies).content
			if re.search(r'你被.*偷袭了!',html):
				gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
				gurl=zhandou(gurl)
				gurl=checkgim(gurl)

			return gurl

		else:
			print u'此处没有东行走方向'
			html=etn(html)
			gurl=searchurl(html,'刷新')
			return gurl

	elif d == 's':
		html=requests.get(gurl,headers=headers2,proxies=proxies).content

		if re.search(r'>南 .*↓</a>',html):
			html=etn(html)
			gurl=searchurl(html,'南 ')

			#需设置首位宠物快捷技能
			html=requests.get(gurl,headers=headers2,proxies=proxies).content
			if re.search(r'你被.*偷袭了!',html):
				gurl=fs+'fengshen/'+etn(html).xpath('//body//a/@href')[0]
				gurl=zhandou(gurl)
				gurl=checkgim(gurl)

			return gurl

		else:
			print u'此处没有南行走方向'
			html=etn(html)
			gurl=searchurl(html,'刷新')
			return gurl

def zhandou(zhandouurl):
	global zhandoumoney
	global experience
	global times

	zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

	if re.search('这里不能打架或现在无法挑战该NPC!',zhandouhtml):
		print u'这里不能打架或现在无法挑战该NPC!'
		zhandouhtml=etn(zhandouhtml)
		gameurl=searchurl(zhandouhtml,'返回游戏')
		return gameurl

	else:
		global tou
		tou=''
		while not re.search('返回游戏',zhandouhtml):
			if re.search(r'偷走了.*身上的(.*)。',zhandouhtml):
				tou=re.search(r'偷走了.*身上的(.*)。',zhandouhtml).group(1)

			print etn(zhandouhtml).xpath('string(//body)').decode('utf-8')
			if re.search(r'下回合法术:(.*)\(\d\d?\)',zhandouhtml):

				#遇到火生换技能
				if re.search(r'对方:.*火生.*我们该怎么办呢?',zhandouhtml):
					if not re.search(r'角木蛟.*对方:',zhandouhtml):
						if re.search(r'下回合法术:火龙\(\d\d?\)',zhandouhtml):
							zhandouhtml=etn(zhandouhtml)
							zhandouurl=searchurl(zhandouhtml,'法术')
							zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

							if re.search('凫水',zhandouhtml):
								zhandouhtml=etn(zhandouhtml)
								zhandouurl=searchurl(zhandouhtml,'凫水')
								zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

				#遇到雷属性换技能
				elif re.search(r'对方:.*雷.*我们该怎么办呢?',zhandouhtml):
					if not re.search(r'角木蛟.*对方:',zhandouhtml):
						if re.search(r'下回合法术:火龙\(\d\d?\)',zhandouhtml):
							zhandouhtml=etn(zhandouhtml)
							zhandouurl=searchurl(zhandouhtml,'法术')
							zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

							if re.search('凫水',zhandouhtml):
								zhandouhtml=etn(zhandouhtml)
								zhandouurl=searchurl(zhandouhtml,'凫水')
								zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

				#遇到土属性换BB
				elif re.search(r'对方:.*土.*我们该怎么办呢?',zhandouhtml):
					if not re.search(r'角木蛟.*对方:',zhandouhtml):
						zhandouhtml=etn(zhandouhtml)
						zhandouurl=searchurl(zhandouhtml,'交换')
						zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

						if re.search(r'角木蛟',zhandouhtml):
							zhandouhtml=etn(zhandouhtml)
							zhandouurl=searchurl(zhandouhtml,'角木蛟')
							zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

						else:
							zhandouhtml=etn(zhandouhtml)
							zhandouurl=searchurl(zhandouhtml,'返回')
							zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

					if re.search('法术',zhandouhtml):
						zhandouhtml=etn(zhandouhtml)
						zhandouurl=searchurl(zhandouhtml,'法术')
						zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

						while not re.search('出窍</a>',zhandouhtml):
							if re.search('返回上级',zhandouhtml):
								zhandouhtml=etn(zhandouhtml)
								zhandouurl=searchurl(zhandouhtml,'返回上级')
								zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

							if re.search('法术',zhandouhtml):
								zhandouhtml=etn(zhandouhtml)
								zhandouurl=searchurl(zhandouhtml,'法术')
								zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

							if re.search('战斗正在结算中,请稍后刷新!',zhandouhtml):
								zhandouhtml=etn(zhandouhtml)
								zhandouurl=searchurl(zhandouhtml,'刷新')
								zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content
								break

							if re.search('返回游戏',zhandouhtml):
								break

					if re.search('出窍',zhandouhtml):
						zhandouhtml=etn(zhandouhtml)
						zhandouurl=searchurl(zhandouhtml,'出窍')
						zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

						if re.search(r'下回合法术:出窍\(\d\d?\)',zhandouhtml):
							if int(re.search(r'下回合法术:出窍\((\d\d?)\)',zhandouhtml).group(1)) < 4:
								zhandouhtml=etn(zhandouhtml)
								zhandouurl=searchurl(zhandouhtml,'小还丹')
								zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

								zhandouhtml=etn(zhandouhtml)
								zhandouurl=searchurl(zhandouhtml,'出窍')
								zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

						print u'对抗土系妖怪努力使用出窍中！'

					if re.search('法术',zhandouhtml):
						zhandouhtml=etn(zhandouhtml)
						zhandouurl=searchurl(zhandouhtml,'法术')
						zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

					if re.search('汲命术</a>',zhandouhtml):
						zhandouhtml=etn(zhandouhtml)
						zhandouurl=searchurl(zhandouhtml,'汲命术')
						zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

					if re.search(r'己方:.*\((\d*)/\d*\).*对方:',zhandouhtml):
						if int(re.search(r'己方:.*\((\d*)/\d*\).*对方:',zhandouhtml).group(1)) < (int(re.search(r'己方:.*\(\d*/(\d*)\).*对方:',zhandouhtml).group(1))-50) :
							print u'你的宝宝需要吃血药啦！'
							if re.search('续命丹',zhandouhtml):
								zhandouhtml=etn(zhandouhtml)
								zhandouurl=searchurl(zhandouhtml,'续命丹')			#需设置战斗快捷

								zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content
							else:
								while 1:
									print u'您已经用光了所有的续命丹！！！请抓紧自己解决战斗并购买续命丹！！！'
									time.sleep(0.5)

				else:
					if not re.search(r'角木蛟.*对方:',zhandouhtml):
						if not re.search(r'下回合法术:火龙\(\d\d?\)',zhandouhtml):
							zhandouhtml=etn(zhandouhtml)
							zhandouurl=searchurl(zhandouhtml,'法术')
							zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

							if re.search('火龙',zhandouhtml):
								zhandouhtml=etn(zhandouhtml)
								zhandouurl=searchurl(zhandouhtml,'火龙')
								zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

				if re.search(r'己方:.*\((\d*)/\d*\).*对方:',zhandouhtml):
					if int(re.search(r'己方:.*\((\d*)/\d*\).*对方:',zhandouhtml).group(1)) < (int(re.search(r'己方:.*\(\d*/(\d*)\).*对方:',zhandouhtml).group(1))-120) :
						print u'你的宝宝需要吃血药啦！'
						if re.search('续命丹',zhandouhtml):
							zhandouhtml=etn(zhandouhtml)
							zhandouurl=searchurl(zhandouhtml,'续命丹')			#需设置战斗快捷

							zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content
						else:
							while 1:
								print u'您已经用光了所有的续命丹！！！请抓紧自己解决战斗并购买续命丹！！！'
								time.sleep(0.5)

				if not re.search('返回游戏',zhandouhtml):
					if not re.search(r'战斗正在结算中,请稍后刷新!',zhandouhtml):
						if int(re.search(r'下回合法术:.*\((\d\d?)\)',zhandouhtml).group(1)) < 5:
							jn=re.search(r'下回合法术:(.*)\(\d\d?\)',zhandouhtml).group(1)

							'''zhandouhtml=etn(zhandouhtml)
							zhandouurl=searchurl(zhandouhtml,'法术')			#需设置备用第二方案

							zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content'''

							if re.search('小还丹',zhandouhtml):
								zhandouhtml=etn(zhandouhtml)
								zhandouurl=searchurl(zhandouhtml,'小还丹')			#需设置战斗快捷

								zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

								if re.search('返回上级',zhandouhtml):
									zhandouhtml=etn(zhandouhtml)
									zhandouurl=searchurl(zhandouhtml,jn)
									zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

							else:
								while 1:
									print u'您已经用光了所有的小还丹！！！请抓紧自己解决战斗并购买小还丹！！！'
									time.sleep(0.5)

				if not re.search('返回游戏',zhandouhtml):
					zhandouhtml=etn(zhandouhtml)
					zhandouurl=fs+'fengshen/'+zhandouhtml.xpath('//body//a/@href')[0]

					zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

			elif re.search(r'战斗正在结算中,请稍后刷新!',zhandouhtml):
				gameurl=searchurl(etn(zhandouhtml),'刷新')
				zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

			elif re.search(r'小客栈',zhandouhtml):
				while 1:
					print u'您的宠物全部死亡，请拯救他们！！！'
					time.sleep(0.5)
			else:
				while 1:
					print u'你未设置默认法术！！！'
					time.sleep(0.5)

		print etn(zhandouhtml).xpath('string(//body)').decode('utf-8')
		if re.search('胜利',zhandouhtml):
			zhandoumoney=zhandoumoney+int(re.search(r'胜利.*你获得了(.*)枚铜板。',zhandouhtml).group(1))

			print u'胜利：'+str(times).decode('utf-8')
			print u'铜板：'+str(zhandoumoney).decode('utf-8')

			if re.search(r'铜板。<br />.*获得了(.*)点经验。',zhandouhtml):
				experience=experience+int(re.search(r'铜板。<br />.*获得了(.*)点经验。',zhandouhtml).group(1))

				if re.search('升级了',zhandouhtml):
					print u'哈哈哈哈哈哈！'+re.search(r'下次升级.*经验。<br />(.*升级了!)',zhandouhtml).group(1).decode('utf-8')
					print re.search(r'(等级:\d\d\d? → \d\d\d?)<br>',zhandouhtml).group(1).decode('utf-8')

				print u'经验：'+str(experience).decode('utf-8')
				print u'下次升级经验：'+(re.search(r'下次升级还要(.*)经验',zhandouhtml).group(1)).decode('utf-8')

			else:
				print etn(zhandouhtml).xpath('string(//body)').decode('utf-8')
				print re.search(r'铜板。<br />(你的.*已经满级)了。',zhandouhtml).group(1).decode('utf-8')+u'啦！！！'

			if re.search(r'你的【(.*)】可以进化为【.*】。',zhandouhtml):
				while 1:
					print u'你的'+re.search(r'你的【(.*)】可以进化为【.*】。',zhandouhtml).group(1).decode('utf-8')+u'似乎要进化了~快来看看'
					time.sleep(0.5)

			if re.search('杨显的山魈战死了。',zhandouhtml):
				if re.search(r'任务已完成,快去领奖吧!',zhandouhtml):
					print u'你完成了梅山七圣(40级)任务！~干的漂亮！'
				else:
					zhandouhtml=etn(zhandouhtml)
					gameurl=searchurl(zhandouhtml,'返回游戏')

					zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content
					zhandouhtml=etn(zhandouhtml)
					gameurl=searchurl(zhandouhtml,'任务')

					zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

					if re.search('常昊x1次(还差1次)',zhandouhtml):
						while 1:
							print u'你少挑战了常昊一次！快去干掉他！'
							time.sleep(0.5)

					elif re.search('朱子真x1次(还差1次)',zhandouhtml):
						while 1:
							print u'你少挑战了朱子真一次！快去干掉他！'
							time.sleep(0.5)

					elif re.search('吴龙x1次(还差1次)',zhandouhtml):
						while 1:
							print u'你少挑战了吴龙一次！快去干掉他！'
							time.sleep(0.5)

					elif re.search('袁洪x1次(还差1次)',zhandouhtml):
						while 1:
							print u'你少挑战了袁洪一次！快去干掉他！'
							time.sleep(0.5)

					elif re.search('金大升x1次(还差1次)',zhandouhtml):
						while 1:
							print u'你少挑战了金大升一次！快去干掉他！'
							time.sleep(0.5)

					elif re.search('戴礼x1次(还差1次)',zhandouhtml):
						while 1:
							print u'你少挑战了戴礼一次！快去干掉他！'
							time.sleep(0.5)

					elif re.search('杨显x1次(还差1次)',zhandouhtml):
						while 1:
							print u'你少挑战了杨显一次！快去干掉他！'
							time.sleep(0.5)

					else:
						print re.search(r'少侠,请留步!.*领奖:杨百万',etn(zhandouhtml).xpath('string(//body)').decode('utf-8'))
						while 1:
							print u'不知道谁没挑战过，来帮我看看~'
							time.sleep(0.5)

			if re.search('杨百万的诸犍战死了。',zhandouhtml):
				if re.search(r'任务已完成,快去领奖吧!',zhandouhtml):
					print u'你完成了歹毒妖道(40级)任务！~干的漂亮！'

		times=times+1

		zhandouhtml=etn(zhandouhtml)
		gameurl=searchurl(zhandouhtml,'返回游戏')

		if not tou == '':
			gameurl=checkgim(gameurl)
			zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

			gameurl=searchurl(etn(zhandouhtml),'宠物')
			zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

			if re.search('死亡',zhandouhtml):
				while 1:
					print u'翼火蛇被干掉了。。。救救小火蛇吧'
					time.sleep(0.5)

			gameurl=fs+'fengshen/'+etn(zhandouhtml).xpath('//body//a/@href')[0]
			zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

			gameurl=searchurl(etn(zhandouhtml),'装配道具')
			zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

			if not re.search(tou,zhandouhtml):
				while 1:
					print u'被偷的装备不见了！快找回来~'
					time.sleep(0.5)

			gameurl=searchurl(etn(zhandouhtml),tou)
			zhandouhtml=requests.get(zhandouurl,headers=headers2,proxies=proxies).content

			gameurl=searchurl(etn(zhandouhtml),'返回游戏')

		return gameurl

def etn(html):      #etree化字符串，同时将<br>标签转换为换行符
	html=re.sub('<br>','\n',html)
	html=re.sub('<br />','\n',html)
	html=re.sub('✔','',html)
	html=etree.HTML(html)
	return html

def searchurl(html,st):      #在html中寻找st字符串对应的url
	for a in html.xpath('//body//a'):
		if re.search(st,a.xpath('text()')[0].encode('utf-8')):
			if re.search('/',a.xpath('@href')[0].encode('utf-8')):			#首页进入下层链接
				return fs+a.xpath('@href')[0]
			else:											#其余页面就在首页进入的下层链接的该层进行跳转
				return fs+'fengshen/'+a.xpath('@href')[0]

def main():	#吃丹位、cure
	gurl=login(play2)
	job(gurl)

if __name__ == '__main__':
	main()
