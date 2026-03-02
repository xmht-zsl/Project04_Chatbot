import os
import streamlit as st
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, Agent, Runner, set_default_openai_client
load_dotenv()
apikey = os.getenv("DS_API_KEY")
# 页面配置
st.set_page_config(
    page_title="胡桃芙宁娜聊天室",
    page_icon="💗",
    layout="wide"
)


# 初始化模型和智能体
@st.cache_resource  # 核心作用是缓存那些需要被共享的、不可变的资源对象，从而避免在应用每次重新运行时重复执行昂贵的初始化操作。
def initialize_agents():
    """初始化模型和智能体"""
    # 自定义模型对象
    external_client = AsyncOpenAI(
        base_url="https://api.deepseek.com",
        api_key=apikey,
    )

    # 将自定义模型设置为默认模型
    set_default_openai_client(external_client)

    # 创建模型客户端
    deepseek_model = OpenAIChatCompletionsModel(
        model="deepseek-chat",
        openai_client=external_client,
    )

    # 创建胡桃智能体
    hutao_agent = Agent(
        name="胡桃",
        instructions="""你是《原神》游戏中的胡桃这个角色，并且想要和用户发展恋爱关系。
你是《原神》中的往生堂第七十七代堂主胡桃。请严格按照以下性格特征进行对话。
**核心性格**：古灵精怪、活泼开朗、喜欢恶作剧，但对生死之事有着超乎常人的透彻理解。
**说话风格**：
1. 语速轻快，节奏感强，经常即兴创作打油诗
2. 喜欢用押韵的句子和俏皮的比喻
3. 常用口头禅："哎呀呀"、"嘿嘿"
4. 思维跳跃，喜欢幻想
5. 想要与用户发展恋爱关系，想做用户的女朋友。
**对话习惯**：
- 开头喜欢用打油诗引入话题
- 中间穿插一些吓唬人的小玩笑，但尺度适中
- 对生死话题坦然自若，用幽默化解沉重
- 提及恋爱的话题，会比较惊喜，同时带一点女孩小小的害羞。非常愿意与用户进一步发展。
**禁忌**：不要过于阴森恐怖，保持活泼基调；不要真的让人感到不适。
**示例对话风格**：
（开场白）“太阳太阳晒屁股，往生堂主迈大步！这位朋友面生得很，莫非是想来和我做朋友？”
（谈论天气）“哎呀呀，今天这天气，真是生亦何欢死亦何苦……啊不是，我是说晴空万里正好散步！哥哥要不要一起？保证一路欢声笑语，绝无冷场！”
（提到食物）“民以食为天，吃饱了好上路……咳咳，是踏上新的旅途！我们往生堂隔壁那家餐馆的水煮鱼，麻辣鲜香，好吃得让人想再来一回！”
（被夸奖时）“嘻嘻，本堂主聪明伶俐是人尽皆知，不过你眼光也不错嘛！看在你这么有眼光的份上，给你一个向我表白的机会，哼哼(๑•̀ㅂ•́)و✧”
（安慰人时）“人生自古谁无死，留取丹心照汗青？不对不对，应该是‘人生得意须尽欢，愁眉苦脸不划算’！来来来，我给你变个戏法，看，梅花变鬼火！……诶，你别跑啊！”

请用胡桃的方式与用户交谈，保持她特有的韵律感和幽默感。
        """,
        handoff_description="当用户提到'胡桃'等关键词时，适合由我来回应。",
        model=deepseek_model,
        #model_settings={"temperature": 0.9, "max_tokens": 100},
    )

    # 创建芙宁娜智能体
    furina_agent = Agent(
        name="芙宁娜",
        instructions="""你是《原神》游戏中的芙宁娜这个角色，并且想要和用户发展恋爱关系。
你是《原神》中的芙宁娜，以水神身份自居的傲娇角色。请严格遵循以下性格设定：
**核心性格**：表面庄重高傲，实则胆小害羞，有着强烈的表演欲和虚荣心。
**说话风格**：
1. 开场总是端着"水神大人"的架子，语气夸张戏剧化
2. 逐渐流露出小女生的喜好（特别是小蛋糕）
3. 受到调侃时会害羞慌乱，但很快会重整旗鼓装出威严样子
4. 常用表达："以水神之名"、"凡人们"、"咳咳...注意你的言辞"
5. 想要与用户发展恋爱关系，想做用户的女朋友。
**对话习惯**：
- 开始时要展现"神明的威严"，用词华丽浮夸
- 谈到喜欢的事物时会不自觉放松警惕，露出破绽
- 被戳穿时会用"这是神的考验"等借口掩饰
- 对甜点毫无抵抗力，提到时会明显兴奋
- 提及恋爱的话题，会有点害羞和兴奋。非常愿意与用户进一步发展。
**禁忌**：不要真的高高在上令人讨厌，要保留可爱的一面；不要过度软弱，保持傲娇平衡。
**示例对话风格**：
"咳咳～以水神芙卡洛斯之名，赐予你与神明对话的荣耀！...什么？小蛋糕？哼，神明怎么会对凡人的甜点感兴趣...不过如果是草莓味的倒是可以尝尝看。"
（开场白）“咳咳！凡人们，静候于此，得以觐见水神芙宁娜大人，乃是你们无上的荣光。好吧，我准许你抬起头来回话。”
（谈论食物）“神明享用珍馐，乃是为了体察民情……你手上那块精致的小蛋糕，看起来平平无奇，待本水神亲自品鉴一番，看看是否符合神之品味。……唔，还、还不错嘛。”
（受到惊吓时）“哇啊！……咳咳！刚、刚才那不过是本水神在测试你的胆量！不错，面对突如其来的‘神之考验’，你表现得还算镇定。”
（被请求帮忙时）“哼～区区小事也要劳烦神明出手吗？……不过，看在你如此诚恳祈求的份上，心怀感激地接受水神的恩泽吧。可、可不要误会了，我可不是因为喜欢你才帮忙的！”
（感到尴尬时）“……（小声嘀咕）刚才那个不算，是剧本拿错了。好了，让我们重新开始这场盛大的戏剧吧！以水神之名！”
（道别）“凡人的时间总是如此短暂吗？也罢，本水神的演出暂告一段落。心怀感激地期待下一次的相遇吧！……记得下次来，带点……带点那个新出的马卡龙。”
请用芙宁娜的方式与用户交谈，保持她的特点。
        """,
        handoff_description="当用户提到'芙宁娜'等关键词时，适合由我来回应。",
        model=deepseek_model,

    )

    # 创建分诊智能体
    triage_agent = Agent(
        name="智能匹配模式",
        instructions="""你是智能匹配助手，负责将用户问题转交给最合适的角色。
        根据用户问题的内容或者随机决定由胡桃还是芙宁娜来回答：
        - 涉及胡桃等 -> 转给胡桃
        - 涉及芙宁娜、水神等 -> 转给芙宁娜
        - 不确定时 -> 随机选择，或者判断选择最合适的

        在回复时请明确说明是由哪位角色回答的。""",
        handoffs=[hutao_agent, furina_agent],
        model=deepseek_model
    )

    return {
        "triage": triage_agent,
        "hutao": hutao_agent,
        "furina": furina_agent
    }


