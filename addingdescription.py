#coding:utf-8

#descriptionにコメントを追記するツール
#さらにノードの色を変えたりエッジの色や太さもクエリのtsvによって変えられる

#ターミナルでの使い方
#$ python addingdescription.py originFile.graphml commentedFile.graphml node.dat edge.dat
#凡例はsysのコメント参照

import sys
originFile = str(sys.argv[1]) #コメントを追加したり色を更新したいネットワーク図のgraphml
commentedFile = str(sys.argv[2]) #コメントを追加した後のネットワーク図のgraphml
nodeFile = str(sys.argv[3]) #更新用ノードデータのtsv
edgeFile = str(sys.argv[4]) #更新用エッジデータのtsv
#更新用データはデータベースを更新してtsv保存し、makeNodeEdgeすると簡単に作られる

#graphmlとxmlの拡張子を行き来するツール
import gmltoxml
#パースのためにxmlにする
gmltoxml.T(originFile,'origindata_c.xml')

#パースして準備
from xml.dom import minidom
xdoc0 = minidom.parse('origindata_c.xml')
Nodes = xdoc0.getElementsByTagName('node')
Edges = xdoc0.getElementsByTagName('edge')
Nnode = len(Nodes)
Nedge = len(Edges) 
lsNodeX = []
lsNodeY = []
'''
lsNodeX = [x0,x1,...]
lsNodeY = [y0,y1,...]
#xi,yi:x,y of Nodes[i]
'''
MatNodes = [] 
'''
MatNodes == [
[nhoge,Nodelabel,nodeID],
[n0,spam,43],
[node id=,text,taxID or '-'],
...
]
'''
MatEdges = []
'''
MatEdges = [
[ehoge,source,target],
...
]
'''
#updownString:{'-',-1,0,1} -> str
#descriptionに書き込む増減
def updownString(uptribool) : #{
	if str(uptribool) == '-' : #{
		uptribool = 'unknown'
	#}
	else : #{
		if int(uptribool) == 1 : #{
			uptribool = 'increase'
		#}
		elif int(uptribool) == -1 : #{
			uptribool = 'decrease'
		#}
		elif int(uptribool) == 0 : #{
			uptribool = 'neutral'
		#}
		else : #{
			uptribool = 'undef'
		#}
	#}
	return uptribool
#}

#specimenString:str -> str
#descriptionに書き込む検体
def specimenString(kentai) :
	if str(kentai) == '-' :
		kentai = 'unknown'
	else :
		if str(kentai) == 'h' :
			kentai = 'human'
		elif str(kentai) == 'm' :
			kentai = 'mice'
		elif str(kentai) == 'nd' :
			kentai = 'no_data'
		else :
			kentai = str(kentai)
	return kentai

#methodString:str -> str
#descriptionに書き込む方法論
def methodString(method) : #{
	if str(method) == '-' : #{
		method = 'unknown'
	#}
	else : #{
		method = str(method)
	#}
	return method
#}

#methodString:{'-',0,1} -> str
#descriptionに書き込む実験の有無
def clinic_testString(clinicbool) : #{
	if str(clinicbool) == '-' : #{
		clinicbool = 'unknown'
	#*
	else : #{
		if int(clinicbool) == 1 : #{
			clinicbool = 'true'
		#}
		elif int(clinicbool) == 0 : #{
			clinicbool = 'false'
		#}
		else : #{
			clinicbool = 'undef'
		#}
	#}
	return clinicbool
#}

#descriptionStrings:str*...*str -> list
#実際に書き込むdescriptionの元になる配列
def descriptionStrings(uptribool, kentai, method, clinicbool, kentaiC) : #{
	updown = updownString(uptribool)
	specimen = specimenString(kentai)
	method = methodString(method)
	#method = 'spam'
	clinic_test = clinic_testString(clinicbool)
	specimenC = specimenString(kentaiC)
	a = [updown,specimen,method,clinic_test,specimenC]
	return a
#}


for i in range(0,Nnode): #{
	lsNode = [] #[ID,Nodelabel,nodeID(taxIDなど)]
	ID = Nodes[i].getAttribute('id') #n0とか
	lsNode.append(ID)
	Nodelabel = Nodes[i].getElementsByTagName('y:NodeLabel')[0].childNodes[0].data #Escherichia_coliとか
	lsNode.append(Nodelabel)
	nodeID = Nodes[i].getElementsByTagName('data')[0].childNodes[0].data #562とか
	lsNode.append(nodeID)
	MatNodes.append(lsNode)
	'''
	x = Nodes[i].getElementsByTagName('y:Geometry')[0].getAttribute('x')
	y = Nodes[i].getElementsByTagName('y:Geometry')[0].getAttribute('y')
	x = float(x)
	y = float(y)
	lsNodeX.append(x)
	lsNodeY.append(y)
	'''
