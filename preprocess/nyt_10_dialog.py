from logging import exception
import re
import spacy 
import ujson as json
import copy


with open(r"/datasets/nyt_10_dialog/test.json") as file_object:
    lines=file_object.readlines()
i=0
nlp = spacy.load("en_core_web_md")

dataList=[]
index=0
for line in lines:
    # if index==2812:
    #     continue
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

    dataElement['dataset']='NYT-10'
    dataElement['title']=''
    labels['r']= rObj['relation']
    labels['h']=0
    labels['t']=1
    labels['evidence']=[0]

    doc = nlp(rObj['sentence'])
    listtokens=[]

    listtokensHead=[]
    docHead=nlp(rObj['head']['word'])
    for tokenHead in docHead:
         listtokensHead.append(tokenHead.text)

    listtokensTail=[]
    docTail=nlp(rObj['tail']['word'])
    for tokenTail in docTail:
        listtokensTail.append(tokenTail.text)

    for token in doc:
         listtokens.append(token.text)
 
    # if len(listtokensHead)==1:
    headpos.append(listtokens.index(listtokensHead[0]))
    headpos.append(listtokens.index(listtokensHead[len(listtokensHead)-1],headpos[0])+1)
    # else:
    # if headpos[1]-headpos[0]!=len(listtokensHead):
    #     print("Head Error!!",index)
    while headpos[1]-headpos[0]!=len(listtokensHead):
        if index==9827:
            headpos[1]=listtokens.index(listtokensHead[0],headpos[0]+1)+1
            print(headpos[1]-headpos[0])
            break

        try:
            headpos[0]=listtokens.index(listtokensHead[0],headpos[0]+1)
            headpos[1]=listtokens.index(listtokensHead[len(listtokensHead)-1],headpos[0]+1)+1
        except:
            print("Head Error!!",index)
    # if len(listtokensTail)==1:
    tailpos.append(listtokens.index(listtokensTail[0]))
    tailpos.append(listtokens.index(listtokensTail[len(listtokensTail)-1],tailpos[0])+1)
    # if tailpos[1]-tailpos[0]!=len(listtokensTail):
    #     print("Tail Error!!",index)
    while tailpos[1]-tailpos[0]!=len(listtokensTail):
        if index==2812:
            tailpos[1]=listtokens.index(listtokensTail[0],tailpos[0]+1)+1
            print(tailpos[1]-tailpos[0])
            break
        try:
           tailpos[0]=listtokens.index(listtokensTail[0],tailpos[0]+1)
           tailpos[1]=listtokens.index(listtokensTail[len(listtokensTail)-1],tailpos[0]+1)+1
        except:
           print("Tail Error!!",index)
   
    dataSents=[]
    dataSents.append(listtokens)
    dataElement['sents']=dataSents

    vertex['sent_id']=0
    headName=" ".join(listtokensHead)
    vertex['name']=headName #对应实际头实体名字
    vertex['type']="null" #null
    vertex['pos']=headpos
    vertexSetSonH.append(copy.copy(vertex))

    tailName=" ".join(listtokensTail)
    vertex['name']=tailName #对应实际头实体名字
    vertex['type']="null" #null
    vertex['pos']=tailpos
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

with open('nyt_10_dialog.json', 'w', encoding ='utf8') as json_file:
    json.dump(dataList, json_file,escape_forward_slashes=False)


