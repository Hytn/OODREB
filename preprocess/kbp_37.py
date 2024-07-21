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


modifyMap={"per:spouse(e1,e2)":"P26","per:spouse(e2,e1)":"P26",
           "per:employee_of(e1,e2)":"P108","per:employee_of(e2,e1)":"P108",
           "per:countries_of_residence(e2,e1)":"P551","per:countries_of_residence(e1,e2)":"P551",
           "per:stateorprovinces_of_residence(e1,e2)":"P551","per:stateorprovinces_of_residence(e2,e1)":"P551",
           "per:cities_of_residence(e2,e1)":"P551","per:cities_of_residence(e1,e2)":"P551",
           "per:country_of_birth(e1,e2)":"P19","per:country_of_birth(e2,e1)":"P19",
           "org:subsidiaries(e1,e2)":"P355","org:subsidiaries(e2,e1)":"P355",
           "org:top_members/employees(e1,e2)":"P488", "org:top_members/employees(e2,e1)":"P488",
           "org:founded(e2,e1)":"P571","org:founded(e1,e2)":"P571",
           "org:founded_by(e1,e2)":"P112","org:founded_by(e2,e1)":"P112",
           "org:country_of_headquarters(e1,e2)":"P159","org:country_of_headquarters(e2,e1)":"P159",
           "org:stateorprovince_of_headquarters(e1,e2)":"P159","org:stateorprovince_of_headquarters(e2,e1)":"P159",
           "org:city_of_headquarters(e1,e2)":"P159","org:city_of_headquarters(e2,e1)":"P159"
           }

with open(r"/datasets/kbp-37/test.txt") as file_object:
    lines=file_object.readlines()
i=0
nlp = spacy.load("en_core_web_md")

dataList=[]
for line in lines:
    if i%4==0:
      str=line.rstrip()
      str=(str.split("\t"))[1] 
      str=str.strip('"') 
      doc = nlp(str)
      listtokens=[]
      index=0

      ###############+++++++++++++++ only for test
      for token in doc:
         listtokens.append(token.text)
      s1=SearchString(listtokens,['<','e1','>'])
      s2=SearchString(listtokens,['<','/e1','>'])
      s11=SearchString(listtokens,['<','e2','>'])
      s22=SearchString(listtokens,['<','/e2','>'])

      e1pos=[s1[1],s2[0]]
      e2pos=[s11[1],s22[0]]

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

       headpos.append(e1pos[0])
       headpos.append(e1pos[1])
       tailpos.append(e2pos[0])
       tailpos.append(e2pos[1])

       dataElement['dataset']='kbp_37_test'
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
       headName=listtokens[e1pos[0]]
       for ii in range(e1pos[0]+1,e1pos[1]):
          headName=headName+" "+listtokens[ii]
       vertex['name']=headName
       vertex['type']="null" #null
       vertex['pos']=headpos
       vertexSetSonH.append(copy.copy(vertex))

       tailName=listtokens[e2pos[0]]
       for jj in range(e2pos[0]+1,e2pos[1]):
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
with open('test_kbp_37.json', 'w', encoding ='utf8') as json_file:
    json.dump(dataList, json_file, escape_forward_slashes=False)

