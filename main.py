# -*- coding: utf-8 -*-

## 李运辰 2021-2-18

import requests
from lxml import etree
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar
from pyecharts.charts import Pie
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',}

###饼状图
def pie(name,value,picname,tips):
    c = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(name, value)],
            # 饼图的中心（圆心）坐标，数组的第一项是横坐标，第二项是纵坐标
            # 默认设置成百分比，设置成百分比时第一项是相对于容器宽度，第二项是相对于容器高度
            center=["35%", "50%"],
        )
            .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])  # 设置颜色
            .set_global_opts(
            title_opts=opts.TitleOpts(title=""+str(tips)),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="70%", orient="vertical"),  # 调整图例位置
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render(str(picname)+".html")
    )

###柱形图
def bars(name,dict_values):

    # 链式调用
    c = (
        Bar(
            init_opts=opts.InitOpts(  # 初始配置项
                theme=ThemeType.MACARONS,
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="cubicOut"  # 初始动画延迟和缓动效果
                ))
        )
            .add_xaxis(xaxis_data=name)  # x轴
            .add_yaxis(series_name="股票型", yaxis_data=dict_values['股票型'])  # y轴
            .add_yaxis(series_name="混合型", yaxis_data=dict_values['混合型'])  # y轴
            .add_yaxis(series_name="债券型", yaxis_data=dict_values['债券型'])  # y轴
            .add_yaxis(series_name="指数型", yaxis_data=dict_values['指数型'])  # y轴
            .add_yaxis(series_name="QDII型", yaxis_data=dict_values['QDII型'])  # y轴
            .set_global_opts(
            title_opts=opts.TitleOpts(title='涨跌幅', subtitle='李运辰绘制',  # 标题配置和调整位置
                                      title_textstyle_opts=opts.TextStyleOpts(
                                          font_family='SimHei', font_size=25, font_weight='bold', color='red',
                                      ), pos_left="90%", pos_top="10",
                                      ),
            xaxis_opts=opts.AxisOpts(name='阶段', axislabel_opts=opts.LabelOpts(rotate=45)),
            # 设置x名称和Label rotate解决标签名字过长使用
            yaxis_opts=opts.AxisOpts(name='涨跌点'),

        )
            .render("基金各个阶段涨跌幅.html")
    )

###拉伸图
def silder(name,value,tips):
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
            .add_xaxis(xaxis_data=name)
            .add_yaxis(tips, yaxis_data=value)
            .set_global_opts(
            title_opts=opts.TitleOpts(title=str(tips)+"近30个交易日净值情况"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
            .render(str(tips)+"近30个交易日净值情况.html")
    )

###基金类型
dict_type={"股票型":1,"混合型":3,"债券型":2,"指数型":5,"QDII型":11}
###时间
dict_time={'近一周':'1w','近一月':'1m','近三月':'3m','近六月':'6m','近1年':'1y','近2年':'2y','近3年':'3y','近5年':'5y'}


####分析1： 近一月涨跌幅前10名
def analysis1():
    for key in dict_type:
        url = "https://danjuanapp.com/djapi/v3/filter/fund?type="+str(dict_type[key])+"&order_by=1w&size=10&page=1"
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        s = s['data']['items']
        name = []
        value = []
        for i in range(0,len(s)):
            print(s[i]['fd_name']+":"+s[i]['yield'])
            name.append(s[i]['fd_name'])
            value.append(s[i]['yield'])
        ###开始绘图
        pie(name, value, str(key)+"基金涨跌幅", "["+str(key)+"]基金近一月涨跌幅前10名")

####分析2： 基金各个阶段涨跌幅
def analysis2():
    name =['近1周','近1月','近3月','近6月','近1年','近3年','近5年']
    ##五类基金
    dict_value={}

    for key in dict_type:
        #### 获取排名第一名基金代号
        url = "https://danjuanapp.com/djapi/v3/filter/fund?type="+str(dict_type[key])+"&order_by=1w&size=10&page=1"
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        ###取第一名
        fd_code = s['data']['items'][0]['fd_code']

        #### 获取排名第一名基金各个阶段情况
        fu_url = "https://danjuanapp.com/djapi/fund/derived/"+str(fd_code)
        res = requests.get(fu_url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        data = s['data']

        valuess=[]

        ####防止基金最长时间不够1年、2年、5年的情况报错，用0填充
        ##近1周
        try:
            valuess.append(data['nav_grl1w'])
        except:
            valuess.append(0)
        ##近1月
        try:
            valuess.append(data['nav_grl1m'])
        except:
            valuess.append(0)
        ##近3月
        try:
            valuess.append(data['nav_grl3m'])
        except:
            valuess.append(0)
        ##近6月
        try:
            valuess.append(data['nav_grl6m'])
        except:
            valuess.append(0)
        ##近1年
        try:
            valuess.append(data['nav_grl1y'])
        except:
            valuess.append(0)
        ##近3年
        try:
            valuess.append(data['nav_grl3y'])
        except:
            valuess.append(0)
        ##近5年
        try:
            valuess.append(data['nav_grl5y'])
        except:
            valuess.append(0)
        ###添加到集合中
        dict_value[key]=valuess
    bars(name,dict_value)

####分析3： 近30个交易日净值情况
def analysis3():
    for key in dict_type:
        #### 获取排名第一名基金代号
        url = "https://danjuanapp.com/djapi/v3/filter/fund?type=" + str(
            dict_type[key]) + "&order_by=1w&size=10&page=1"
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        ###取第一名
        fd_code = s['data']['items'][0]['fd_code']

        #### 获取排名第一名基金近30个交易日净值情况
        fu_url = "https://danjuanapp.com/djapi/fund/nav/history/"+str(fd_code)+"?size=30&page=1"
        res = requests.get(fu_url, headers=headers)
        res.encoding = 'utf-8'
        s = json.loads(res.text)
        data = s['data']['items']
        name=[]
        value=[]
        for k in range(0,len(data)):
            name.append(data[k]['date'])
            value.append(data[k]['nav'])

        silder(name, value,key)

#name =['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
#value=[34,42,12,37,76,11,13,53,42,23,43,64,67,22,41]
####分析1： 近一月涨跌幅前10名
#analysis1()
####分析2：基金各个阶段涨跌幅
#analysis2()
####分析3：近30个交易日净值情况
analysis3()




# c = (
#     Bar()
#     .add_xaxis(
#         [
#             "名字很长的X轴标签1",
#             "名字很长的X轴标签2",
#             "名字很长的X轴标签3",
#             "名字很长的X轴标签4",
#             "名字很长的X轴标签5",
#             "名字很长的X轴标签6",
#         ]
#     )
#     .add_yaxis("商家A", v1)
#     .add_yaxis("商家B", v2)
#     .add_yaxis("商家C", v3)
#     .add_yaxis("商家D", v4)
#     .add_yaxis("商家E", v5)
#     #全局配置项
#     .set_global_opts(
#         #设置x轴  （轴标签旋转-15度（顺时针））
#         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
#         #标题配置项
#         title_opts=opts.TitleOpts(title="Bar-旋转X轴标签", subtitle="解决标签名字过长的问题"),
#     )
#     .render("4.html")
# )



