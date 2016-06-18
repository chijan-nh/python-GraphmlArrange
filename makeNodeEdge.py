#coding:utf-8
#utf-8なので日本語コメントが使えるはず

#ターミナルでの使い方
#$ python makeNodeEdge.py oriTSV.txt nodemd.dat edgemd.dat phymd.csv
#oriTSVはエクセルで作ったデータベースを細菌でsortしてからtsvとして保存したもの
#最終行がnull byteになるのでこれを削除しておく
#mdは月日。例えばnode0218.datとする

import sys
oritable = str(sys.argv[1]) #元database
nodetable = str(sys.argv[2]) #作成するnodeのtsv
edgetable = str(sys.argv[3]) #作成するedgeのtsv
phyloTcsv = str(sys.argv[4]) #phyloTのために作成するtaxIDのcsvファイル名

#ファイル書き込み
nodeFile = open(nodetable,'w')
edgeFile = open(edgetable,'w')
phyFile = open(phyloTcsv,'w') 

#uniq:list -> list
#sort|uniqコマンドのようなもの
def uniq(seq) : #{
	new_ls = []
	new_ls_add = new_ls.append
	seen = set()
	seen_add = seen.add
	for item in seq : #{
		item = tuple(item)
		if item not in seen : #{
			seen_add(item)
			new_ls_add(item)
		#}
	#}
	return new_ls
#}

#lsmarge:list*list -> void
#seq1にseq2の一意な中身を後ろから継ぎ足すことで配列をマージするサブルーチン
def lsmarge(seq1,seq2) : #{
	addseq = uniq(seq2)
	for item in addseq : #{
		seq1.append(item)
	#}
#}

#getNodeColor:str -> str
#nodeの色をrankから定義する。疾病ノードは所属するオントロジーから設定し、細菌ノードは所属する門から設定
#必要があればこの関数をいじってノードデータの色を変えてaddingdescriptionすると幸せになれる
def getNodeColor(rank) : #{
	if str(rank) == 'd0' : #{
		return '#008000'
	#}
	elif str(rank) == 'd1' : #{
		return '#FF8C00'
	#}
	elif str(rank) == 'd2' : #{
		return '#FFD700'
	#}
	elif str(rank) == 'd3' : #{
		return '#8A2BE2'
	#}
	elif str(rank) == 'd4' : #{
		return '#008080'
	#}
	elif str(rank) == 'd5' : #{
		return '#87CEEB'
	#}
	elif str(rank) == 'd6' : #{
		return '#d2b48c'
	#}
	elif int(rank) == 201174 : #{
		return '#ff1493'
	#}
	elif int(rank) == 976 : #{
		return '#dc143c'
	#}
	elif int(rank) == 1224 : #{
		return '#FF0000'
	#}
	elif int(rank) == 1239 : #{
		return '#ff69b4'
	#}
	elif int(rank) == 32066 : #{
		return '#ff4500'
	#}
	elif int(rank) == 74201 : #{
		return '#c71585'
	#}
#}

#getEdgeColor:str -> str
#getNodeCOlorのEdge版。ただしスコア・容量関数すなわちエッジの太さもここで定義している
#よって今後スコアを変更する場合はこの関数をいじってaddingdescriptionすると幸せになれる
def getEdgeColor(updown) : #{
	if str(updown) == '-' :
		return [1,'#C0C0C0']
	#}
	elif int(updown) == 1 : #{
		return [3,'#000000']
	#}
	elif int(updown) == 0 : #{
		return [2,'#808080']
	#}
	elif int(updown) == -1 : #{
		return [3,'#0000FF']
	#}
#}

#makeNode:str*str*str*str*str*fileobject -> void
#作成するnodeのtsvの形式に合わせてノード１つ分のデータをtsvとして書き込む
def makeNode(name, size, ncolor, shape, nodeID,ofp) : #{
	ofp.write('%s\t%f\t%s\t%s\t%s\n'%(name,size,ncolor,shape,nodeID))
#}

#makeEdge:str*...*str*fileobject -> void
#作成するedgeのtsvの形式に合わせてエッジ１つ分のデータをtsvとして書き込む
def makeEdge(source, target, score, ecolor, edgeID, comment, uptribool, kentai, method, clinicbool, kentaiC, ofp) : #{
	ofp.write('%s\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(source, target, score, ecolor, edgeID, comment, uptribool, kentai, method, clinicbool, kentaiC))
#}

#tsvをパースするための準備 delimiterをタブ文字にすればcsvライブラリで行ける
import csv
oridata = csv.DictReader(open(oritable, 'rU'), delimiter = '\t') #エクセルの最初の行を辞書のキーとして連想配列の形でテーブルを読めるようにパース
creatures = [] #生物種（１５年度では細菌）のリスト
diseases = [] #疾病のリスト
Nodedata = [] #ノードデータのリスト。これを用いてtsvの各行をmakeNodeする
Edgedata = [] #エッジデータのリスト。これを用いてtsvの各行をmakeEdgeする

for row in oridata : #{
	#print(row['creature'])
	#a.append(row['taxID'])
	creatures.append([row['bacteria'],row['Phylo'],row['taxID']])
	diseases.append([row['disease'],row['DO1'],'-'])
	Edgedata.append([row['bacteria'],row['disease'],row['PMID'],row['comment'],row['updown'],row['specimen'],row['method'],row['experimental_validation'],row['specimen_for_experimental_validation']])
#}

#creatures,diseasesの順番ででノードデータを作る
"""
#nodemd.dat
bacteria1 hoge1
...
bacteriaX hogeX
disease1 hogeX+1
...
diseaseY hogeX+Y
が目標
"""
lsmarge(Nodedata,creatures)
lsmarge(Nodedata,diseases)

#sort|uniqして細菌名や疾病名が同じノードが複数できないようにする
NodeUNIQED = uniq(Nodedata)
'''
NodeUNIQED = [
('nodeLabel','rank(Ncolor is depend on rank)','nodeID'),...
]
'''
#print(NodeUNIQED[0][1])

#確実にいるであろう大腸菌のtaxIDをとりあえずphyloT用csvに書いておく
phyFile.write('562')

#ノードデータから実際にそれをtsvとして書く
for v in NodeUNIQED : #{
	color = getNodeColor(v[1])
	makeNode(v[0],50.0,color,'circle',v[2],nodeFile)
	phyFile.write(',%s'%v[2])
#}
#エッジデータから実際にそれをtsvとして書く
for v in Edgedata : #{
	poyo = getEdgeColor(v[4])
	makeEdge(v[0],v[1],poyo[0],poyo[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],edgeFile)
#}

#ファイルは閉じる
nodeFile.close()
edgeFile.close()
phyFile.close()
#処理終了を明記
print('SUCCESS')



