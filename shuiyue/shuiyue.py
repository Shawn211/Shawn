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
play2='http://www.mfengshen.com/wapgame.php?sid=e541a56ccd9c553f0ebe21567046f317'
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
	lg0=requests.get(player,headers=headers1,proxies=proxies).content
	#print lg0.decode('utf-8')
	lg0=etn(lg0)
	#print lg0.xpath('string(//body)').decode('utf-8')      #显示页面内容，后期删除
	url0=searchurl(lg0,'封妖师OL一区-奇迹世界')
	#print url0

	lg1=requests.get(url0,headers=headers1,proxies=proxies).content
	#print lg1.decode('utf-8')
	if re.search('欢迎回家',lg1):
		print re.search(r'(欢迎回家,.*!)<br />',lg1).group(1).decode('utf-8')
		lg1=etn(lg1)
		#print lg1.xpath('string(//body)').decode('utf-8')      #显示页面内容，后期删除
		url1=searchurl(lg1,'我回来了')

		lg2=requests.get(url1,headers=headers1,proxies=proxies).content
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
	time_start=time.time()

	global run_start
	run_start=0
	global needcure

	if needcure == 1:
		gurl=cure(gurl)
	else:
		print u'血量还安全着呢~无需治疗~'

	while 1:
		html=requests.get(gurl,headers=headers1,proxies=proxies).content
		global yuxinflag
		global realsl

		if re.search('封妖观 ',html):			#设置初始封妖馆地点
			run_start=time.time()

			html=etn(html)
			gurl=searchurl(html,'刷新')

			#存钱
			gurl=deposite(gurl)

			#封妖馆 水月桥
			gurl=fwalks(gurl)

			html=requests.get(gurl,headers=headers1,proxies=proxies).content
			if re.search(r'水月桥 .*你遇到了.*影魔',html):
				html=etn(html)
				gurl=searchurl(html,'刷新')

				gurl=checkjob(gurl)			#检测是否有无任务需提交或领取

				gurl=shuiyue(gurl)

				gurl=checkgim(gurl)			#检测地上是否有gimgim的宝贝

				if yuxinflag == 0:
					#水月桥 溶洞
					gurl=swalkr(gurl)
					gurl=checkjob(gurl)			#检测是否有无任务需提交或领取

					gurl=checkgim(gurl)			#检测地上是否有gimgim的宝贝

			else:
				print u'你在最后一步踏上水月桥时，被神秘力量迷失了。'
				if re.search('刷新',html):
					html=etn(html)
					gurl=searchurl(html,'刷新')
				else:
					html=etn(html)
					gurl=searchurl(html,'返回游戏')

			print u'程序运行秒数：'+str(int(time.time()-time_start))

		elif re.search('溶洞 ',html):			#设置战斗刷怪地点
			html=etn(html)
			gurl=searchurl(html,'刷新')
			gurl=checkjob(gurl)			#检测是否有无任务需提交或领取

			gurl=checkgim(gurl)			#检测地上是否有gimgim的宝贝

			#溶洞 水月桥
			gurl=rwalks(gurl)
			gurl=checkjob(gurl)			#检测是否有无任务需提交或领取

			gurl=checkgim(gurl)			#检测地上是否有gimgim的宝贝

		elif re.search('水月桥 ',html):			#设置战斗刷怪地点
			html=etn(html)
			gurl=searchurl(html,'刷新')
			gurl=checkjob(gurl)			#检测是否有无任务需提交或领取

			gurl=checkgim(gurl)			#检测地上是否有gimgim的宝贝

			#水月桥 封妖馆
			gurl=swalkf(gurl)

			#封妖馆 树林
			gurl=fwalksl(gurl)
			gurl=checkjob(gurl)			#检测是否有无任务需提交或领取
			gurl=checkjob(gurl)			#检测是否有无任务需提交或领取

			gurl=checkgim(gurl)			#检测地上是否有gimgim的宝贝

			print u'程序运行秒数：'+str(int(time.time()-time_start))

		elif re.search('树林 ',html):			#设置战斗刷怪地点
			while not re.search(r'你遇到了.*郭巳',html):
				print u'您被迷失到了假的树林！！！'
				if re.search('东 镜花小道→',html):
					html=etn(html)
					gurl=searchurl(html,'东 镜花小道→')

					gurl=walk(gurl,'s')
					gurl=walk(gurl,'a')

					html=requests.get(gurl,headers=headers1,proxies=proxies).content
				elif re.search('西 镜花小道←',html):
					html=etn(html)
					gurl=searchurl(html,'西 镜花小道←')

					gurl=walk(gurl,'a')

					html=requests.get(gurl,headers=headers1,proxies=proxies).content
				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')
					print u'你又被迷失到了其他地方！！！'
					html=requests.get(gurl,headers=headers1,proxies=proxies).content
					break

			html=etn(html)
			gurl=searchurl(html,'刷新')
			gurl=checkjob(gurl)			#检测是否有无任务需提交或领取
			gurl=checkjob(gurl)			#检测是否有无任务需提交或领取

			gurl=checkgim(gurl)			#检测地上是否有gimgim的宝贝

			#树林 封妖馆
			gurl=slwalkf(gurl)
			if needcure == 1:
				gurl=cure(gurl)
			else:
				print u'血量还安全着呢~无需治疗~'

			if run_start == 0:
				print u'您又跑了一圈,已经跑了'+str(int(time.time()-time_start))+u'秒！奔跑正式开始计时！'

			else:
				print u'您又跑了一圈,已经跑了'+str(int(time.time()-time_start))+u'秒！本圈奔跑了'+str(int(time.time()-run_start))+u'秒！'

		elif re.search('沼泽地 ',html):
			while not re.search(r'请选择你的行走方向:.*镜花小道',html):
				if re.search('北 ',html):
					html=etn(html)
					gurl=searchurl(html,'北 ')
					html=requests.get(gurl,headers=headers1,proxies=proxies).content

				elif re.search('西 ',html):
					html=etn(html)
					gurl=searchurl(html,'西 ')
					html=requests.get(gurl,headers=headers1,proxies=proxies).content

				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')
					print u'你又被迷失到了其他地方！！！'
					html=requests.get(gurl,headers=headers1,proxies=proxies).content
					break

				print u'你被迷失到了沼泽地！正在努力尝试脱离困境！！！'

			html=etn(html)
			gurl=searchurl(html,' 镜花小道')
			html=requests.get(gurl,headers=headers1,proxies=proxies).content
			print u'你成功脱离沼泽地困境！回到了镜花小道！！！'

			while not re.search(r'西 水月桥←',html):
				if re.search('北 ',html):
					html=etn(html)
					gurl=searchurl(html,'北 ')
					html=requests.get(gurl,headers=headers1,proxies=proxies).content
				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')
					print u'你又被迷失到了其他地方！！！'
					html=requests.get(gurl,headers=headers1,proxies=proxies).content
					break

			if re.search(r'西 水月桥←',html):
				if yuxinflag == 0:
					print u'你怀着一颗御心去找若兰仙子。'
					while not re.search(r'北 溶洞↑',html):
						if re.search('北 ',html):
							html=etn(html)
							gurl=searchurl(html,'北 ')
							html=requests.get(gurl,headers=headers1,proxies=proxies).content
						else:
							html=etn(html)
							gurl=searchurl(html,'刷新')
							print u'你又被迷失到了其他地方！！！'
							html=requests.get(gurl,headers=headers1,proxies=proxies).content
							break

					if re.search(' 溶洞',html):
						html=etn(html)
						gurl=searchurl(html,' 溶洞')
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')

				elif yuxinflag == 1:
					print u'你没有御心，不能去见若兰仙子。\n你只能回到水月桥。'
					html=etn(html)
					gurl=searchurl(html,' 水月桥')

			else:
				html=etn(html)
				gurl=searchurl(html,'刷新')

		elif re.search('腐地 ',html):
			while not re.search(r'请选择你的行走方向:.*镜花小道',html):
				if re.search('北 ',html):
					html=etn(html)
					gurl=searchurl(html,'北 ')
					html=requests.get(gurl,headers=headers1,proxies=proxies).content

				elif re.search('东 ',html):
					html=etn(html)
					gurl=searchurl(html,'东 ')
					html=requests.get(gurl,headers=headers1,proxies=proxies).content

				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')
					print u'你又被迷失到了其他地方！！！'
					html=requests.get(gurl,headers=headers1,proxies=proxies).content
					break

				print u'你被迷失到了腐地！正在努力尝试脱离困境！！！'

			html=etn(html)
			gurl=searchurl(html,' 镜花小道')
			html=requests.get(gurl,headers=headers1,proxies=proxies).content
			print u'你成功脱离腐地困境！回到了镜花小道！！！'

			while not re.search(r'西 水月桥←',html):
				if re.search('北 ',html):
					html=etn(html)
					gurl=searchurl(html,'北 ')
					html=requests.get(gurl,headers=headers1,proxies=proxies).content
				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')
					print u'你又被迷失到了其他地方！！！'
					html=requests.get(gurl,headers=headers1,proxies=proxies).content
					break

			if yuxinflag == 0:
				print u'你怀着一颗御心去找若兰仙子。'
				while not re.search(r'北 溶洞↑',html):
					if re.search('北 ',html):
						html=etn(html)
						gurl=searchurl(html,'北 ')
						html=requests.get(gurl,headers=headers1,proxies=proxies).content
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')
						print u'你又被迷失到了其他地方！！！'
						html=requests.get(gurl,headers=headers1,proxies=proxies).content
						break

				if re.search(' 溶洞',html):
					html=etn(html)
					gurl=searchurl(html,' 溶洞')
				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')

			elif yuxinflag == 1:
				print u'你没有御心，不能去见若兰仙子。\n你只能回到水月桥。'
				if re.search(r'西 水月桥←',html):
					html=etn(html)
					gurl=searchurl(html,' 水月桥')
				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')

		elif re.search('瀑布 ',html):
			print u'你被迷失到了瀑布！正在努力尝试脱离困境！！！'

			html=etn(html)
			gurl=searchurl(html,' 溶洞')
			print u'你成功脱离瀑布困境！回到了溶洞！！！'

		elif re.search('黑水湖 ',html):
			print u'你被迷失到了黑水湖！正在努力尝试脱离困境！！！'

			html=etn(html)
			gurl=searchurl(html,' 清风峡')
			print u'你成功脱离黑水湖困境！回到了清风峡！！！'

		elif re.search('清风峡 ',html):
			print u'你被迷失到了清风峡！正在努力尝试脱离困境！！！'

			while not re.search('东 水月桥→',html):
				if re.search('东 ',html):
					html=etn(html)
					gurl=searchurl(html,'东 ')
					html=requests.get(gurl,headers=headers1,proxies=proxies).content
				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')
					print u'你又被迷失到了其他地方！！！'
					html=requests.get(gurl,headers=headers1,proxies=proxies).content
					break

			if re.search(r' 水月桥',html):
				html=etn(html)
				gurl=searchurl(html,' 水月桥')
				print u'你成功脱离清风峡困境！回到了水月桥！！！'
			else:
				html=etn(html)
				gurl=searchurl(html,'刷新')

		elif re.search('望海崖 ',html):
			print u'你被迷失到了望海崖！正在努力尝试脱离困境！！！'

			if not re.search('南 镜花小道↓',html):
				html=etn(html)
				gurl=searchurl(html,' 望海崖')
				html=requests.get(gurl,headers=headers1,proxies=proxies).content

			if re.search(r'南 镜花小道↓',html):
				html=etn(html)
				gurl=searchurl(html,'南 镜花小道↓')
			else:
				html=etn(html)
				gurl=searchurl(html,'刷新')
			html=requests.get(gurl,headers=headers1,proxies=proxies).content

			while not re.search('东 水月桥→',html):
				if re.search('东 ',html):
					html=etn(html)
					gurl=searchurl(html,'东 ')
					html=requests.get(gurl,headers=headers1,proxies=proxies).content
				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')
					print u'你又被迷失到了其他地方！！！'
					html=requests.get(gurl,headers=headers1,proxies=proxies).content
					break

			if re.search(r' 水月桥',html):
				html=etn(html)
				gurl=searchurl(html,' 水月桥')
				print u'你成功脱离望海崖困境！回到了水月桥！！！'
			else:
				html=etn(html)
				gurl=searchurl(html,'刷新')

		elif re.search('镜湖 ',html):
			print u'你被迷失到了镜湖！正在努力尝试脱离困境！！！'

			if not re.search(' 镜花小道',html):
				html=etn(html)
				gurl=searchurl(html,' 镜湖')
				html=requests.get(gurl,headers=headers1,proxies=proxies).content

			if re.search(r' 镜花小道',html):
				html=etn(html)
				gurl=searchurl(html,' 镜花小道')
				print u'你成功脱离镜湖困境！回到了镜花小道！接下来请回到树林。'
			else:
				html=etn(html)
				gurl=searchurl(html,'刷新')

			html=requests.get(gurl,headers=headers1,proxies=proxies).content
			while re.search('南 镜花小道↓',html):
				html=etn(html)
				gurl=searchurl(html,'南 镜花小道↓')
				html=requests.get(gurl,headers=headers1,proxies=proxies).content

			if re.search('东 镜花小道→',html):
				html=etn(html)
				gurl=searchurl(html,'东 镜花小道→')
			else:
				html=etn(html)
				gurl=searchurl(html,'刷新')
				print u'你又被迷失到了其他地方！！！'

			gurl=walk(gurl,'d')
			print u'你路过封妖馆~~~'

			gurl=fwalksl(gurl)
			print u'你成功回到了树林！！！'

		elif re.search('镜花水月 ',html):
			print u'你被迷失到了起点-镜花水月！正在努力尝试脱离困境！！！'
			html=etn(html)
			gurl=searchurl(html,'东 镜花小道→')

			gurl=walk(gurl,'d')
			gurl=walk(gurl,'d')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'a')

			print u'你成功脱离镜花水月困境！回到了树林！！！'

		elif re.search('镜花屋 ',html):
			print u'你被迷失到了镜花屋！正在努力尝试脱离困境！！！'
			html=etn(html)
			gurl=searchurl(html,'西 镜花小道←')

			gurl=walk(gurl,'a')
			gurl=walk(gurl,'a')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'a')

			print u'你成功脱离镜花屋困境！回到了树林！！！'

		elif re.search('星月坡 ',html):
			print u'你被迷失到了星月坡！正在努力尝试脱离困境！！！'

			if not re.search('星光小道',html):
				html=etn(html)
				gurl=searchurl(html,'西 ')
				html=requests.get(gurl,headers=headers1,proxies=proxies).content

			else:
				html=etn(html)
				gurl=searchurl(html,' 星光小道')

				print u'你成功脱离星光小道困境！回到了星光小道！！！'

				gurl=walk(gurl,'a')
				gurl=walk(gurl,'a')
				gurl=walk(gurl,'a')

				html=requests.get(gurl,headers=headers1,proxies=proxies).content
				if yuxinflag == 0:
					print u'你怀着一颗御心去找若兰仙子。'
					while not re.search(r'北 溶洞↑',html):
						if re.search('北 ',html):
							html=etn(html)
							gurl=searchurl(html,'北 ')
							html=requests.get(gurl,headers=headers1,proxies=proxies).content
						else:
							html=etn(html)
							gurl=searchurl(html,'刷新')
							print u'你又被迷失到了其他地方！！！'
							html=requests.get(gurl,headers=headers1,proxies=proxies).content
							break

					if re.search(' 溶洞',html):
						html=etn(html)
						gurl=searchurl(html,' 溶洞')
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')

				elif yuxinflag == 1:
					print u'你没有御心，不能去见若兰仙子。\n你只能回到水月桥。'
					if re.search(' 水月桥',html):
						html=etn(html)
						gurl=searchurl(html,' 水月桥')
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')

		elif re.search('镜花亭 ',html):
			print u'你被迷失到了镜花亭！正在努力尝试脱离困境！！！'
			html=etn(html)
			gurl=searchurl(html,'西 星光小道←')

			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'w')
			gurl=walk(gurl,'a')
			gurl=walk(gurl,'a')
			gurl=walk(gurl,'a')

			print u'你成功脱离镜花亭困境！回到了镜花小道！！！'

			html=requests.get(gurl,headers=headers1,proxies=proxies).content
			if yuxinflag == 0:
				print u'你怀着一颗御心去找若兰仙子。'
				while not re.search(r'北 溶洞↑',html):
					if re.search('北 ',html):
						html=etn(html)
						gurl=searchurl(html,'北 ')
						html=requests.get(gurl,headers=headers1,proxies=proxies).content
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')
						print u'你又被迷失到了其他地方！！！'
						html=requests.get(gurl,headers=headers1,proxies=proxies).content
						break

				if re.search(' 溶洞',html):
					html=etn(html)
					gurl=searchurl(html,' 溶洞')
				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')

			elif yuxinflag == 1:
				print u'你没有御心，不能去见若兰仙子。\n你只能回到水月桥。'
				if re.search(' 水月桥',html):
					html=etn(html)
					gurl=searchurl(html,' 水月桥')
				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')

		elif re.search('杂货铺 ',html):
			print u'你被迷失到了杂货铺！正在努力回到小树林~~~'
			html=etn(html)
			gurl=searchurl(html,'南 封妖观↓')

			gurl=walk(gurl,'s')
			gurl=walk(gurl,'s')
			gurl=walk(gurl,'s')
			gurl=walk(gurl,'a')

			print u'你成功脱离杂货铺困境！回到了树林~~~'

		elif re.search('镜花小道 ',html):
			print u'你被迷失到了镜花小道！正在努力尝试脱离困境！！！'

			if re.search('西 镜花水月←',html):
				html=etn(html)
				gurl=searchurl(html,'西 镜花水月←')
				print u'你成功脱离镜花小道困境！回到了镜花水月！！！'

			elif re.search('东 镜花屋→',html):
				html=etn(html)
				gurl=searchurl(html,'东 镜花屋→')
				print u'你成功脱离镜花小道困境！回到了镜花屋！！！'

			elif re.search('西 树林←',html):
				html=etn(html)
				gurl=searchurl(html,'西 树林←')
				print u'你成功脱离镜花小道困境！回到了树林！！！'

			elif re.search('北 封妖观↑',html):
				html=etn(html)
				gurl=searchurl(html,'南 镜花小道↓')

				gurl=walk(gurl,'s')
				gurl=walk(gurl,'a')
				print u'你成功脱离镜花小道困境！回到了树林！！！'

			elif re.search('东 封妖观→',html):
				html=etn(html)
				gurl=searchurl(html,'东 封妖观→')
				print u'你路过封妖馆~~~'

				gurl=fwalksl(gurl)
				print u'你成功脱离镜花小道困境！回到了树林！！！'

			elif re.search('西 封妖观←',html):
				html=etn(html)
				gurl=searchurl(html,'西 封妖观←')
				print u'你路过封妖馆~~~'

				gurl=fwalksl(gurl)
				print u'你成功脱离镜花小道困境！回到了树林！！！'

			elif re.search('西 镜湖←',html):
				html=etn(html)
				gurl=searchurl(html,'南 镜花小道↓')

				html=requests.get(gurl,headers=headers1,proxies=proxies).content
				while re.search('南 镜花小道↓',html):
					html=etn(html)
					gurl=searchurl(html,'南 镜花小道↓')
					html=requests.get(gurl,headers=headers1,proxies=proxies).content

				html=etn(html)
				gurl=searchurl(html,'刷新')

				gurl=walk(gurl,'d')
				gurl=walk(gurl,'d')
				print u'你路过封妖馆~~~'

				gurl=fwalksl(gurl)
				print u'你成功脱离镜花小道困境！回到了树林！！！'

			elif re.search(r'北 望海崖↑.*西 清风峡←',html):
				html=etn(html)
				gurl=searchurl(html,'东 镜花小道→')

				gurl=walk(gurl,'d')
				gurl=walk(gurl,'d')
				if yuxinflag == 0:
					print u'你怀着一颗御心去找若兰仙子。\n你路过水月桥~~~'
					gurl=walk(gurl,'d')

					html=requests.get(gurl,headers=headers1,proxies=proxies).content
					while not re.search(r'北 溶洞↑',html):
						if re.search('北 ',html):
							html=etn(html)
							gurl=searchurl(html,'北 ')
							html=requests.get(gurl,headers=headers1,proxies=proxies).content
						else:
							html=etn(html)
							gurl=searchurl(html,'刷新')
							print u'你又被迷失到了其他地方！！！'
							html=requests.get(gurl,headers=headers1,proxies=proxies).content
							break

					if re.search(' 溶洞',html):
						html=etn(html)
						gurl=searchurl(html,' 溶洞')
						print u'你成功脱离镜花小道困境！回到了溶洞！！！'
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')

				elif yuxinflag == 1:
					print u'你没有御心，不能去见若兰仙子。\n你只能回到水月桥。\n你成功脱离镜花小道困境！回到了水月桥！！！'

			elif re.search('东 水月桥→',html):
				html=etn(html)
				gurl=searchurl(html,'东 水月桥→')

				if yuxinflag == 0:
					print u'你怀着一颗御心去找若兰仙子。\n你路过水月桥~~~'
					gurl=walk(gurl,'d')

					html=requests.get(gurl,headers=headers1,proxies=proxies).content
					while not re.search(r'北 溶洞↑',html):
						if re.search('北 ',html):
							html=etn(html)
							gurl=searchurl(html,'北 ')
							html=requests.get(gurl,headers=headers1,proxies=proxies).content
						else:
							html=etn(html)
							gurl=searchurl(html,'刷新')
							print u'你又被迷失到了其他地方！！！'
							html=requests.get(gurl,headers=headers1,proxies=proxies).content
							break

					if re.search(' 溶洞',html):
						html=etn(html)
						gurl=searchurl(html,' 溶洞')
						print u'你成功脱离镜花小道困境！回到了溶洞！！！'
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')

				elif yuxinflag == 1:
					print u'你没有御心，不能去见若兰仙子。\n你只能回到水月桥。\n你成功脱离镜花小道困境！回到了水月桥！！！'

			elif re.search('西 水月桥←',html):
				if yuxinflag == 0:
					print u'你怀着一颗御心去找若兰仙子。'

					html=requests.get(gurl,headers=headers1,proxies=proxies).content
					while not re.search(r'北 溶洞↑',html):
						if re.search('北 ',html):
							html=etn(html)
							gurl=searchurl(html,'北 ')
							html=requests.get(gurl,headers=headers1,proxies=proxies).content
						else:
							html=etn(html)
							gurl=searchurl(html,'刷新')
							print u'你又被迷失到了其他地方！！！'
							html=requests.get(gurl,headers=headers1,proxies=proxies).content
							break

					if re.search(' 溶洞',html):
						html=etn(html)
						gurl=searchurl(html,' 溶洞')
						print u'你成功脱离镜花小道困境！回到了溶洞！！！'
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')

				elif yuxinflag == 1:
					if re.search('西 水月桥←',html):
						html=etn(html)
						gurl=searchurl(html,'西 水月桥←')
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')
					print u'你没有御心，不能去见若兰仙子。\n你只能回到水月桥。\n你成功脱离镜花小道困境！回到了水月桥！！！'

			elif re.search('北 溶洞↑',html):
				html=etn(html)
				gurl=searchurl(html,'北 溶洞↑')
				print u'你成功脱离镜花小道困境！回到了溶洞！！！'

			elif re.search(r'西 腐地←.*东 沼泽地→.*南 腐地↓',html):
				while not re.search(r'西 水月桥←',html):
					if re.search('北 镜花小道↑',html):
						html=etn(html)
						gurl=searchurl(html,'北 镜花小道↑')
						html=requests.get(gurl,headers=headers1,proxies=proxies).content
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')
						print u'你又被迷失到了其他地方！！！'
						html=requests.get(gurl,headers=headers1,proxies=proxies).content
						break

				if re.search(r'西 水月桥←',html):
					if yuxinflag == 0:
						print u'你怀着一颗御心去找若兰仙子。'
						while not re.search(r'北 溶洞↑',html):
							if re.search('北 ',html):
								html=etn(html)
								gurl=searchurl(html,'北 ')
							else:
								html=etn(html)
								gurl=searchurl(html,'刷新')
							html=requests.get(gurl,headers=headers1,proxies=proxies).content

						if re.search(' 溶洞',html):
							html=etn(html)
							gurl=searchurl(html,' 溶洞')
							print u'你成功脱离镜花小道困境！回到了溶洞！！！'
						else:
							html=etn(html)
							gurl=searchurl(html,'刷新')

					elif yuxinflag == 1:
						print u'你没有御心，不能去见若兰仙子。\n你只能回到水月桥。'
						if re.search('西 水月桥←',html):
							html=etn(html)
							gurl=searchurl(html,'西 水月桥←')
							print u'你成功脱离镜花小道困境！回到了水月桥！！！'
						else:
							html=etn(html)
							gurl=searchurl(html,'刷新')
				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')

			elif re.search('东 星光小道→',html):
				while not re.search(r'西 水月桥←',html):
					if re.search('西 镜花小道←',html):
						html=etn(html)
						gurl=searchurl(html,'西 镜花小道←')
						html=requests.get(gurl,headers=headers1,proxies=proxies).content
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')
						print u'你又被迷失到了其他地方！！！'
						html=requests.get(gurl,headers=headers1,proxies=proxies).content
						break

				if yuxinflag == 0:
					print u'你怀着一颗御心去找若兰仙子。'
					while not re.search(r'北 溶洞↑',html):
						if re.search('北 ',html):
							html=etn(html)
							gurl=searchurl(html,'北 ')
							html=requests.get(gurl,headers=headers1,proxies=proxies).content
						else:
							html=etn(html)
							gurl=searchurl(html,'刷新')
							print u'你又被迷失到了其他地方！！！'
							html=requests.get(gurl,headers=headers1,proxies=proxies).content
							break

					if re.search(' 溶洞',html):
						html=etn(html)
						gurl=searchurl(html,' 溶洞')
						print u'你成功脱离镜花小道困境！回到了溶洞！！！'
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')

				elif yuxinflag == 1:
					print u'你没有御心，不能去见若兰仙子。\n你只能回到水月桥。'
					if re.search('西 水月桥←',html):
						html=etn(html)
						gurl=searchurl(html,'西 水月桥←')
						print u'你成功脱离镜花小道困境！回到了水月桥！！！'
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')

			else:
				if re.search('北 镜花小道↑',html):
					print u'这里一点路标都没有！我悄悄的向北走去瞧瞧~'
					html=etn(html)
					gurl=searchurl(html,'北 镜花小道↑')

				elif re.search('西 镜花小道←',html):
					print u'这里一点路标都没有！向北没有路，我悄悄的向西走去瞧瞧~'
					html=etn(html)
					gurl=searchurl(html,'西 镜花小道←')

				elif re.search('东 镜花小道→',html):
					print u'这里一点路标都没有！向北、西都没有路，我悄悄的向东走去瞧瞧~'
					html=etn(html)
					gurl=searchurl(html,'东 镜花小道→')
					gurl=walk(gurl,'d')

				elif re.search('南 镜花小道↓',html):
					print u'这里一点路标都没有！向北、西、东都没有路，我悄悄的向南走去瞧瞧~'
					html=etn(html)
					gurl=searchurl(html,'南 镜花小道↓')

				else:
					while 1:
						print u'你到达了一个我完全不知道的镜花小道！请自己回到熟悉的地方！！！'
						time.sleep(0.5)

		elif re.search('星光小道 ',html):
			print u'你被迷失到了星光小道！正在努力尝试脱离困境！！！'

			while not re.search('西 镜花小道←',html):
				if re.search('北 星光小道↑',html):
					html=etn(html)
					gurl=searchurl(html,'北 星光小道↑')
					html=requests.get(gurl,headers=headers1,proxies=proxies).content
				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')
					print u'你又被迷失到了其他地方！！！'
					html=requests.get(gurl,headers=headers1,proxies=proxies).content
					break

			if re.search('西 镜花小道←',html):
				html=etn(html)
				gurl=searchurl(html,'西 镜花小道←')
			else:
				html=etn(html)
				gurl=searchurl(html,'刷新')

			gurl=walk(gurl,'a')
			gurl=walk(gurl,'a')

			html=requests.get(gurl,headers=headers1,proxies=proxies).content
			if yuxinflag == 0:
				print u'你怀着一颗御心去找若兰仙子。'
				while not re.search(r'北 溶洞↑',html):
					if re.search('北 ',html):
						html=etn(html)
						gurl=searchurl(html,'北 ')
						html=requests.get(gurl,headers=headers1,proxies=proxies).content
					else:
						html=etn(html)
						gurl=searchurl(html,'刷新')
						print u'你又被迷失到了其他地方！！！'
						html=requests.get(gurl,headers=headers1,proxies=proxies).content
						break

				if re.search(' 溶洞',html):
					html=etn(html)
					gurl=searchurl(html,' 溶洞')
					print u'你成功脱离星光小道困境！回到了溶洞！！！'
				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')

			elif yuxinflag == 1:
				print u'你没有御心，不能去见若兰仙子。\n你只能回到水月桥。'
				if re.search('西 水月桥←',html):
					html=etn(html)
					gurl=searchurl(html,'西 水月桥←')
					print u'你成功脱离星光小道困境！回到了水月桥！！！'
				else:
					html=etn(html)
					gurl=searchurl(html,'刷新')

		else:
			while 1:
				print u'你不存在于镜花水月，也不存在于小客栈。你不存在于我给你创造的世界。'
				time.sleep(0.5)

