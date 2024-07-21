from logging import exception
import re
import spacy 
import ujson as json
import copy

def SearchString(a,b):
    if b[0]=="Calif":
        outpos=a.index("Calif.",0)
    else:
        if b[0]=="Merce":
            outpos=a.index("--Merce",0)
        else:
            if b[0]=="N.Y" or b[0]=="N.M" or b[0]=="Okla" or b[0]=="Fla":
                outpos=a.index(b[0]+".",0)
            else:
                if b[0]=="Pitie" or b[0]=="German":
                    outpos=a.index(b[0]+"-",0)
                else:
                    # if b[0]=="INA":
                    #     outpos=a.index("-INA-,Rwhich",0)
                    # else:
                    outpos=a.index(b[0],0)
    while True:
        pos=outpos
        flag=True
        for i in range(len(b)):
            if a[pos]==b[i]:
                pos=pos+1
                continue
            else:
                flag=False
                break
        if i==(len(b)-1) and flag!=False:
            return [outpos,pos]
            break
        else:
            outpos=outpos+1
            try:
               outpos=a.index(b[0],outpos)
            except:
               return [-1,-1]
    #    pos=a.index(b[0],pos)

with open(r"/datasets/wiki_kbp/test.json") as file_object:
    lines=file_object.readlines()
i=0
nlp = spacy.load("en_core_web_md")

dataList=[]
index=0
for line in lines:
    str=line.rstrip()
    rObj=json.loads(str)

    dataElement={}
    vertex={}
    labels={}

    dataElement['dataset']='wiki-kbp'
    dataElement['title']=rObj['articleId']

    doc = nlp(rObj['sentText'].replace("''"," "))
    if index==281:
        doc = nlp(rObj['sentText'].replace("-INA-","INA"))
    
    listtokens=[]
    for token in doc:
         listtokens.append(token.text)

    labelsList=[]
    tempRelations=rObj['relationMentions']
    tempEnties=rObj['entityMentions']
    for relNum in range(len(tempRelations)):
        labels['r']=tempRelations[relNum]['label']
        def htpos(subet,enties):
            for enum in range(len(enties)):
                if enties[enum]['text']==subet:
                    return enum
        labels['h']=htpos(tempRelations[relNum]['em1Text'],tempEnties)
        labels['t']=htpos(tempRelations[relNum]['em2Text'],tempEnties)
        labels['evidence']=[0]
        labelsList.append(copy.copy(labels))
    print(labelsList)

    entityList=[]
    for enNum in range(len(tempEnties)):
        subenList=[]
        def enfenci(words):
            doc = nlp(words)
            entitytokens=[]
            for token in doc:
               entitytokens.append(token.text)
            return entitytokens," ".join(entitytokens)

        tempet, vertex['name']=enfenci(tempEnties[enNum]['text'])
        vertex['pos']=SearchString(listtokens,tempet)
        vertex['sent_id']=0
        vertex['type']=tempEnties[enNum]['label']
        subenList.append(copy.copy(vertex))
        entityList.append(subenList)

    dataSents=[]
    dataSents.append(listtokens)
    dataElement['sents']=dataSents

    dataElement['labels']=labelsList
    dataElement['vertexSet']=entityList
    dataList.append(dataElement)

    index=index+1
    
print("OK")

with open('wiki_kbp.json', 'w', encoding ='utf8') as json_file:
    json.dump(dataList, json_file,escape_forward_slashes=False)

    