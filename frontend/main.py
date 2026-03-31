import subprocess
import sys
import os

def install_dependencies():
    """Attempt to install dependencies from requirements.txt at runtime."""
    # Use a file-based flag to avoid repeated installations in the same deployment
    flag_file = "/tmp/dependencies_installed.txt" if os.name != 'nt' else os.path.join(os.environ.get('TEMP', ''), 'dependencies_installed.txt')
    
    if not os.path.exists(flag_file):
        print("检测到环境缺少依赖，正在自动安装，请稍候...")
        try:
            # Determine requirements.txt path relative to this file
            current_dir = os.path.dirname(__file__)
            req_path = os.path.join(current_dir, "requirements.txt")
            
            # If not in frontend/requirements.txt, try root requirements.txt
            if not os.path.exists(req_path):
                req_path = os.path.join(os.path.dirname(current_dir), "requirements.txt")

            if os.path.exists(req_path):
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", 
                    "-r", req_path, 
                    "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
                ])
                with open(flag_file, "w") as f:
                    f.write("installed")
                print("依赖安装成功！请刷新页面或等待应用自动重载。")
                # Force a rerun if possible, though simply finishing the script might work
        except Exception as e:
            print(f"自动安装依赖失败: {e}")

# Run installation check
install_dependencies()

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

