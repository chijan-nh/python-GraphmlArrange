#coding:utf-8
'''
how to use
$ python addingdata3.py node edge origin newgraph
node:nodedata.dat
	a tab-delimited file for adding node information.
	each line corresponds to each node.
	name(string)\\tsize(float)\\tcolor(rgba-string:e.g.#FF00FF)\\tshape(string: e.g. 'roundrectangle', 'ellipse', etc.)\\tnodeID(str)
edge:edgedata.dat
	a tab-delimited file for edge information.
    each line corresponds to each edge.
    name1(should be compatible with nodeFile)\\tname2\\tscore(float)\\tcolor(rgba-string:e.g.#FF0000)\\tedgeID(str)\\tcomment(str)\\tupdown(str)\\tkentai(str)\\tmethod(str)\\tclinical_test(str)\\tkentaiC(str)
origin:origindata.graphml
	an original bacteria2disease data graphml file.
newgraph:newdata.graphml
	a graphml file which node and edge is added in the origin file.

'''
import sys
array=str(sys.argv)
nodeFile=str(sys.argv[1])
edgeFile=str(sys.argv[2])
origin=str(sys.argv[3])
newgraph=str(sys.argv[4])

print(nodeFile+' '+edgeFile+' '+origin+' '+newgraph)

import graphmltkool3

toaddheader = '''\
<?xml version="1.0" encoding="UTF-8"?>
 <graphml xmlns="http://graphml.graphdrawing.org/xmlns/graphml" 
 xmlns:y="http://www.yworks.com/xml/graphml" 
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
 xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns/graphml 
 http://www.yworks.com/xml/schema/graphml/1.0/ygraphml.xsd">
 
  <graph id="G" edgedefault="directed">'''
toadd = open('toadd.graphml','w')
toadd.write(toaddheader)
#print(graphmltkool3.footer)

import gmltoxml
#gmltoxml.T('toadd.graphml','toadd.xml')
gmltoxml.T(origin,'origindata.xml')


from xml.dom import minidom
# make xml
# empty root element:<kesuyo />
xdoc = minidom.parseString('<kesuyo />')



