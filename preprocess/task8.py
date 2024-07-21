from logging import exception
import re
import spacy 
import ujson as json
import copy

modifyMap={"Entity-Origin(e1,e2)":"P807","Entity-Origin(e2,e1)":"P807","Component-Whole(e2,e1)":"P361","Component-Whole(e1,e2)":"P361"}

with open(r"/datasets/task8/train.txt") as file_object:
    lines=file_object.readlines()
i=0
nlp = spacy.load("en_core_web_md")

dataList=[]
for line in lines:
    if i%4==0:
      str=line.rstrip()
    # strlist=re.findall('(\d+[A-Za-z]+)',str)
      #print(str)
      str=(str.split("\t"))[1]
      str=str.strip('"') 
    #   print(str)
    #   print(re.findall('(<e1>[A-Za-z]+</e1>)',str))
    # str="Even commercial <e1>networks</e1> have moved into <e2>high-definition broadcast</e2>."
      doc = nlp(str)
    # print([(w.text, w.pos_) for w in doc])
      listtokens=[]
      index=0
      for token in doc:
         listtokens.append(token.text)
         if token.text.find('</e1')!=-1:
             e1pos=index
             listtokens[index]=listtokens[index][0:(len(listtokens[index])-4)]
         if token.text.find('</e2')!=-1:
             e2pos=index
             listtokens[index]=listtokens[index][0:(len(listtokens[index])-4)]
         index=index+1

      for e1p in range(e1pos,0,-1):
          if listtokens[e1p]=="e1":
              e1start=e1p+2
              break
      for e2p in range(e2pos,0,-1):
          if listtokens[e2p]=="e2":
              e2start=e2p+2
              break
      if e1start<e2start:
          ebefore=e1start-2-1
          listtokens=(listtokens[0:ebefore]+listtokens[e1start:e1pos+1]+listtokens[e1pos+2:(e2start-2-1)]+listtokens[e2start:e2pos+1]+listtokens[e2pos+2:])
          e1start=e1start-3
          e1pos=e1pos-3
          e2start=e2start-3-1-3
          e2pos=e2pos-3-1-3
      else:
          ebefore=e2start-2-1
          listtokens=(listtokens[0:ebefore]+listtokens[e2start:e2pos+1]+listtokens[e2pos+2:(e1start-2-1)]+listtokens[e1start:e1pos+1]+listtokens[e1pos+2:])
          e2start=e2start-3
          e2pos=e2pos-3
          e1start=e1start-3-1-3
          e1pos=e1pos-3-1-3

      #print(type(listtokens[0]))
    if i%4==1:
        str2=line[:-1]
    if i%4==2:
        str3=line
    if i%4==3:

       dataElement={}
       vertexSetFather=[]
       vertexSetSonH=[]
       vertexSetSonT=[]
       vertex={}
       headpos=[]
       tailpos=[]
       labels={}

       #print(e1start,e1pos,e2start,e2pos,listtokens)
       headpos.append(e1start)
       headpos.append(e1pos+1)
       tailpos.append(e2start)
       tailpos.append(e2pos+1)

       dataElement['dataset']='SemEval-2010_train'
       dataElement['title']=''
       labels['r']=str2
       labels['h']=0
       labels['t']=1
       if str2[len(str2)-3:]=='e1)':
           labels['h']=1
           labels['t']=0
       labels['evidence']=[0]

       dataSents=[]
       dataSents.append(listtokens)
       dataElement['sents']=dataSents

       vertex['sent_id']=0
       headName=listtokens[e1start]
       for ii in range(e1start+1,e1pos+1):
          headName=headName+" "+listtokens[ii]
       vertex['name']=headName
       vertex['type']="null" #null
       vertex['pos']=headpos
       vertexSetSonH.append(copy.copy(vertex))

       tailName=listtokens[e2start]
       for jj in range(e2start+1,e2pos+1):
          tailName=tailName+" "+listtokens[jj]
       vertex['name']=tailName
       vertex['type']="null" #null
       vertex['pos']=tailpos
       vertexSetSonT.append(copy.copy(vertex))

       vertexSetFather.append(vertexSetSonH)
       vertexSetFather.append(vertexSetSonT)
      #print(vertexSetFather)

       labelsList=[]
       labelsList.append(labels)
       dataElement['labels']=labelsList
       dataElement['vertexSet']=vertexSetFather

      #print(dataElement)
      #dataList.append(copy.copy(dataElement))
       if dataElement['labels'][0]["r"] in modifyMap.keys():
           dataElement['labels'][0]["r"]=modifyMap[dataElement['labels'][0]["r"]]
           dataList.append(dataElement)
       else:
           i=i+1
           continue
    i=i+1
print(len(dataList))
# with open('train_semval2010_task8.json', 'w', encoding ='utf8') as json_file:
with open('task8.json', 'w', encoding ='utf8') as json_file:
    json.dump(dataList, json_file, escape_forward_slashes=False)

