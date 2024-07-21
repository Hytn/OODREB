from tqdm import tqdm
import ujson as json
import copy

dataList=[]
count=1

# val:157 test:199  train:624
modifyMap={"Work_For":"P108","Live_In":"P361","OrgBased_In":"P159"}

with open(r"datasets/conll04/conll04_train.json","r") as fh:
    data=json.load(fh)
for record in data:
      dataElement={}
      vertexSetFather=[]
      vertexSetSon=[]
      vertex={}
      labels={}
      # print(count)
      count=count+1
      dataElement['dataset']='conll4_train'
      dataElement['title']=record['orig_id']

      dataSents=[]
      dataSents.append(record["tokens"])
      dataElement['sents']=dataSents

      vertex['sent_id']=0

      for i in range((len(record['entities']))):
         enPos=[]
         enPos.append(record['entities'][i]['start'])
         enPos.append(record['entities'][i]['end'])
         innerkh=[]
         vertex['pos']=enPos
         vertex['name']=" ".join(record["tokens"][record['entities'][i]['start']:record['entities'][i]['end']])
         vertex['type']=record['entities'][i]['type']
         innerkh.append(copy.copy(vertex))
         vertexSetSon.append(innerkh)
    
      vertexSetFather.append(vertexSetSon)
      dataElement['vertexSet']=vertexSetFather

      labelsList=[]
      for k in range((len(record['relations']))):
            labels['r']=record['relations'][k]['type']
            labels['h']=record['relations'][k]['head']
            labels['t']=record['relations'][k]['tail']
            labels['evidence']=[0]
   
            if labels['r'] in modifyMap.keys():
                labels['r']=modifyMap[labels['r']]
                print(labels['r'])
            else:
                continue
            labelsList.append(copy.copy(labels))

      dataElement['labels']=labelsList
      
      if len(labelsList)==0:
          continue
      dataList.append(dataElement)

print(len(dataList))
with open('myfile_conll4_train.json', 'w', encoding ='utf8') as json_file:
    json.dump(dataList, json_file, escape_forward_slashes=False) # ensure_ascii = False)

    