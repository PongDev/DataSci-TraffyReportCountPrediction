import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime
import pickle
from geopy.geocoders import Nominatim
def fetchData():
  url = 'https://publicapi.traffy.in.th/share/teamchadchart/search'
  df = pd.DataFrame(columns = ['type', 'org', 'description', 'ticket_id', 'coords', 'photo_url', 'after_photo', 'address', 'timestamp', 'problem_type_abdul', 'star', 'count_reopen', 'note', 'state', 'last_activity'])
  offset=0
  now = datetime.now()
  start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
  start_of_yesterday = start_of_day.replace(day = start_of_day.day-1)
  while True:
    try:
      response_API =requests.get(url+f'?offset={offset}')
      data = response_API.text
      parse_json = json.loads(data)
      offset+=len(parse_json['results'])
      new_data = pd.DataFrame(parse_json['results'])
      new_data = new_data[new_data['timestamp'].apply(lambda x: np.datetime64(x[:-3])<start_of_day and np.datetime64(x[:-3])>=start_of_yesterday)]
      if new_data.shape[0] == 0 :break
      df = pd.concat([df,new_data],ignore_index=True)
    except:
      print(f'error occured at offset={offset}')

  df = df.drop(columns=['type','org','ticket_id','photo_url','after_photo','star','count_reopen','note','state','last_activity'])
  df = df.loc[np.vectorize(lambda x: x[0]!='')(df['problem_type_abdul'])] 
  df = df.dropna(axis=0,subset=['description','address'])
  district_list = ['พระนคร', 'ดุสิต', 'หนองจอก', 'บางรัก', 'บางเขน', 'บางกะปิ', 'ปทุมวัน', 'ป้อมปราบศัตรูพ่าย', 'พระโขนง', 'มีนบุรี', 'ลาดกระบัง', 'ยานนาวา', 'สัมพันธวงศ์', 'พญาไท', 'ธนบุรี',
  'บางกอกใหญ่', 'ห้วยขวาง', 'คลองสาน', 'ตลิ่งชัน', 'บางกอกน้อย', 'บางขุนเทียน', 'ภาษีเจริญ', 'หนองแขม', 'ราษฎร์บูรณะ', 'บางพลัด', 'ดินแดง', 'บึงกุ่ม', 'สาทร', 'บางซื่อ', 'จตุจักร', 'บางคอแหลม',
  'ประเวศ', 'คลองเตย', 'สวนหลวง', 'จอมทอง', 'ดอนเมือง', 'ราชเทวี', 'ลาดพร้าว', 'วัฒนา', 'บางแค', 'หลักสี่', 'สายไหม', 'คันนายาว', 'สะพานสูง', 'วังทองหลาง', 'คลองสามวา', 'บางนา', 'ทวีวัฒนา',
  'ทุ่งครุ', 'บางบอน']
  with open ('kwaeng.pkl','rb') as kwaeng_file:
      kwaeng_to_khet = pickle.load(kwaeng_file)

  def calc_district(address,coords):
    address = address.split('เขต')[-1].strip()
    district = address.split('กรุงเทพ')[0].strip()
    if district in district_list:
      return district
    kw = calc_disc_from_sub(address)
    if kw in kwaeng_to_khet:
      district = kwaeng_to_khet[kw]
      return district
    else:
      return None
      # return coords_to_district(coords)

  def calc_disc_from_sub(address):
      x = address.find('แขวง')
      if x == -1: return 'NF'
      y = address.find(' ', x)
      if y == x + 4:
          z = address.find(' ', y+1)
          return address[y:z].strip()
      return address[x+4:y].strip()
  def coords_to_district(coords):
    geolocator = Nominatim(user_agent="http")
    # location = geolocator.reverse(eval(coords)[::-1])
    location = geolocator.reverse(coords[::-1])
    if location is None:
        return
    if 'suburb' in location.raw['address']:
      district = location.raw['address']['suburb']
      if 'เขต'in district: district = district[3:]
      if district in district_list:
        return district
      return 
    if 'county' in location.raw['address']:
      district = location.raw['address']['county']
      if 'เขต' in district: district = district[3:]
      if district in district_list:
        return district
      return 
    return 
  df.loc[:,'district'] = df.apply(lambda x: calc_district(x['address'],x['coords']),axis=1)
  for i in df[df['district'].isna()].index:
      try:
          df.loc[i,'district'] = coords_to_district(df.loc[i,'coords'])
      except Exception as e:
          print('sth went wrong')
  df = df.dropna(axis=0,subset=['district'])
  df.loc[:,'date'] = df['timestamp'].apply(lambda x: x.split()[0])
  df.loc[:,'temp'] = df['description']+df['address']
  df = df.drop_duplicates(subset='temp')
  df = df.drop(columns=['description','coords','address','temp','timestamp'])
  df = df.explode('problem_type_abdul')
  df['count'] = 1
  df=df.groupby(['date','district','problem_type_abdul']).sum().reset_index()

  relavent_type = ['กีดขวาง','คลอง','ความปลอดภัย','ความสะอาด','จราจร','ต้นไม้','ถนน','ทางเท้า','ท่อระบายน้ำ','น้ำท่วม','สะพาน','สายไฟ','แสงสว่าง']
  khets = set(kwaeng_to_khet.values())
  khets = list(khets)
  region_to_dist = {'กรุงธนเหนือ': ['ธนบุรี','จอมทอง','บางกอกใหญ่','คลองสาน','บางกอกน้อย','บางพลัด','ทวีวัฒนา','ตลิ่งชัน'],
                    'กรุงเทพกลาง': ['สัมพันธวงศ์','ดุสิต','พระนคร','ป้อมปราบศัตรูพ่าย','พญาไท','ราชเทวี','ดินแดง','วังทองหลาง','ห้วยขวาง'],
                    'กรุงธนใต้': ['ภาษีเจริญ','บางแค','หนองแขม','ราษฎร์บูรณะ','ทุ่งครุ','บางขุนเทียน','บางบอน'],
                    'กรุงเทพตะวันออก':['บึงกุ่ม','บางกะปิ','คันนายาว','สะพานสูง','หนองจอก','ลาดกระบัง','มีนบุรี','คลองสามวา','ประเวศ'],
                    'กรุงเทพใต้':['คลองเตย','บางคอแหลม','ปทุมวัน','บางรัก','สาทร','ยานนาวา','วัฒนา','บางนา','พระโขนง','สวนหลวง'],
                    'กรุงเทพเหนือ': ['ลาดพร้าว','หลักสี่','จตุจักร','บางซื่อ','สายไหม','บางเขน','ดอนเมือง']
                    }
  dist_to_region = {}
  for key in region_to_dist:
    for district in region_to_dist[key]:
      dist_to_region[district] = key
  df['region'] = df['district'].apply(dist_to_region.get)
  dfs=[]
  for reg in region_to_dist.keys():
    df_r = df[(df['region']==reg) & (df['problem_type_abdul'].isin(relavent_type))].groupby(['date','problem_type_abdul'])['count'].sum().reset_index().pivot(index='date',columns='problem_type_abdul',values='count').fillna(0)
    for t in relavent_type:
      if t not in df_r.columns:
        df_r[t]=0
    df_r['region']=reg
    dfs.append(df_r)
  df = pd.concat(dfs)
  df=df.sort_values('date')
  df = df.reset_index()
  df = df.rename_axis(None, axis=1)
  df = df.rename(columns={'กีดขวาง':'obstacle','คลอง':'canal',	'ความปลอดภัย':'security',	'ความสะอาด':'sanitary',	'จราจร':'traffic',	'ต้นไม้':'tree'	,'ถนน':'road',	'ทางเท้า':'sidewalk',	'ท่อระบายน้ำ':'sewer',	'น้ำท่วม':'flood',	'สะพาน':'bridge',	'สายไฟ':'electricWire',	'แสงสว่าง':'light'})
  return df.to_json(orient="records")