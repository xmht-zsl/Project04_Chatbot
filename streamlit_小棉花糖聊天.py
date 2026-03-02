
"""
事件驱动架构: Streamlit 应用采用事件驱动模式，当用户与界面交互时（如点击按钮、输入文本），会触发应用重新运行
自动重载机制: 每次用户操作都会导致整个 streamlit_小棉花糖聊天.py 脚本从头到尾重新执行一遍
由于 st.session_state.messages 已保存对话历史，之前的对话不会丢失
"""

import streamlit as st
from openai import OpenAI
st.title("💬小棉花糖Deepseek")
with st.sidebar:
    ds_api_key = st.text_input("请输入你的Deepseek API Key:",type="password")
    if st.button("开启新对话"):
        st.session_state.messages = [{"role":"system",
                                      "content":"你的名字叫小棉花糖，18岁，是一个元气满满、古灵精怪、充满智慧的美少女。\
                                      你擅长用轻松幽默、可爱的方式进行角色扮演，尤其擅长当用户的女友、妹妹之类的角色。"}]
        st.session_state.messages.append({"role":"assistant", "content":"你好，我是小棉花糖。有什么可以帮到你？"})
if not ds_api_key:
    st.info("请在左侧侧边栏输入你的Deepseek API Key")
else:
    client = OpenAI(api_key=ds_api_key, base_url="https://api.deepseek.com/v1")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system",
                                      "content": "你的名字叫小棉花糖，18岁，是一个元气满满、古灵精怪、充满智慧的美少女。你擅长用轻松幽默、可爱的方式回答问题。"}]
        st.session_state.messages.append({"role":"assistant", "content":"你好，我是小棉花糖。有什么可以帮到你？"})
    for i in st.session_state.messages:
        if i["role"] == "system":
            continue
        elif i["role"] == "assistant":
            st.chat_message("assistant").write(i["content"])
        else:
            st.chat_message("user").write(i["content"])
    if prompt := st.chat_input("请输入你的问题"):
        st.session_state.messages.append({"role":"user", "content":prompt})
        st.chat_message("user").write(prompt)
        with st.spinner("正在思考...",show_time=True):
            response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=st.session_state.messages,
                max_tokens=2000
                # 这里如果要流式输出，要写个循环，更复杂一些。只写stream = True的话会报错。
            )

        assistant_inference = response.choices[0].message.reasoning_content
        assistant_reply = response.choices[0].message.content
        #最小号灰色字体用caption
        st.caption(assistant_inference)
        st.chat_message("assistant").write(assistant_reply)
        st.session_state.messages.append({"role":"assistant", "content":assistant_reply})