def fwalks(gurl):
	#封妖馆 水月桥
	gurl=walk(gurl,'a')
	gurl=walk(gurl,'a')
	gurl=walk(gurl,'w')
	gurl=walk(gurl,'w')
	gurl=walk(gurl,'w')
	gurl=walk(gurl,'w')
	gurl=walk(gurl,'d')
	gurl=walk(gurl,'d')
	gurl=walk(gurl,'w')
	gurl=walk(gurl,'w')
	gurl=walk(gurl,'w')
	gurl=walk(gurl,'d')
	gurl=walk(gurl,'d')
	gurl=walk(gurl,'d')
	print '---------------------'
	print u'水月桥'
	print u'碧水无尘,明月映照下的石桥,宛如月宫仙境。'
	print u'你遇到了影魔'
	print u'烟云起处荡乾坤,黑雾阴霾大地昏,隐于黑暗终于光明。'
	print u'影魔对你说:我生于黑暗隐于黑暗……'
	print '---------------------'
	return gurl

def swalkr(gurl):
	#水月桥 溶洞
	gurl=walk(gurl,'d')
	gurl=walk(gurl,'w')
	gurl=walk(gurl,'w')
	gurl=walk(gurl,'w')
	print '---------------------'
	print u'溶洞'
	print u'石洞如同一条蜿蜒盘旋的巨龙,洞内千姿百态、奇幻迷离,摄人心魄。'
	print u'你遇到了若兰仙子'
	print u'一身蓝色的翠烟衫,散花水雾绿草百褶裙,身披淡蓝色的翠水薄烟纱,肩若削成腰若约素,肌若凝脂气若幽兰。'
	print u'若兰仙子对你说:我很想再和小时候一样去星光小路看看漫天的繁星。'
	print '---------------------'
	return gurl

