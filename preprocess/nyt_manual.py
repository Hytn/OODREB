from logging import exception
import re
import spacy 
import ujson as json
import copy

def SearchString(a,b):
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



with open(r"/datasets/nyt-manual/test.json") as file_object:
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
    vertex={}
    labels={}

    dataElement['dataset']='NYT-manual'
    dataElement['title']=rObj['articleId']


    # labels['r']= rObj['relation']
    # # labels['h']=0
    # # labels['t']=1
    # labels['evidence']=[0]
    doc = nlp(rObj['sentText'])
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

with open('myfile_nytmanual.json', 'w', encoding ='utf8') as json_file:
    json.dump(dataList, json_file,escape_forward_slashes=False)
