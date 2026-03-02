#%%
import streamlit_核心功能 as st
import pandas as pd

st.write("Hello World")
# table = pd.DataFrame(
#     {
#         "name": ["胡桃", "芙宁娜", "甘雨", "纳西妲", "刻晴"],
#         "age": [16,20,21,18,19]
#     }
#  )
# st.write(table)
# slider_num = st.slider("num")
# st.write(slider_num)
# username = st.text_input("username")
# st.write(f"欢迎~{username}")
# st.write("密码是520")
#
# # 创建一个文本输入框，并将其类型设置为密码
# password = st.text_input("请输入密码", type="password")
#
# # 检查密码是否正确
# if st.button("登录"):
#     if password == "520" and username == "小棉花糖":
#         st.success("登录成功！")
#     else:
#         st.error("用户名或密码错误，请重试。")
#
# #返回值为选中的内容信息
# option = st.selectbox(
#     label='请选择省份信息：',
#     options=['河北','山东','河南','吉林']
# )
# st.write("您选择的是: ", option)
#
# # columns参数表示列数
# left_column, right_column = st.columns(2)
# # 左边列设置
# with left_column:
#     # 返回值为选中的选项值
#     chosen = st.radio(
#         label='电脑品牌',
#         options=('苹果', '华为', '小米')
#     )
#     st.write(f'你选择的品牌是: {chosen}')
#
# # 右边列设置
# with right_column:
#     # 返回值为选中的选项值
#     chosen = st.radio(
#         label='操作系统',
#         options=('苹果', '华为鸿蒙', '安卓')
#     )
#     st.write(f'你选择的手机操作系统是: {chosen}')

import time
st.write("模拟长时间的计算...")

# 创建一个动态显示数据的容器，用于动态显示进度条的进度数值
value = st.empty()
#创建进度条，进度条初始值为0
bar = st.progress(0)
for i in range(100):
    #这是动态显示的数值
    value.text(f'已加载 {i+1}%')
    # 更新进度条
    bar.progress(i+1)
    time.sleep(0.1)
st.write('运行结束!')


"""
侧边栏sidebar
下拉框
并排布局
选项卡布局
折叠布局
"""