def rwalks(gurl):
	#溶洞 水月桥
	gurl=walk(gurl,'s')
	gurl=walk(gurl,'s')
	gurl=walk(gurl,'s')
	gurl=walk(gurl,'a')
	print '---------------------'
	print u'水月桥'
	print u'碧水无尘,明月映照下的石桥,宛如月宫仙境。'
	print u'你遇到了影魔'
	print u'烟云起处荡乾坤,黑雾阴霾大地昏,隐于黑暗终于光明。'
	print u'影魔对你说:我生于黑暗隐于黑暗……'
	print '---------------------'
	return gurl

def swalkf(gurl):
	#水月桥 封妖馆
	gurl=walk(gurl,'a')
	gurl=walk(gurl,'a')
	gurl=walk(gurl,'a')
	gurl=walk(gurl,'s')
	gurl=walk(gurl,'s')
	gurl=walk(gurl,'s')
	gurl=walk(gurl,'a')
	gurl=walk(gurl,'a')
	gurl=walk(gurl,'s')
	gurl=walk(gurl,'s')
	gurl=walk(gurl,'s')
	gurl=walk(gurl,'s')
	gurl=walk(gurl,'d')
	gurl=walk(gurl,'d')
	print '---------------------'
	print u'封妖观'
	print u'镜花虚境,终究离碎无欢。'
	print u'你遇到了贺有光'
	print u'仪容清秀貌堂堂,两耳垂肩目有光。头戴三山飞凤帽,身穿黝黑玄冥甲。'
	print u'贺有光对你说:镜花虚境,终究离碎无欢。梦一场、梦一场……'
	print '---------------------'
	return gurl

