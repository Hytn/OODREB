from logging import exception
import re
import ujson as json
import copy
import spacy 

with open(r"/datasets/nyt_10_manual/nyt_10_manual.txt",encoding="UTF-8") as file_object:
    lines=file_object.readlines()
i=0

nlp = spacy.load("en_core_web_md")
dataList=[]
index=0
for line in lines:
    str=line.rstrip()
    rObj=json.loads(str)
    #开始处理
    dataElement={}
    vertexSetFather=[]
    vertexSetSonH=[]
    vertexSetSonT=[]
    vertex={}
    headpos=[]
    tailpos=[]
    labels={}

    # text=rObj['text']
    # texthead=text[rObj['h']['pos'][0]:rObj['h']['pos'][1]]

    dataElement['dataset']='NYT-10M'
    dataElement['title']=''
    labels['r']= rObj['relation']
    labels['h']=0
    labels['t']=1
    labels['evidence']=[0]

    doc = nlp(rObj['text'])
    listtokens=[]

    listtokensHead=[]
    docHead=nlp(rObj['text'][rObj['h']['pos'][0]:rObj['h']['pos'][1]])
    for tokenHead in docHead:
         listtokensHead.append(tokenHead.text)
 
    listtokensTail=[]
    docTail=nlp(rObj['text'][rObj['t']['pos'][0]:rObj['t']['pos'][1]])
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
        if index==7346 or index==7666:
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
        if index==1391 or index==10065:
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

with open('nyt_10_manual.json', 'w', encoding ='utf8') as json_file:
    json.dump(dataList, json_file,escape_forward_slashes=False)