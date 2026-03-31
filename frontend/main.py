import subprocess
import sys

def install_missing_packages():
    """Attempt to install missing packages at runtime."""
    required_packages = [
        "streamlit-float",
        "streamlit-card",
        "streamlit-chat",
        "streamlit-extras",
        "st-pages",
        "streamlit-option-menu",
        "streamlit-on-Hover-tabs",
        "extra-streamlit-components",
        "pdfplumber",
        "httpx"
    ]
    for package in required_packages:
        package_name = package.split('==')[0].replace('-', '_')
        try:
            __import__(package_name)
        except ImportError:
            print(f"Installing missing package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Run installation check before anything else
install_missing_packages()

import streamlit as st
import time
from utils.state import initialize_session_state, change_selected_goal_id, save_persistent_state, load_persistent_state, _get_data_store_path
initialize_session_state()


st.session_state.setdefault("_autosave_enabled", True)
try:
    save_persistent_state()
except Exception:
    pass

from components.chatbot import render_chatbot

st.set_page_config(page_title="GenMentor", page_icon="🧠", layout="wide")
st.logo("./assets/avatar.png")
st.markdown('<style>' + open('./assets/css/main.css').read() + '</style>', unsafe_allow_html=True)

try:
    if st.session_state.get("if_complete_onboarding", False) and not st.session_state.get("_navigated_lp_once", False):
        st.session_state["_navigated_lp_once"] = True
        try:
            st.switch_page("pages/learning_path.py")
        except Exception:
            pass
except Exception:
    pass

@st.dialog("确认重置")
def show_reset_dialog():
    st.warning("所有历史记录将被清除。您确定要重置吗？")
    st.divider()
    col_confirm, _space, col_cancel = st.columns([1, 2, 0.7])
    with col_confirm:
        if st.button("确认", type="primary"):
            from pathlib import Path
            from datetime import datetime
            import shutil
            try:
                st.session_state["_autosave_enabled"] = False
            except Exception:
                pass
            try:
                data_path = _get_data_store_path()
            except Exception:
                data_path = Path(__file__).resolve().parent / "user_data" / "data_store.json"
            try:
                data_path.parent.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass
            if data_path.exists():
                try:
                    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
                    backup_path = data_path.parent / f"data_storage-{ts}.json"
                    shutil.copy2(str(data_path), str(backup_path))
                except Exception:
                    pass
                try:
                    data_path.unlink()
                except Exception:
                    pass
            try:
                st.session_state.clear()
            except Exception:
                pass
            try:
                # After clearing state, navigate to onboarding page explicitly
                try:
                    st.switch_page("pages/onboarding.py")
                except Exception:
                    st.rerun()
            except Exception:
                try:
                    st.rerun()
                except Exception:
                    pass
    with col_cancel:
        if st.button("取消"):
            # simply rerun to close the dialog without changes
            try:
                st.rerun()
            except Exception:
                try:
                    st.rerun()
                except Exception:
                    pass

if st.session_state["show_chatbot"]:
    render_chatbot()

if st.session_state["if_complete_onboarding"]:
    onboarding = st.Page("pages/onboarding.py", title="入门引导", icon=":material/how_to_reg:", default=False, url_path="onboarding")
    learning_path = st.Page("pages/learning_path.py", title="学习路径", icon=":material/route:", default=True, url_path="learning_path")
else:
    onboarding = st.Page("pages/onboarding.py", title="入门引导", icon=":material/how_to_reg:", default=True, url_path="onboarding")
    learning_path = st.Page("pages/learning_path.py", title="学习路径", icon=":material/route:", default=False, url_path="learning_path")
skill_gaps = st.Page("pages/skill_gap.py", title="技能差距", icon=":material/insights:", default=False, url_path="skill_gap")
knowledge_document = st.Page("pages/knowledge_document.py", title="继续学习", icon=":material/menu_book:", default=False, url_path="knowledge_document")
learner_profile = st.Page("pages/learner_profile.py", title="我的档案", icon=":material/person:", default=False, url_path="learner_profile")
goal_management = st.Page("pages/goal_management.py", title="目标管理", icon=":material/flag:", default=False, url_path="goal_management")
dashboard = st.Page("pages/dashboard.py", title="学习分析", icon=":material/browse:", default=False, url_path="dashboard")

# Learning Analytics Dashboard
if not st.session_state["if_complete_onboarding"]:
    nav_position = "sidebar"
    pg = st.navigation({"GenMentor": [onboarding, skill_gaps, learning_path]}, position="hidden", expanded=True)
else:
    nav_position = "sidebar"
    pg = st.navigation({"GenMentor": [goal_management, learning_path, knowledge_document, learner_profile, dashboard]}, position=nav_position, expanded=True)
    with st.sidebar:
        _left, _center, _right = st.columns([2, 2, 2])
        with _center:
            if st.button("重置", help="清除本地历史记录（保留时间戳备份）"):
                show_reset_dialog()
    goal = st.session_state["goals"][st.session_state["selected_goal_id"]]
    goal['start_time'] = time.time()
    try:
        save_persistent_state()
    except Exception:
        pass
    unlearned_skill = len(goal['learner_profile']['cognitive_status']['in_progress_skills'])
    learned_skill = len(goal['learner_profile']['cognitive_status']['mastered_skills'])
    all_skill = learned_skill + unlearned_skill

    if goal['id'] not in st.session_state['learned_skills_history']:
        st.session_state['learned_skills_history'][goal['id']] = []
        try:
            save_persistent_state()
        except Exception:
            pass

    if all_skill != 0:
        mastery_rate = learned_skill / all_skill if all_skill != 0 else 0
        if st.session_state['learned_skills_history'][goal['id']] == []:
            st.session_state['learned_skills_history'][goal['id']].append(mastery_rate)
            try:
                save_persistent_state()
            except Exception:
                pass
    if(time.time()-goal['start_time']>600):
        goal['start_time'] = time.time()
        try:
            save_persistent_state()
        except Exception:
            pass
        st.session_state['learned_skills_history'][goal['id']].append(mastery_rate)
        try:
            save_persistent_state()
        except Exception:
            pass

    if len(st.session_state['learned_skills_history'][goal['id']]) > 10:
        st.session_state['learned_skills_history'][goal['id']].pop(0)
        try:
            save_persistent_state()
        except Exception:
            pass

    try:
        save_persistent_state()
    except Exception:
        pass

try:
    if st.session_state.get("_autosave_enabled", True):
        save_persistent_state()
except Exception:
    pass

if len(st.session_state["goals"]) != 0:
    change_selected_goal_id(st.session_state["selected_goal_id"])
    try:
        save_persistent_state()
    except Exception:
        pass

pg.run()