def fwalksl(gurl):
	#封妖馆 树林
	gurl=walk(gurl,'s')
	gurl=walk(gurl,'s')
	gurl=walk(gurl,'s')
	gurl=walk(gurl,'a')
	print '---------------------'
	print u'树林'
	print u'诡异的树林,雾气弥漫看不真切,唯有沙沙声萦绕耳畔。'
	print u'你遇到了郭巳'
	print u'阳光下一个身量不高,面色黑红的少年。'
	print u'郭巳对你说:读万卷书行万里路！'
	print '---------------------'
	return gurl

def slwalkf(gurl):
	#树林 封妖馆
	gurl=walk(gurl,'d')
	gurl=walk(gurl,'w')
	gurl=walk(gurl,'w')
	gurl=walk(gurl,'w')
	print '---------------------'
	print u'封妖观'
	print u'镜花虚境,终究离碎无欢。'
	print u'你遇到了贺有光'
	print u'仪容清秀貌堂堂,两耳垂肩目有光。头戴三山飞凤帽,身穿黝黑玄冥甲。'
	print u'贺有光对你说:镜花虚境,终究离碎无欢。梦一场、梦一场……'
	print '---------------------'
	return gurl

def checkjob(gurl):
	html=requests.get(gurl,headers=headers1,proxies=proxies).content
	if re.search('有没有兴趣',html):
		gurl=fs+'fengshen/'+re.search(r'对你说:.*<a href="(.*)" title="查看">查看</a><br />请选择你的行走方向:',html).group(1)

		html=requests.get(gurl,headers=headers1,proxies=proxies).content
		html=etn(html)

		gurl=searchurl(html,'接受任务')

		html=requests.get(gurl,headers=headers1,proxies=proxies).content
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

			html=requests.get(gurl,headers=headers1,proxies=proxies).content

			if re.search('背包已满,无法领奖!',html):
				print u'背包已满,无法领奖!'
				html=etn(html)
				gurl=searchurl(html,'返回游戏')

				gurl=fullbag(gurl)

				html=requests.get(gurl,headers=headers1,proxies=proxies).content
			else:
				while not re.search('返回游戏',html):
					html=etn(html)
					gurl=fs+'fengshen/'+html.xpath('//body//a/@href')[0]
					html=requests.get(gurl,html).content

				global yuxinflag
				global yuxin
				if re.search(r'<br />你获得了1颗御心。<br />',html):
					yuxin=yuxin+1
					yuxinflag=0
					print u'你获得一颗御心，你得去溶洞将御心交给若兰仙子。'

				else:
					yuxinflag=1
					print u'你未获得一颗御心，不能去见若兰仙子。'

				global jobmoney
				if re.search(r'。<br />你获得了.*枚铜板。<br />',html):
					jobmoney=jobmoney+int(re.search(r'。<br />你获得了(\d*)枚铜板。<br />',html).group(1))
					print re.search(r'。<br />(你获得了\d*枚铜板)。<br />',html).group(1).decode('utf-8')+u'！'
					print u'\n你获得任务赏金共'+str(jobmoney)+u'枚铜板。'
					print u'你获得任务赏金共'+str(jobmoney)+u'枚铜板。'
					print u'你获得任务赏金共'+str(jobmoney)+u'枚铜板。\n'

				if re.search('副本金钱已达到每日限额',html):
					print u'副本金钱已达到每日限额！！！'
					print u'副本金钱已达到每日限额！！！'
					print u'副本金钱已达到每日限额！！！'
					print u'\n你获得任务赏金共'+str(jobmoney)+u'枚铜板。\n'

				html=etn(html)
				gurl=searchurl(html,'返回游戏')
				html=requests.get(gurl,headers=headers1,proxies=proxies).content

		html=etn(html)
		gurl=searchurl(html,'刷新')

		return gurl

	else:
		html=etn(html)
		return searchurl(html,'刷新')

