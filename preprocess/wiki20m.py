from logging import exception
import re
import ujson as json
import copy

with open(r"/datasets/wiki20m/wiki20m_test.txt",encoding="UTF-8") as file_object:
    lines=file_object.readlines()
i=0

dataList=[]
index=0
for line in lines:
    str=line.rstrip()
    rObj=json.loads(str)
 
    dataElement={}
    vertexSetFather=[]
    vertexSetSonH=[]
    vertexSetSonT=[]
    vertex={}
    headpos=[]
    tailpos=[]
    labels={}

    dataElement['dataset']='wiki20m'
    dataElement['title']=''
    labels['r']= rObj['relation']
    labels['h']=0
    labels['t']=1
    labels['evidence']=[0]

    listtokens=rObj['token']
 
    dataSents=[]
    dataSents.append(listtokens)
    dataElement['sents']=dataSents

    vertex['sent_id']=0
    vertex['name']=rObj["h"]["name"]
    vertex['type']="null" #null
    vertex['pos']=rObj["h"]["pos"]
    vertexSetSonH.append(copy.copy(vertex))

    vertex['name']=rObj["t"]["name"]
    vertex['type']="null" #null
    vertex['pos']=rObj["t"]["pos"]
    vertexSetSonT.append(copy.copy(vertex))

    
    vertexSetFather.append(vertexSetSonH)
    vertexSetFather.append(vertexSetSonT)

    labelsList=[]
    labelsList.append(labels)
    dataElement['labels']=labelsList
    dataElement['vertexSet']=vertexSetFather
    dataList.append(dataElement)

    index=index+1
    
print("OK")

with open('wiki20m.json', 'w', encoding ='utf8') as json_file:
    json.dump(dataList, json_file,escape_forward_slashes=False)
