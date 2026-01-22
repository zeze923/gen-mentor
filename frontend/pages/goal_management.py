import streamlit as st

from components.goal_refinement import render_goal_refinement
from utils.request_api import create_learner_profile, identify_skill_gap
from components.gap_identification import render_identified_skill_gap, render_identifying_skill_gap
from utils.state import add_new_goal, change_selected_goal_id, index_goal_by_id, reset_to_add_goal, save_persistent_state
from components.skill_info import render_skill_info


def render_goal_management():
    st.title("目标管理")
    st.write("管理您的学习目标：添加新目标，编辑或删除现有目标。")

    render_add_new_goal()
    st.divider()
    render_existing_goals()

def render_add_new_goal():
    if "if_refining_learning_goal" not in st.session_state:
        st.session_state["if_refining_learning_goal"] = False
        try:
            save_persistent_state()
        except Exception:
            pass
    if "if_show_skill_gap_results_in_dialog" not in st.session_state:
        st.session_state["if_show_skill_gap_results_in_dialog"] = False
        try:
            save_persistent_state()
        except Exception:
            pass
    
    # Initialize to_add_goal if not present
    if "to_add_goal" not in st.session_state:
        reset_to_add_goal()
    
    # 确保 to_add_goal 的所有字段都正确初始化
    to_add_goal = st.session_state["to_add_goal"]
    if to_add_goal.get("skill_gaps") is None:
        to_add_goal["skill_gaps"] = []
    if to_add_goal.get("learner_profile") is None:
        to_add_goal["learner_profile"] = {}
    if to_add_goal.get("learning_path") is None:
        to_add_goal["learning_path"] = []
    if to_add_goal.get("learning_goal") is None:
        to_add_goal["learning_goal"] = ""
    st.subheader("🎯 添加新目标")
    new_learning_goal = st.text_area("输入您的新目标：", to_add_goal["learning_goal"], key="new_learning_goal")
    to_add_goal["learning_goal"] = new_learning_goal

    refine_col, clear_col, hint_col, add_col = st.columns([1, 1, 3, 1])

    render_goal_refinement(to_add_goal, refine_col, hint_col)
    if clear_col.button("清空", key="clear_goal"):
        reset_to_add_goal()
        try:
            save_persistent_state()
        except Exception:
            pass
        st.rerun()

    if add_col.button("添加目标", type="primary", icon=":material/add:", use_container_width=True):
        if new_learning_goal:
            render_skill_gap_dialog()
        else:
            hint_col.warning("请在添加前输入目标。")

    if st.session_state["if_show_skill_gap_results_in_dialog"]:
        render_skill_gap_dialog()