def checkgim(gurl):
	html=requests.get(gurl,headers=headers1,proxies=proxies).content
	while re.search(r'地上有',html):
		gurl=fs+'fengshen/'+re.search(r'地上有<a href="(.*)" title=".*">.*</a><br />请选择你的行走方向:',html).group(1)

		html=requests.get(gurl,headers=headers1,proxies=proxies).content
		while not re.search('刷新',html):
			html=etn(html)

			gurl=fs+'fengshen/'+html.xpath('//body//a/@href')[0]
			html=requests.get(gurl,headers=headers1,proxies=proxies).content

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

		if re.search('抱歉,您的背包已满。',html):
			print u'背包已满，捡不起gimgim宝贝！'

			html=etn(html)
			gurl=searchurl(html,'刷新')

			gurl=fullbag(gurl)

			html=requests.get(gurl,headers=headers1,proxies=proxies).content

	html=etn(html)
	gurl=searchurl(html,'刷新')

	return gurl

def fullbag(gurl):						#设置满包处理
	html=requests.get(gurl,headers=headers1,proxies=proxies).content
	html=etn(html)
	gurl=searchurl(html,'物品')

	html=requests.get(gurl,headers=headers1,proxies=proxies).content
	if not re.search('经验内丹',html):
		if re.search('下—页',html):
			html=etn(html)
			gurl=searchurl(html,'下—页')
			html=requests.get(gurl,headers=headers1,proxies=proxies).content

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

	html=requests.get(gurl,headers=headers1,proxies=proxies).content
	html=etn(html)
	gurl=searchurl(html,'使用物品')

	html=requests.get(gurl,headers=headers1,proxies=proxies).content
	html=etn(html)
	gurl=fs+'fengshen/'+html.xpath('//body//a/@href')[1]	#吃丹第几位

	html=requests.get(gurl,headers=headers1,proxies=proxies).content

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