# read xmlfile
# print(type(NodeID))
xdoc0 = minidom.parse("origindata.xml")
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
MatNode == [
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
for i in range(0,Nnode):
	lsNode = []
	ID = Nodes[i].getAttribute('id')
	lsNode.append(ID)
	Nodelabel = Nodes[i].getElementsByTagName('y:NodeLabel')[0].childNodes[0].data
	lsNode.append(Nodelabel)
	nodeID = Nodes[i].getElementsByTagName('data')[0].childNodes[0].data
	lsNode.append(nodeID)
	MatNodes.append(lsNode)

	x = Nodes[i].getElementsByTagName('y:Geometry')[0].getAttribute('x')
	y = Nodes[i].getElementsByTagName('y:Geometry')[0].getAttribute('y')
	x = float(x)
	y = float(y)
	lsNodeX.append(x)
	lsNodeY.append(y)

for i in range(0,Nedge):
	lsEdge = []
	ID = Edges[i].getAttribute('id')
	lsEdge.append(ID)
	source = Edges[i].getAttribute('source')
	lsEdge.append(source)
	target = Edges[i].getAttribute('target')
	lsEdge.append(target)
	MatEdges.append(lsEdge)

#print(MatNodes)
#print(MatEdges)
#read and make node
N = Nnode
maxX = max(lsNodeX)
minX = min(lsNodeX)
maxY = max(lsNodeY)
minY = min(lsNodeY)
for line in open(nodeFile):
        name, size, color, shape, nodeID = line.rstrip().split('\t')
        size = float(size)
        X = float(minX)-2*size
        Y = float(minY)-2*size
        hantei = 0
        if nodeID == '-' :
        	for i in range(0,Nnode):
        		oldLabel = MatNodes[i][1]
        		if name == oldLabel :
        			hantei +=1

        else:
        	for i in range(0,Nnode):
        		oldnodeID = MatNodes[i][2]
        		#print(oldnodeID)
        		#print(nodeID)

        		if nodeID == oldnodeID :
        			hantei += 1
        		#print(hantei)
        		#print('N=' + str(N))
        if hantei == 0 :
        	Nstr = str(N)
        	graphmltkool3.normal_node(name, color, size, name, 'true', X, Y, shape, nodeID, toadd)
        	#'n%s'%Nstr
        	N += 1
print("Nodes have been written.")
#read and make edge
#M = Nedge

for line in open(edgeFile):
        e1, e2, score, color, edgeID, comment, uptribool, kentai, method, clinicbool, kentaiC= line.rstrip().split('\t') #EDITED BY NHayashi
        score = float(score)
        flagAnd = 0
        flagSrc = 0
        flagTgt = 0
        flagNor = 0
        truesourceID = ''
        truetargetID = ''
        for i in range(0,Nnode):
        	sourceLabel = MatNodes[i][1]
        	sourceID = MatNodes[i][0]
        	
        	#print(sourceLabel)
        	if e1 == sourceLabel :
        		for j in range(0,Nnode):
        			targetLabel = MatNodes[j][1]
        			targetID = MatNodes[j][0]
        			#print(targetLabel)
        			if e2 == targetLabel :
        				flagAnd += 1
        				for a in MatEdges:
        					#print(a)
        					if a[1]==sourceID and a[2]==targetID :
        						flagAnd = 0
        						
        				if flagAnd == 1 :
        					truesourceID = sourceID
        					truetargetID = targetID
        			else :
        				flagSrc += 1
        				if flagSrc == Nnode :
        					truesourceID = sourceID

        	else :
        		for j in range(0,Nnode):
        			targetLabel = MatNodes[j][1]
        			targetID = MatNodes[j][0]
        			if e2 == targetLabel :
        				flagTgt += 1
        				if flagTgt == Nnode :
        					truetargetID = targetID
        			else :
        				flagNor += 1


        #print('e1= '+e1)
        #print('e2= '+e2)
        print('flags= ' + str(flagAnd) + ',' + str(flagSrc) + ',' + str(flagTgt) + ',' +str(flagNor))
        if flagAnd == 1 :
        	graphmltkool3.normal_edge(truesourceID,truetargetID,score,color,'01',edgeID,comment,toadd)
        elif flagSrc == Nnode :
        	graphmltkool3.normal_edge(truesourceID,e2,score,color,'01',edgeID,comment,toadd)
        elif flagTgt == Nnode :
        	graphmltkool3.normal_edge(e1,truetargetID,score,color,'01',edgeID,comment,toadd)
        elif flagNor == Nnode*Nnode :
        	graphmltkool3.normal_edge(e1,e2,score,color,'01',edgeID,comment,toadd)

print("Edges have been written.")

toadd.write(graphmltkool3.footer)
toadd.close()
gmltoxml.T('toadd.graphml','toadd.xml')
xdoc1 = minidom.parse("toadd.xml")




'''
lenOriginNodes = len(xdoc0.getElementsByTagName('node'))
for i in range(0,lenOriginNodes):
	Nodes = xdoc0.getElementsByTagName('node')[i]
	ifNodeID=Nodes.getElementsByTagName('data')[0].childNodes[0].data
	print(ifNodeID)
	#yGeo.setAttribute('x','1')
	#hoge.append(e.childNodes[0].data)
	#hoge.append(float(x))
	if ifNodeID==NodeID :
		NodeName=Nodes.getElementsByTagName('y:NodeLabel')[0]
		print("NodeName of " + "NodeID = " + NodeID + " is " + NodeName.childNodes[0].data)
'''


# adding
clone = xdoc0.cloneNode(xdoc0.documentElement)
#print(clone)
xdoc.documentElement.appendChild(xdoc0.documentElement)
xdoc.documentElement.appendChild(xdoc1.documentElement)
'''
fuga = xdoc.getElementsByTagName('y:NodeLabel')
print("hoge2")
#for x in hoge:
#	print(x)

print(hoge)
'''
print("XMLs have been marged.")
# file transform string
xmldoc = xdoc
#str = """It is meaningless only to think my long further aims idly.
#It is important to set my aims but at the same time I should confirm my present condition.
#Unless I set the standard where I am in any level, I'll be puzzled about what I should do from now on."""

newdoc = minidom.getDOMImplementation().createDocument(None, "graphml", None)


'''
MEMO
<graphml 
xmlns="http://graphml.graphdrawing.org/xmlns" 
xmlns:java="http://www.yworks.com/xml/yfiles-common/1.0/java" 
xmlns:sys="http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0" 
xmlns:x="http://www.yworks.com/xml/yfiles-common/markup/2.0" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xmlns:y="http://www.yworks.com/xml/graphml" 
xmlns:yed="http://www.yworks.com/xml/yed/3" 
xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd">
'''

#for yED
root_node = newdoc.documentElement
root_node.setAttribute('xmlns', 'http://graphml.graphdrawing.org/xmlns')
root_node.setAttribute('xmlns:java', 'http://www.yworks.com/xml/yfiles-common/1.0/java')
root_node.setAttribute('xmlns:sys','http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0')
root_node.setAttribute('xmlns:x','http://www.yworks.com/xml/yfiles-common/markup/2.0')
root_node.setAttribute('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
root_node.setAttribute('xmlns:y','http://www.yworks.com/xml/graphml')
root_node.setAttribute('xmlns:yed','http://www.yworks.com/xml/yed/3')
root_node.setAttribute('xsi:schemaLocation','http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd')


graphmls = xmldoc.getElementsByTagName('graphml')
for graphml in graphmls:
    for child in graphml.childNodes:
        newdoc.documentElement.appendChild(child.cloneNode(True))
 
xstr = newdoc.toxml()
 

f = open('newdata.xml', 'w') #open file with w-mode
f.write(xstr) #write xstr in the xml
f.close() #close file
print("newdata.xml has been written.")

gmltoxml.T('newdata.xml',newgraph)
print("SUCCESS") #terminate
