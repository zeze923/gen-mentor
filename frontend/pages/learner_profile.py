import math
import streamlit as st
from utils.request_api import create_learner_profile, update_learner_profile
from components.skill_info import render_skill_info
from components.navigation import render_navigation
from utils.pdf import extract_text_from_pdf
from streamlit_extras.tags import tagger_component 
from utils.state import save_persistent_state


def render_learner_profile():
    # Title and introduction
    goal = st.session_state["goals"][st.session_state["selected_goal_id"]]

    st.title("学习者档案")
    st.write("学习者的背景、目标、进度、偏好和行为模式概览。")
    if not goal["learner_profile"]:
        with st.spinner('正在识别技能差距...'):
            st.info("请完成入门流程以查看学习者档案。")
    else:
        try:
            render_learner_profile_info(goal)
        except Exception as e:
            st.error("渲染学习者档案时发生错误。")
            # re generate the learner profile
            with st.spinner("正在重新准备您的档案..."):
                learner_profile = create_learner_profile(goal["learning_goal"], st.session_state["learner_information"], goal["skill_gaps"], st.session_state["llm_type"])
            goal["learner_profile"] = learner_profile
            try:
                save_persistent_state()
            except Exception:
                pass
            st.rerun()

def render_learner_profile_info(goal):
    st.markdown("""
        <style>
        .section {
            background-color: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
        }
        .progress-indicator {
            color: #28a745;
            font-weight: bold;
        }
        .skill-in-progress {
            color: #ffc107;
        }
        .skill-required {
            color: #dc3545;
        }
        </style>
    """, unsafe_allow_html=True)
    learner_profile = goal["learner_profile"]
    with st.container(border=True):
        # Learner Information
        st.markdown("#### 👤 学习者信息")
        st.markdown(f"<div class='section'>{learner_profile['learner_information']}</div>", unsafe_allow_html=True)

        # Learning Goal
        st.markdown("#### 🎯 学习目标")
        st.markdown(f"<div class='section'>{learner_profile['learning_goal']}</div>", unsafe_allow_html=True)

    with st.container(border=True):
        render_cognitive_status(goal)
    with st.container(border=True):
        render_learning_preferences(goal)
    with st.container(border=True):
        render_behavioral_patterns(goal)

    render_additional_info_form(goal)


def render_cognitive_status(goal):
    learner_profile = goal["learner_profile"]
    # Cognitive Status
    st.markdown("#### 🧠 认知状态")
    st.write("**总体进度：**")
    st.progress(learner_profile["cognitive_status"]["overall_progress"])
    st.markdown(f"<p class='progress-indicator'>{learner_profile['cognitive_status']['overall_progress']}% 已完成</p>", unsafe_allow_html=True)
    render_skill_info(learner_profile)

def render_learning_preferences(goal):
    learner_profile = goal["learner_profile"]
    st.markdown("#### 📚 学习偏好")
    st.write(f"**内容风格：** {learner_profile['learning_preferences']['content_style']}")
    st.write(f"**偏好的活动类型：** {learner_profile['learning_preferences']['activity_type']}")
    st.write(f"**其他备注：**")
    st.info(learner_profile['learning_preferences']['additional_notes'])

def render_behavioral_patterns(goal):
    learner_profile = goal["learner_profile"]
    st.markdown("#### 📊 行为模式")
    st.write(f"**系统使用频率：**")
    st.info(learner_profile['behavioral_patterns']['system_usage_frequency'])
    st.write(f"**课程时长和参与度：**")
    st.info(learner_profile['behavioral_patterns']['session_duration_engagement'])
    st.write(f"**激励触发因素：**")
    st.info(learner_profile['behavioral_patterns']['motivational_triggers'])
    st.write(f"**其他备注：**")
    st.info(learner_profile['behavioral_patterns']['additional_notes'])


def render_additional_info_form(goal):
    with st.form(key="additional_info_form"):
        st.markdown("#### 重视您的反馈")
        st.info("通过提供您的反馈帮助我们改善您的学习体验。")
        st.write("您对当前档案的认同程度如何？")
        agreement_star = st.feedback("stars", key="agreement_star")
        st.write("您有任何建议或更正吗？")
        suggestions = st.text_area("在此提供您的建议。", label_visibility="collapsed")
        st.write("您有任何其他信息要添加吗？")
        additional_info = st.text_area("在此提供任何其他信息或反馈。", label_visibility="collapsed")
        pdf_file = st.file_uploader("上传包含其他信息的 PDF（例如简历）", type="pdf")
        if pdf_file is not None:
            with st.spinner("正在从 PDF 提取文本..."):
                additional_info_pdf = extract_text_from_pdf(pdf_file)
                st.toast("✅ PDF 上传成功。")
        else:
            additional_info_pdf = ""
        st.session_state["additional_info"] = {
            "agreement_star": agreement_star,
            "suggestions": suggestions,
            "additional_info": additional_info + additional_info_pdf
        }
        try:
            save_persistent_state()
        except Exception:
            pass
        submit_button = st.form_submit_button("更新档案", on_click=update_learner_profile_with_additional_info, 
                                              kwargs={"goal": goal, "additional_info": additional_info, }, type="primary")
        
def update_learner_profile_with_additional_info(goal, additional_info):
    additional_info = st.session_state["additional_info"]
    new_learner_profile = update_learner_profile(goal["learner_profile"], additional_info)
    if new_learner_profile is not None:
        goal["learner_profile"] = new_learner_profile
        try:
            save_persistent_state()
        except Exception:
            pass
        st.toast("🎉 档案更新成功！")
    else:
        st.toast("❌ 档案更新失败。请重试。")


render_learner_profile()