def cure(gurl):
	global curetimes
	global needcure

	html=requests.get(gurl,headers=headers1,proxies=proxies).content
	if re.search('治疗宠物',html):
		html=etn(html)
		gurl=searchurl(html,'治疗宠物')

		html=requests.get(gurl,headers=headers1,proxies=proxies).content
		if re.search('本次治疗需要1000枚铜板,你身上没有足够的铜板了。',html):
			while 1:
				print u'我们已被限制治疗！可能需要钱，也可能是死了。。。请您拯救我们！！！'
				time.sleep(0.5)

		while re.search('等待',html):
			html=etn(html)
			gurl=searchurl(html,'等待')
			html=requests.get(gurl,headers=headers1,proxies=proxies).content
			if re.search('本次治疗需要1000枚铜板,你身上没有足够的铜板了。',html):
				while 1:
					print u'我们已被限制治疗！可能需要钱，也可能是死了。。。请您拯救我们！！！'
					time.sleep(0.5)

		html=etn(html)
		gurl=searchurl(html,'返回游戏')

		needcure=0
		curetimes=curetimes+1
		print u'封妖馆治疗次数：'+str(curetimes)
		return gurl
	else:
		print u'您当前不在封妖馆！'
		html=etn(html)
		gurl=searchurl(html,'刷新')
		return gurl

