import streamlit as st
from collections import defaultdict
import pandas as pd
import re
import time

from utils.state import get_current_session_uid

def render_dashboard():
    # Initialize goals if not present
    if "goals" not in st.session_state or not st.session_state["goals"]:
        st.warning("未找到目标。请先创建一个目标。")
        if st.button("前往目标管理"):
            st.switch_page("pages/goal_management.py")
        return
    
    # Check if selected_goal_id is valid
    if "selected_goal_id" not in st.session_state:
        st.session_state["selected_goal_id"] = 0
    
    if st.session_state["selected_goal_id"] >= len(st.session_state["goals"]):
        st.session_state["selected_goal_id"] = 0
    
    goal = st.session_state["goals"][st.session_state["selected_goal_id"]]

    if not goal["learner_profile"]:
        st.warning("请等待学习路径安排完成后查看仪表板。")

    st.title("学习分析")
    st.write("在这里跟踪您的学习进度并查看学习洞察。")
    with st.container(border=True):
        render_learning_progress(goal)
    with st.container(border=True):
        render_skill_radar_chart(goal)
    with st.container(border=True):
        render_session_learning_timeseries(goal)
    with st.container(border=True):
        render_mastery_skills_timeseries(goal)


def render_learning_progress(goal):
    st.markdown("#### 学习进度")
    st.write("查看每个课程的学习进度。")
    learner_profile = goal["learner_profile"]
    overall_progress = learner_profile["cognitive_status"]["overall_progress"]
    st.progress(overall_progress)
    st.write(f"Overall Progress: {overall_progress:.2f}%")

def render_skill_radar_chart(goal):
    import plotly.graph_objects as go

    st.markdown("#### 不同技能的熟练程度")
    # st.write("View the skill radar chart for your learning progress.")
    learner_profile = goal["learner_profile"]
    mastered_skills = learner_profile["cognitive_status"]["mastered_skills"]
    in_progress_skills = learner_profile["cognitive_status"]["in_progress_skills"]
    level_map = defaultdict(lambda: 0, {"unlearned": 0, "未学习": 0, "beginner": 1, "初级": 1, "intermediate": 2, "中级": 2, "advanced": 3, "高级": 3})
    mastered_skills = [{
        "name": skill_info["name"], 
        "required_level": skill_info["proficiency_level"], 
        "current_level": skill_info["proficiency_level"]} for skill_info in mastered_skills]
    in_progress_skills = [{
        "name": skill_info["name"], 
        "required_level": skill_info["required_proficiency_level"], 
        "current_level": skill_info["current_proficiency_level"]} for skill_info in in_progress_skills]
    skills = mastered_skills + in_progress_skills
    skill_names = [skill["name"] for skill in skills]
    current_levels = [level_map[skill["current_level"]] for skill in skills]
    required_levels = [level_map[skill["required_level"]] for skill in skills]
    st.write(f"您已掌握 {len(mastered_skills)} 项技能，目前正在学习 {len(in_progress_skills)} 项技能。")

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=current_levels,
        theta=skill_names,
        fill='toself',
        name='当前熟练程度',
    ))
    fig.add_trace(go.Scatterpolar(
        r=required_levels,
        theta=skill_names,
        fill='toself',
        name='所需熟练程度',
        fillcolor='rgba(255, 192, 203, 0.3)',
        line=dict(color='rgba(255, 105, 97, 0.6)')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3],
                tickvals=[0, 1, 2, 3],
                ticktext=['未学习', '初级', '中级', '高级'],
                tickfont=dict(size=14)
            ),
            angularaxis=dict(  # Set font size for skill names (theta labels)
                tickfont=dict(size=18)
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="center",
            x=0.5,
            font=dict(size=18)
        ),
    )
    event = st.plotly_chart(fig, key="iris", on_select="rerun")


def render_session_learning_timeseries(goal):
    st.markdown("#### 课程学习时间序列")
    st.write("查看随时间变化的学习进度。")
    goal = st.session_state["goals"][st.session_state["selected_goal_id"]]
    session_data = {
        "Session": [],
        "Time": [],
    }
    for session in goal["learning_path"]:
        session_data["Session"].append(session['id'])
        if_learned = session['if_learned']
        
        if if_learned:
            selected_gid = st.session_state["selected_goal_id"]
            match = re.search(r'\d+', session['id'])
            selected_sid = int(match.group(0)) -1
            times = st.session_state["session_learning_times"][f'{selected_gid}-{selected_sid}']
            if times["end_time"] is not None:
                # st.markdown(times)
                time_spent = (times["end_time"] - times["start_time"]) / 60
                # st.markdown(time_spent)
            else:  
                time_spent = 0
            session_data["Time"].append(time_spent)
            # st.markdown(session_data)
        else:
            session_data["Time"].append(0)
    
    for sid, session in enumerate(goal["learning_path"]):
        session_uid = session["id"]
        if session_uid not in session_data["Session"]:
            session_data["Session"].append(session_uid)
            session_data["Time"].append(0)

    session_data = pd.DataFrame(session_data)

    st.bar_chart(session_data, x="Session", y="Time", stack=False)
    

def render_mastery_skills_timeseries(goal):
    st.markdown("#### 掌握技能时间序列")
    st.write("查看随时间变化的学习进度。")
    time_values = [i * 10 for i in range(len(st.session_state['learned_skills_history'][goal['id']]))]
    char_data = pd.DataFrame({
        '掌握率': st.session_state['learned_skills_history'][goal['id']],
        '时间': time_values,
    })
    st.line_chart(char_data, x='时间', y='掌握率')
    


render_dashboard()