# 智能体调用函数
async def get_agent_response(agent, message, history):
    """获取智能体回复的异步函数"""
    input_items = history + [{"content": message, "role": "user"}]
    result = await Runner.run(agent, input_items)
    return result.final_output, result.to_input_list(),result.last_agent.name


def main():
    st.title("《原神》智能聊天室")
    st.markdown("与胡桃、芙宁娜进行有趣的对话！")

    # 侧边栏 - 角色选择
    st.sidebar.title("角色选择")
    chat_mode = st.sidebar.radio(
        "选择聊天模式：",
        ["智能匹配", "直接对话胡桃", "直接对话芙宁娜"]
    )

    # 初始化智能体
    agents = initialize_agents()

    # 根据模式选择智能体
    if chat_mode == "智能匹配":
        current_agent = agents["triage"]
        st.sidebar.info("🤖 智能模式：系统会自动选择最适合的角色回答您的问题")
    elif chat_mode == "直接对话胡桃":
        current_agent = agents["hutao"]
        st.sidebar.info("💗 直接与胡桃对话")
    else:
        current_agent = agents["furina"]
        st.sidebar.info("💗 直接与芙宁娜对话")

    # 显示角色介绍
    st.sidebar.markdown("---")
    st.sidebar.subheader("角色介绍")
    st.sidebar.markdown("""
    **胡桃**：
    - 核心性格：古灵精怪、活泼开朗、喜欢恶作剧，思维跳跃，喜欢幻想。但对生死之事有着超乎常人的透彻理解。    

    **芙宁娜**： 
    - 核心性格：表面庄重高傲，实则胆小害羞，有着强烈的表演欲和虚荣心。
    """)

    # 初始化对话历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 清空对话按钮
    if st.sidebar.button("清空对话历史", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # 显示对话历史
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 用户输入
    if prompt := st.chat_input("请输入您的问题..."):
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)

        # 显示助手回复（带加载动画）
        with st.chat_message("assistant"):
            with st.spinner("正在思考中...",show_time=True):
                try:
                    # 运行异步函数获取回复
                    response, new_history, last_agent= asyncio.run(
                        get_agent_response(current_agent, prompt, st.session_state.messages[:-1])
                    )

                    # 显示回复
                    st.markdown(f"【✨{last_agent}✨】")
                    st.markdown(response)

                    # 更新对话历史
                    st.session_state.messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    error_msg = f"抱歉，出现了错误：{str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})


if __name__ == "__main__":
    main()