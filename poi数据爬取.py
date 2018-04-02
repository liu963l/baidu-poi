# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 10:31:28 2018

@author: Liu-pc
"""






import pandas as pd
import urllib2  
import json 
#from pymongo import MongoClient



##设置网格区域
origin_gps = [39.930577,116.42405,39.955221,116.439393]  #要抓取的总范围,左下角-右上角（东四-东直门）


#在这个大范围里分割小区域

def split_area(origin_gps, lon_number, lat_number):
    l = []
    lat_gap = (origin_gps[2] - origin_gps[0])/lat_number
    lon_gap = (origin_gps[3] - origin_gps[1])/lon_number
    
    lat_list = [origin_gps[0]]
    for i in range(1,lat_number+1):
        lat_list.append(lat_list[0] + lat_gap*i)
    
    lon_list = [origin_gps[1]]
    for i in range(1,lon_number+1):
        lon_list.append(lon_list[0] + lon_gap*i)
    #print lon_list  
    #print lat_list    
    for i in range(len(lon_list)-1):
        for j in range(1,len(lat_list)):
            l.append([lat_list[j-1],lon_list[i], lat_list[j],lon_list[i + 1]])
    return l

lon_lat_list = split_area(origin_gps, 2,3)
#获取每个区域经纬度对角线列表


#获取url列表

def url_list(lon_lat, class_area, long_):
    #long 表示多少页
    #获取每个区域的url
    url = []
    for i in lon_lat:
        for j in range(long_):
            url.append( 'http://api.map.baidu.com/place/v2/search?query='+ class_area +'&scope=2' + '&bounds=' + str(i[0]) +','+ str(i[1])+',' +str(i[2])+','+ str(i[3])+ '&output=json&ak=Y99rGAE4gQXyG0SOchBMqSoyTadxIDR9&page_size=20' + '&page_num='+str(j))
            #url.append( 'http://api.map.baidu.com/place/v2/search?query='+ class_area +'&scope=2'+ 'region=北京'+ '&output=json&ak=Y99rGAE4gQXyG0SOchBMqSoyTadxIDR9&page_size=1' + '&page_num='+str(j))
    return url

url = url_list(lon_lat_list , '丽人', 5)
#因为每个区域内的数据量最多不超过某一值，需要设置一个合理的页数这样才能够抓取全部数据
#得到的是一个url列表，每个url最多包含20条数据，每个区域设置为5页

'''
#获取全北京的
def url_list(lon_lat, class_area, long_):
    #long 表示多少页
    #获取每个区域的url
    url = []
   
    for j in range(long_):
            #url.append( 'http://api.map.baidu.com/place/v2/search?query='+ class_area +'&scope=2' + '&bounds=' + str(i[0]) +','+ str(i[1])+',' +str(i[2])+','+ str(i[3])+ '&output=json&ak=Y99rGAE4gQXyG0SOchBMqSoyTadxIDR9&page_size=1' + '&page_num='+str(j))
        url.append( 'http://api.map.baidu.com/place/v2/search?query='+ class_area +'&scope=2'+ '&region=北京'+ '&output=json&ak=Y99rGAE4gQXyG0SOchBMqSoyTadxIDR9&page_size=1' + '&page_num='+str(j))
    return url
url = url_list(lon_lat_list , '丽人', 500)
'''



place = ['美食', '酒店', '购物', '生活服务', '丽人', '旅游景点','休闲娱乐','运动健身',
         '教育培训', '文化传媒', '医疗', '汽车服务','交通设施', '金融','房地产', '公司企业'
         '政府机构','出入口', '自然地物']


url = []
for i in place:
    url = url + url_list(lon_lat_list, i, 1)
    
#这个url是全部place的url，在origin_gps这个范围内的
    

#编写抓取数据函数
def get_data(url):
    address = []
    area = []
    city = []
    province = []
    name = []
    lon = []
    lat = []
    type_ = []
    tag = []
    comment_num = []
    street_id = []
    data1 = pd.DataFrame()
    for j in range(len(url)):
        data = urllib2.urlopen(url[j])
        hjson = json.loads(data.read());
        if hjson['message'] == 'ok' :
            results = hjson['results']
            print j
            if results != []:
                for i in range(len(results)):
                    if 'address' in results[i].keys():
                        address.append(results[i][u'address'])
                    else:
                        address.append(0)
                    if 'area' in  results[i].keys():
                        area.append(results[i][u'area'])
                    else:
                        area.append(0)
                    if 'city' in results[i].keys():
                        city.append(results[i][u'city'])
                    else:
                        city.append(0)
                    if 'province' in results[i].keys():
                        province.append(results[i][u'province'])
                    else:
                        province.append(0)
                    if 'name' in  results[i].keys():
                        name.append(results[i]['name'])
                    else :
                        name.append(0)
                    
                    lon.append(results[i]['location']['lng'])
                    lat.append(results[i]['location']['lat'])
                    if 'detail_info' in results[i].keys():
                        if 'type' in results[i]['detail_info'].keys():
                            type_.append(results[i]['detail_info']['type'])
                        else:
                            type_.append(0)
                        if 'tag' in results[i]['detail_info'].keys():
                            tag.append(results[i]['detail_info']['tag'])
                        else :
                            tag.append(0)
                        if 'comment_num' in results[i]['detail_info'].keys():
                            comment_num.append(results[i]['detail_info']['comment_num'])
                        else:
                            comment_num.append(0)
                    else:
                        type_.append(0)
                        tag.append(0)
                        comment_num.append(0)
                    if 'street_id' in results[i].keys():
                        street_id.append(results[i]['street_id'])
                    else :
                         street_id.append(0)
                   
            else:
                continue
        else:
            print '%s is error url' %j
            continue
    data1 = pd.DataFrame({'address':address,'area':area,'city': city,'province':province,'name':name, 'lon':lon,'lat':lat, 'type': type_, 
                          'tag':tag, 'street_id':street_id, 'comment_num':comment_num})
    return data1



data = get_data(url)



'''
#测试数据
url = 'http://api.map.baidu.com/place/v2/search?query=美食&scope=2&bounds=39.930577,116.42405,39.9336575,116.4271186&output=json&ak=Y99rGAE4gQXyG0SOchBMqSoyTadxIDR9'

data = urllib2.urlopen(url)
hjson = json.loads(data.read());
if hjson['message'] == 'ok':
    results = hjson['results']         


'''



