def walk(gurl,d):
	if d == 'w':
		html=requests.get(gurl,headers=headers1,proxies=proxies).content

		if re.search(r'>北 .*↑</a>',html):
			html=etn(html)
			gurl=searchurl(html,'北 ')
			return gurl

		elif re.search('你确定要退出副本吗?',html):
			print u'你跑来了终点-镜花亭！！！'
			html=etn(html)
			gurl=searchurl(html,'返回游戏')
			return gurl

		else:
			print u'此处没有北行走方向'
			html=etn(html)
			gurl=searchurl(html,'刷新')
			return gurl

	elif d == 'a':
		html=requests.get(gurl,headers=headers1,proxies=proxies).content

		if re.search(r'>西 .*←</a>',html):
			html=etn(html)
			gurl=searchurl(html,'西 ')
			return gurl

		elif re.search('你确定要退出副本吗?',html):
			print u'你跑来了终点-镜花亭！！！'
			html=etn(html)
			gurl=searchurl(html,'返回游戏')
			return gurl

		else:
			print u'此处没有西行走方向'
			html=etn(html)
			gurl=searchurl(html,'刷新')
			return gurl

	elif d == 'd':
		html=requests.get(gurl,headers=headers1,proxies=proxies).content

		if re.search(r'>东 .*→</a>',html):
			html=etn(html)
			gurl=searchurl(html,'东 ')
			return gurl

		elif re.search('你确定要退出副本吗?',html):
			print u'你跑来了终点-镜花亭！！！'
			html=etn(html)
			gurl=searchurl(html,'返回游戏')
			return gurl

		else:
			print u'此处没有东行走方向'
			html=etn(html)
			gurl=searchurl(html,'刷新')
			return gurl

	elif d == 's':
		html=requests.get(gurl,headers=headers1,proxies=proxies).content

		if re.search(r'>南 .*↓</a>',html):
			html=etn(html)
			gurl=searchurl(html,'南 ')
			return gurl

		elif re.search('你确定要退出副本吗?',html):
			print u'你跑来了终点-镜花亭！！！'
			html=etn(html)
			gurl=searchurl(html,'返回游戏')
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
	global needcure

	zhandouhtml=requests.get(zhandouurl,headers=headers1,proxies=proxies).content

	if re.search('这里不能打架或现在无法挑战该NPC!',zhandouhtml):
		print u'您没有资格挑战该NPC！请立刻想办法K他 ！！！'
		print u'你站在此处想了一会办法~'
		zhandouhtml=etn(zhandouhtml)
		gameurl=searchurl(zhandouhtml,'返回游戏')
		return gameurl

	else:
		while not re.search('返回游戏',zhandouhtml):
			if re.search(r'下回合法术:(.*)\(\d\d?\)',zhandouhtml):
				jn=re.search(r'下回合法术:(.*)\(\d\d?\)',zhandouhtml).group(1)
				if re.search(r'己方:.*\((\d*)/\d*\).*对方:',zhandouhtml):
					if int(re.search(r'己方:.*\((\d*)/\d*\).*对方:',zhandouhtml).group(1))<120:
						print u'你的宝宝需要治疗咯~'
						needcure=1
						if int(re.search(r'己方:.*\((\d*)/\d*\).*对方:',zhandouhtml).group(1))<80:
							print u'你的宝宝需要吃血药啦！'
							if re.search('续命丹',zhandouhtml):
								zhandouhtml=etn(zhandouhtml)
								zhandouurl=searchurl(zhandouhtml,'续命丹')			#需设置战斗快捷

								zhandouhtml=requests.get(zhandouurl,headers=headers1,proxies=proxies).content
							else:
								while 1:
									print u'您已经用光了所有的续命丹！！！请抓紧自己解决战斗并购买续命丹！！！'
									time.sleep(0.5)

				if int(re.search(r'下回合法术:.*\((\d\d?)\)',zhandouhtml).group(1)) == 0:
					'''zhandouhtml=etn(zhandouhtml)
					zhandouurl=searchurl(zhandouhtml,'法术')			#需设置备用第二方案

					zhandouhtml=requests.get(zhandouurl,headers=headers1,proxies=proxies).content'''

					if re.search('小还丹',zhandouhtml):
						zhandouhtml=etn(zhandouhtml)
						zhandouurl=searchurl(zhandouhtml,'小还丹')			#需设置战斗快捷

						zhandouhtml=requests.get(zhandouurl,headers=headers1,proxies=proxies).content
					else:
						while 1:
							print u'您已经用光了所有的小还丹！！！请抓紧自己解决战斗并购买小还丹！！！'
							time.sleep(0.5)

				zhandouhtml=etn(zhandouhtml)
				zhandouurl=searchurl(zhandouhtml,jn)      #需设置默认法术

				zhandouhtml=requests.get(zhandouurl,headers=headers1,proxies=proxies).content

			elif re.search(r'小客栈',zhandouhtml):
				while 1:
					print u'您的宠物全部死亡，请拯救他们！！！'
					time.sleep(0.5)
			else:
				while 1:
					print u'你未设置默认法术！！！'
					time.sleep(0.5)

		zhandoumoney=zhandoumoney+int(re.search(r'你获得了胜利。<br>你获得了(.*)枚铜板。',zhandouhtml).group(1))

		print u'胜利：'+str(times).decode('utf-8')
		print u'铜板：'+str(zhandoumoney).decode('utf-8')

		if not re.search(r'铜板。<br />你的.*已经满级了。',zhandouhtml):
			experience=experience+int(re.search(r'铜板。<br />.*获得了(.*)点经验。',zhandouhtml).group(1))

			if re.search('升级了',zhandouhtml):
				print u'哈哈哈哈哈哈！'+re.search(r'下次升级.*经验。<br />(.*升级了!)',zhandouhtml).group(1).decode('utf-8')
				print re.search(r'(等级:\d\d\d? → \d\d\d?)<br>',zhandouhtml).group(1).decode('utf-8')

			print u'经验：'+str(experience).decode('utf-8')
			print u'下次升级经验：'+(re.search(r'下次升级还要(.*)经验',zhandouhtml).group(1)).decode('utf-8')

		else:
			print re.search(r'铜板。<br />(你的.*已经满级)了。',zhandouhtml).group(1).decode('utf-8')+u'啦！！！'

		if re.search(r'你的【(.*)】可以进化为【.*】。',zhandouhtml):
			while 1:
				print u'你的'+re.search(r'你的【(.*)】可以进化为【.*】。',zhandouhtml).group(1).decode('utf-8')+u'似乎要进化了~快来看看'
				time.sleep(0.5)

		times=times+1

		zhandouhtml=etn(zhandouhtml)
		gameurl=searchurl(zhandouhtml,'返回游戏')

		return gameurl

