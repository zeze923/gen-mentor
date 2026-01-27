import streamlit as st
from streamlit_float import *
from utils.request_api import chat_with_tutor
from utils.state import index_goal_by_id


@st.dialog("🤖 询问导师")
def ask_autor_chatbot():
    instruction = "👋 你好！我是您的个人学习导师 🎯。今天我能如何帮助您实现学习目标？"
    st.info(instruction)
    
    # 初始化 tutor_messages
    if "tutor_messages" not in st.session_state:
        st.session_state["tutor_messages"] = []
    
    if index_goal_by_id(st.session_state["selected_goal_id"]) == None:
        goal = st.session_state["to_add_goal"]
    else:
        goal = st.session_state["goals"][st.session_state["selected_goal_id"]]
    learner_profile = goal.get("learner_profile", {})

    # 创建消息容器
    messages = st.container(height=300)
    
    # 显示历史消息
    with messages:
        for msg in st.session_state["tutor_messages"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
    
    # 聊天输入
    if prompt := st.chat_input("问我任何问题"):
        # 添加用户消息
        st.session_state["tutor_messages"].append({"role": "user", "content": prompt})
        
        # 获取助手回复
        try:
            with st.spinner("正在思考..."):
                response = chat_with_tutor(
                    st.session_state["tutor_messages"][-20:], 
                    learner_profile,
                    st.session_state["llm_type"])
            
            if response:
                st.session_state["tutor_messages"].append({"role": "assistant", "content": response})
            else:
                error_msg = "抱歉，我现在无法回答。请稍后再试。"
                st.session_state["tutor_messages"].append({"role": "assistant", "content": error_msg})
        except Exception as e:
            error_msg = f"抱歉，发生了错误：{str(e)}"
            st.session_state["tutor_messages"].append({"role": "assistant", "content": error_msg})
        
        # 重新运行以显示新消息
        st.rerun()

def click_chatbot_func():
    ask_autor_chatbot()


def render_chatbot():
    float_init()

    button_container = st.container()
    with button_container:
        if_open_chatbot = st.button("询问导师", type="primary", key="chatbot", icon="🤖", on_click=click_chatbot_func)
        if if_open_chatbot:
            st.session_state.show_chatbot = True

    button_css = float_css_helper(width="8rem", right="2rem", bottom="4rem", transition=0)
    button_container.float(button_css)