#}

for i in range(0,Nedge): #{
	lsEdge = [] #[ID,source,target]
	ID = Edges[i].getAttribute('id') #e0とか
	lsEdge.append(ID)
	source = Edges[i].getAttribute('source') #Escherichia_coliとか
	lsEdge.append(source)
	target = Edges[i].getAttribute('target') #Crohn's_diseaseとか
	lsEdge.append(target)
	MatEdges.append(lsEdge)
#}

L = 0 #カウンター
#ノードをいじる
for line in open(nodeFile) : #{
	L += 1
	name, size, color, shape, nodeID= line.rstrip().split('\t')
	for i in range(0,Nnode) : #{
		Node = Nodes[i]
		tmpnode = MatNodes[i][1]
		if name == tmpnode : #{
			#datas = Node.getElementsByTagName('data')
			yFill = Node.getElementsByTagName('y:Fill')[0]
			yFill.setAttribute('color',color)
		#}
		
	#}
	print('node color changed in line[%d]'%L)
#}

#入れ子がすごいことになっているので直積集合用いたループで簡略化した方がいいのかもしれない
L = 0
#エッジをいじる
for line in open(edgeFile) : #{
	L += 1
	e1, e2, score, color, edgeID, comment, uptribool, kentai, method, clinicbool, kentaiC= line.rstrip().split('\t') #EDITED BY NHayashi
	descArray = descriptionStrings(uptribool,kentai,method,clinicbool,kentaiC)
	#エッジのソースとターゲットをn0とかのidではなく名称で追えるようにする
	#そのために上でn0などと名称つまりNodelableとtaxIDつまりnodeIDとの対応を記した行列MatNodesを作っていた
	for i in range(0,Nedge): #{
		Edge = Edges[i]
		tmpe1 = MatEdges[i][1]
		tmpe2 = MatEdges[i][2]
		for x in range(0,len(MatNodes)) : #{
			if tmpe1 == MatNodes[x][0] : #{
				tmpe1 = MatNodes[x][1]
			#}
			if tmpe2 == MatNodes[x][0] : #{
				tmpe2 = MatNodes[x][1]
			#}
		#}
		#print(e1 == tmpe1)
		
		if (e1 == tmpe1 and e2 == tmpe2) : #{
			datas = Edge.getElementsByTagName('data')
			if len(datas)==2 : #{
				#comment = 'spam'
				comedoc = minidom.parseString('<data key="d10"><![CDATA[comment:%s\nupdown:%s\tspecimen:%s\tmethod:%s\nexperimental_validation:%s\tspecimen_for_experimental_validation:%s\n]]></data>'%(comment, descArray[0], descArray[1], descArray[2], descArray[3], descArray[4]))
				comeNode = comedoc.getElementsByTagName('data')[0]
				Edge.appendChild(comeNode)
				#print(comeNode.childNodes[0].data)
			#}
			else : #{
				description = 'comment:%s\nupdown:%s\tspecimen:%s\tmethod:%s\nexperimental_validation:%s\tspecimen_for_experimental_validation:%s\n'%(comment, descArray[0], descArray[1], descArray[2], descArray[3], descArray[4])
				for j in range(0,len(datas)): #{
					key = datas[j].getAttribute('key')
					if str(key) == "d10" : #{
						datas[j].childNodes[0].data = description
						#print(datas[j].childNodes[0].data)
					#}
					if str(key) == "d11" : #{
						Path = datas[j].getElementsByTagName('y:Path')[0]
						Path.setAttribute('sx',"0.0")
						Path.setAttribute('sy',"0.0")
						Path.setAttribute('tx',"0.0")
						Path.setAttribute('ty',"0.0")
						LineStyle = datas[j].getElementsByTagName('y:LineStyle')[0]
						LineStyle.setAttribute('color',str(color))
						LineStyle.setAttribute('width',score)
					#}
				#}
			#}
			print('adding comment success in Edges[%d] in line[%d].'%(i,L))
		#}
		else : #{
			spamspamspam = 1
		#}
	#}
#}

		
		

	
	



#ファイルを作って書き込んで閉じてgraphmlとする
commentedstr = xdoc0.toxml()
commentedxml = open('newdata_c.xml','w')
commentedxml.write(commentedstr)
commentedxml.close()
gmltoxml.T('newdata_c.xml',commentedFile)
"""
必ずyEDで開けるか生成後に確認する。たいてい日本語が混ざっていたり""によりxmlの構造が壊れたことが原因となるはずなので、
NodeLabelに日本語や""が存在しないことを確認する
"""

#po = Edges[12].getElementsByTagName('data')[1].getAttribute('key')
#print(po)