def render_existing_goals():
    st.subheader("📋 Existing Goals")
    
    # Initialize goals if not present
    if "goals" not in st.session_state:
        st.session_state["goals"] = []
    
    goals = st.session_state["goals"]
    non_deleted_goals = [goal for goal in goals if not goal["is_deleted"]]
    
    if not non_deleted_goals:
        st.info("No existing goals. Add a new goal above to get started!")
        return

    for goal_id, goal in enumerate(non_deleted_goals):
        with st.container():
            col_left, col_right = st.columns([3, 1])
            col_left.write(f"#### Goal {goal_id + 1}")
            
            # Check if the current goal is the active goal
            is_active = st.session_state.get("selected_goal_id") == goal["id"]
            
            if is_active:
                col_right.button("Current Active Goal", type="primary", key=f"active_{goal['id']}", use_container_width=True)
            else:
                if col_right.button("Set as Active Goal", key=f"set_{goal['id']}", help="Mark this goal as your active learning goal."):
                    st.session_state.selected_goal_id = goal["id"]
                    try:
                        save_persistent_state()
                    except Exception:
                        pass
                    change_selected_goal_id(goal["id"])
                    try:
                        save_persistent_state()
                    except Exception:
                        pass
                    st.rerun()
            
            st.info(f"{goal['learning_goal']}")
            st.write(f"**Overall Progress:**")
            learner_profile = goal["learner_profile"]
            overall_progress = learner_profile["cognitive_status"]["overall_progress"]
            progress = st.slider("Progress", min_value=0, max_value=100, value=overall_progress, key=f"progress_{goal['id']}", disabled=True)
            unlearned_skill = len(goal['learner_profile']['cognitive_status']['in_progress_skills'])
            learned_skill = len(goal['learner_profile']['cognitive_status']['mastered_skills'])
            all_skill = learned_skill + unlearned_skill
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.metric(label="Total Skill Count", value=all_skill, delta_color="off")
            with col2:
                st.metric(label="Mastered Skill Count", value=learned_skill, delta_color="off")
            with col3:
                st.metric(label="In-progress Skill Count", value=unlearned_skill, delta_color="off")
            with st.expander("Skill Info"):
                render_skill_info(goal["learner_profile"])
            
            col1, col2 = st.columns([7, 1])
            with col1:
                if st.button("Edit", key=f"edit_{goal['id']}"):
                    edited_goal = st.text_area("Edit Goal", value=goal["learning_goal"])
                    if st.button("Save", key=f"save_{goal['id']}"):
                        goal["learning_goal"] = edited_goal
                        st.success("Goal updated successfully!")
            with col2:
                if st.button("Delete", key=f"delete_{goal['id']}", type="primary"):
                    goal_index = index_goal_by_id(goal["id"])
                    st.session_state.goals[goal_index]["is_deleted"] = True
                    try:
                        save_persistent_state()
                    except Exception:
                        pass
                    st.success("Goal deleted successfully!")
                    st.rerun()
        
        if goal_id < len(non_deleted_goals) - 1:
            st.divider()

            
            


@st.dialog("技能差距", width="large")
def render_skill_gap_dialog():
    # Initialize to_add_goal if not present
    if "to_add_goal" not in st.session_state:
        reset_to_add_goal()
    
    to_add_goal = st.session_state["to_add_goal"]
    st.write("查看并确认您的技能差距。")
    
    # 确保 skill_gaps 不是 None
    if to_add_goal["skill_gaps"] is None:
        to_add_goal["skill_gaps"] = []
    
    num_skills = len(to_add_goal["skill_gaps"])
    num_gaps = sum(1 for skill in to_add_goal["skill_gaps"] if skill.get("is_gap", False))
    st.info(f"共有 {num_skills} 项技能，其中识别出 {num_gaps} 个技能差距。")
    if not to_add_goal["skill_gaps"]:
        st.session_state["if_show_skill_gap_results_in_dialog"] = True
        try:
            save_persistent_state()
        except Exception:
            pass
        render_identifying_skill_gap(to_add_goal)
    else:
        st.session_state["if_show_skill_gap_results_in_dialog"] = False
        try:
            save_persistent_state()
        except Exception:
            pass
        render_identified_skill_gap(to_add_goal)
        if_schedule_learning_path_ready = to_add_goal["skill_gaps"]
        if st.button("安排学习路径", type="primary", disabled=not if_schedule_learning_path_ready):
            if to_add_goal["skill_gaps"] and not to_add_goal["learner_profile"]:
                with st.spinner('正在创建您的档案...'):
                    learner_profile = create_learner_profile(to_add_goal["learning_goal"], st.session_state["learner_information"], to_add_goal["skill_gaps"])
                    if learner_profile is None:
                        st.rerun()
                    to_add_goal["learner_profile"] = learner_profile
                    st.toast("🎉 您的档案已创建！")
            new_goal_id = add_new_goal(**to_add_goal)
            st.session_state["selected_goal_id"] = new_goal_id
            try:
                save_persistent_state()
            except Exception:
                pass
            st.session_state["if_complete_onboarding"] = True
            try:
                save_persistent_state()
            except Exception:
                pass
            st.session_state["selected_page"] = "Learning Path"
            try:
                save_persistent_state()
            except Exception:
                pass
            st.switch_page("pages/learning_path.py")



render_goal_management()