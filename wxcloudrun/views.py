
from datetime import datetime
from flask import render_template, request,Flask
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import pkuseg
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
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
    "key": (None,"visualization/"+courseid+".jpg"),
    "Signature": (None,response.json()['authorization']),
    'x-cos-security-token': (None,response.json()['token']),
    'x-cos-meta-fileid': (None,response.json()['cos_file_id']),
    'file': ('visualization.jpg',open(r"/app/wxcloudrun/visualization.jpg","rb"))
  }
  #data2 = json.dumps(data2)
  response2 = requests.post(response.json()['url'], files=data2,verify=False)
  return response.json()["file_id"]

@app.route('/', methods=['POST'])
def upload():

    courseid = request.json.get('courseid')
    file = request.json.get('comdata')
    json_data = file
    
    fig = Figure(dpi = 100)
    label=['完全明白', '一般般', '不大好', '完全听不懂']
    values=[json_data['完全明白'], json_data['一般般'], json_data['不大好'], json_data['完全听不懂']]
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    pie = ax.pie(values,labels=label,autopct='%1.1f%%')

    #图形中的文字无法通过rcParams设置
    for font in pie[1]:
        font.set_fontproperties(mpl.font_manager.FontProperties(
            fname='/app/wxcloudrun/华文楷体.ttf'))
    path = r'E:\竞赛数据集\设计大赛\1.jpg'
    fig.savefig(path)

    fig = Figure(dpi = 100)
    label=['踩', '赞']
    values=[json_data['踩'], json_data['赞']]
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    pie = ax.pie(values,labels=label,autopct='%1.1f%%')
    #图形中的文字无法通过rcParams设置
    for font in pie[1]:
        font.set_fontproperties(mpl.font_manager.FontProperties(
            fname='/app/wxcloudrun/华文楷体.ttf'))
    
#     plt.figure(figsize=(10,10))#将画布设定为正方形，则绘制的饼图是正圆
#     fig1 = plt.subplot(121)
#     label=['Totally understand','So-so','Not good',"don't understand"]#定义饼图的标签，标签是列表
#     explode=[0.01, 0.01, 0.01, 0.01]#设定各项距离圆心n个半径
#     values=[json_data['完全明白'], json_data['一般般'], json_data['不大好'], json_data['完全听不懂']]
#     plt.pie(values,explode=explode,labels=label,autopct='%1.1f%%')#绘制饼图
#     plt.title('Student voting in this course 1')

#     fig2 = plt.subplot(122)
#     label=['bad', 'good']#定义饼图的标签，标签是列表
#     explode=[0.01, 0.01]#设定各项距离圆心n个半径
#     values=[json_data['踩'], json_data['赞']]
#     plt.pie(values,explode=explode,labels=label,autopct='%3.1f%%')#绘制饼图
#     plt.title('Student voting in this course 2')
#     plt.savefig('/app/wxcloudrun/visualization.jpg')
    fig.savefig('/app/wxcloudrun/visualization.jpg')
    a = duixiangcunchu(courseid)
    b = {"re":a}
    c = json.dumps(b)
    return c
    
