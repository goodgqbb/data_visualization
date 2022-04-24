from datetime import datetime
from flask import render_template, request,Flask
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import pkuseg
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from imageio import imread
import  os
import jieba
import json
import requests

def duixiangcunchu(courseid):
  #获取token
  response = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxfb2997f507abf89e&secret=168726b557fb7221c96955cec59b3347',verify=False)
  data ={
    "env": "prod-0gayxkvve034fe60",
    "path": "visualization/"+courseid+".jpg"
  }
  #return str(response.json())
  #转json
  data = json.dumps(data)
  response = requests.post("https://api.weixin.qq.com/tcb/uploadfile?access_token="+response.json()['access_token'],data,verify=False)
  print(response.json())
  #response = json.loads(response.json())
  #得到上传链接

  data2={
    "Content-Type":(None,".jpg"),
    "key": (None,"ciyunimage/"+courseid+".jpg"),
    "Signature": (None,response.json()['authorization']),
    'x-cos-security-token': (None,response.json()['token']),
    'x-cos-meta-fileid': (None,response.json()['cos_file_id']),
    'file': ('ciyun.jpg',open(r"/app/wxcloudrun/visualization.jpg","rb"))
  }
  #data2 = json.dumps(data2)
  response2 = requests.post(response.json()['url'], files=data2,verify=False)
  return response.json()["file_id"]

@app.route('/', methods=['POST'])
def upload():
    courseid = request.json.get('courseid')
    file = request.json.get('comdata')
    json_data = file
    plt.rcParams['font.sans-serif']='SimHei'#设置中文显示
    plt.figure(figsize=(10,10))#将画布设定为正方形，则绘制的饼图是正圆
    fig1 = plt.subplot(121)
    label=['完全明白', '一般般', '不大好', '完全听不懂']#定义饼图的标签，标签是列表
    explode=[0.01, 0.01, 0.01, 0.01]#设定各项距离圆心n个半径
    values=[json_data['完全明白'], json_data['一般般'], json_data['不大好'], json_data['完全听不懂']]
    plt.pie(values,explode=explode,labels=label,autopct='%1.1f%%')#绘制饼图
    plt.title('本次课程学生投票情况1')

    fig2 = plt.subplot(122)
    label=['踩', '赞']#定义饼图的标签，标签是列表
    explode=[0.01, 0.01]#设定各项距离圆心n个半径
    values=[json_data['踩'], json_data['赞']]
    plt.pie(values,explode=explode,labels=label,autopct='%3.1f%%')#绘制饼图
    plt.title('本次课程学生投票情况2')
    plt.save('/app/wxcloudrun/visualization.jpg')
    a = duixiangcunchu(courseid)
    b = {"re":a}
    c = json.dumps(b)
    return c
    
