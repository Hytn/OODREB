from logging import exception
import re
import spacy 
import ujson as json
import copy

with open(r"/datasets/tacred/relmap.json","r") as fhmap:
    modiMap=json.load(fhmap)

with open(r"/datasets/tacred/train.json","r") as file_object:
    data=json.load(file_object)
i=0
print(len(data))

dataList=[]
index=0
for line in data:

    dataElement={}
    vertexSetFather=[]
    vertexSetSonH=[]
    vertexSetSonT=[]
    vertex={}
    headpos=[]
    tailpos=[]
    labels={}

    dataElement['dataset']='tacred_train'
    dataElement['title']=line['docid']
    labels['r']= line['relation']
    labels['h']=0
    labels['t']=1
    labels['evidence']=[0]

    listtokens=line['token']
    if line['docid']=='eng-NG-31-108589-8120474':
        print(listtokens[0])
        print(line['token'][0])

    headpos.append(line['subj_start'])
    headpos.append(line['subj_end']+1)

    tailpos.append(line['obj_start'])
    tailpos.append(line['obj_end']+1)
    
    dataSents=[]
    dataSents.append(listtokens)
    dataElement['sents']=dataSents

    vertex['sent_id']=0
    headName=listtokens[headpos[0]]
    for ii in range(headpos[0]+1,headpos[1]):
        headName=headName+" "+listtokens[ii]
    vertex['name']=headName 
    vertex['type']=line["subj_type"]
    vertex['pos']=headpos
    vertexSetSonH.append(copy.copy(vertex))

    tailName=listtokens[tailpos[0]]
    for ii in range(tailpos[0]+1,tailpos[1]):
        tailName=tailName+" "+listtokens[ii]
    vertex['name']=tailName 
    vertex['type']=line["obj_type"] 
    vertex['pos']=tailpos
    vertexSetSonT.append(copy.copy(vertex))

    vertexSetFather.append(vertexSetSonH)
    vertexSetFather.append(vertexSetSonT)

    labelsList=[]
    labelsList.append(labels)
    dataElement['labels']=labelsList
    dataElement['vertexSet']=vertexSetFather

    if dataElement['labels'][0]["r"] in  modiMap.keys():
           dataElement['labels'][0]["r"]= modiMap[dataElement['labels'][0]["r"]]
           dataList.append(dataElement)
    else:
           index=index+1
           continue
    #dataList.append(dataElement)
    index=index+1
    
print(len(dataList))

with open('tacred_train.json', 'w', encoding ='utf8') as json_file:
    json.dump(dataList, json_file,escape_forward_slashes=False) # ensure_ascii = False)