def shuiyue(gurl):
	html=requests.get(gurl,headers=headers1,proxies=proxies).content

	url=re.search(r'你遇到了<a href="(.*)" title=".*</a><br />这里有',html).group(1)
	gurl=fs+'fengshen/'+url

	#html=requests.get(gurl,headers=headers1,proxies=proxies).content
	#html=etn(html)
	#gurl=fs+'fengshen/'+html.xpath('//body//a/@href')[0]

	html=requests.get(gurl,headers=headers1,proxies=proxies).content
	html=etn(html)
	gurl=searchurl(html,'挑战')

	gurl=zhandou(gurl)

	return gurl

def deposite(gurl):
	html=requests.get(gurl,headers=headers1,proxies=proxies).content
	html=etn(html)
	gurl=searchurl(html,'北 杂货铺↑')

	html=requests.get(gurl,headers=headers1,proxies=proxies).content
	if re.search('杂货铺 ',html):
		print '---------------------'
		print u'杂货铺'
		print u'镜花虚境,终究离碎无欢。'
		print u'你遇到了李婶'
		print u'一个勤劳的女人，上下忙碌着。'
		print u'李婶对你说:一天天的日子过去了，忙碌才能充实。'
		print '---------------------'
		html=etn(html)
		gurl=searchurl(html,'存钱')

		html=requests.get(gurl,headers=headers1,proxies=proxies).content

		gurl=fs+'fengshen/'+re.search(r'<form action="(.*)" method="post">',html).group(1)

		money=re.search(r'你身上有(\d*)枚铜板,想要存多少枚铜板?',html).group(1)
		data={'money':money,'存入':'存入铜板'}

		html=requests.post(gurl,data,headers=headers1,proxies=proxies).content

		bill=html
		if re.search(r'你存入了\d*枚铜板。.*杂货铺有\d*枚铜板。.*身上有\d*枚铜板。',bill):
			bill=re.search(r'你存入了\d*枚铜板。.*杂货铺有\d*枚铜板。.*身上有\d*枚铜板。',bill).group(0).decode('utf-8')
			bill=re.sub('<br>','\n',bill)
			print bill

		else:
			print u'走开,没钱别在这捣乱!'

		html=etn(html)
		gurl=searchurl(html,'返回游戏')

		html=requests.get(gurl,headers=headers1,proxies=proxies).content
		html=etn(html)
		gurl=searchurl(html,'南 封妖观↓')

		print '---------------------'
		print u'封妖观'
		print u'镜花虚境,终究离碎无欢。'
		print u'你遇到了贺有光'
		print u'仪容清秀貌堂堂,两耳垂肩目有光。头戴三山飞凤帽,身穿黝黑玄冥甲。'
		print u'贺有光对你说:镜花虚境,终究离碎无欢。梦一场、梦一场……'
		print '---------------------'

		return gurl

	else:
		html=etn(html)
		gurl=searchurl(html,'刷新')
		return gurl

def etn(html):      #etree化字符串，同时将<br>标签转换为换行符
	html=re.sub('<br>','\n',html)
	html=re.sub('<br />','\n',html)
	html=etree.HTML(html)
	return html

def searchurl(html,st):      #在html中寻找st字符串对应的url
	for a in html.xpath('//body//a'):
		if re.search(st,a.xpath('text()')[0].encode('utf-8')):
			if re.search('/',a.xpath('@href')[0].encode('utf-8')):			#首页进入下层链接
				return fs+a.xpath('@href')[0]
			else:											#其余页面就在首页进入的下层链接的该层进行跳转
				return fs+'fengshen/'+a.xpath('@href')[0]

def main():	#吃丹位、needcure、cure、战斗needcure置1血量
	gurl=login(play1)
	job(gurl)

if __name__ == '__main__':
	main()
