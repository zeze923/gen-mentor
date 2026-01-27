import streamlit as st

from utils.request_api import create_learner_profile, identify_skill_gap
from utils.state import save_persistent_state

def render_identifying_skill_gap(goal):
    with st.spinner('正在识别技能差距...'):
        learning_goal = goal["learning_goal"]
        learner_information = st.session_state["learner_information"]
        llm_type = st.session_state["llm_type"]
        skill_gaps = identify_skill_gap(learning_goal, learner_information, llm_type)
    goal["skill_gaps"] = skill_gaps
    save_persistent_state()
    st.rerun()
    st.toast("🎉 技能差距识别成功！")
    return skill_gaps


def render_identified_skill_gap(goal, method_name="genmentor"):
    """
    以卡片样式渲染技能差距，支持上一个/下一个切换。
    """
    levels = ["未学习", "初级", "中级", "高级"]
    level_map = {"unlearned": "未学习", "beginner": "初级", "intermediate": "中级", "advanced": "高级"}
    reverse_level_map = {"未学习": "unlearned", "初级": "beginner", "中级": "intermediate", "高级": "advanced"}
    
    # 在单页上渲染所有技能卡片（无分页）
    skill_gaps = goal.get("skill_gaps", [])
    total = len(skill_gaps)
    if total == 0:
        st.info("尚未识别出技能。")
        return

    for skill_id, skill_info in enumerate(skill_gaps):
        skill_name = skill_info.get("name", f"技能_{skill_id}")
        required_level_en = skill_info.get("required_level", "unlearned")
        current_level_en = skill_info.get("current_level", "unlearned")
        
        # 转换为中文显示
        required_level = level_map.get(required_level_en, required_level_en)
        current_level = level_map.get(current_level_en, current_level_en)

        background_color = "#ffe6e6" if skill_info.get("is_gap") else "#e6ffe6"
        text_color = "#ff4d4d" if skill_info.get("is_gap") else "#33cc33"

        with st.container(border=True):
            # 卡片标题
            st.markdown(
                f"""
                <div style="background-color: {background_color}; color: {text_color}; padding: 10px 16px; border-radius: 8px; margin-bottom: 12px; display: flex; align-items: center; min-height: 44px;">
                    <p style="font-weight: 700; margin: 0; flex: 1;">{skill_id+1:2d}. {skill_name}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # 所需水平选择器
            new_required_level = st.pills(
                "**所需水平**",
                options=levels,
                selection_mode="single",
                default=required_level,
                disabled=False,
                key=f"required_{skill_name}_{method_name}",
            )
            if new_required_level != required_level:
                goal["skill_gaps"][skill_id]["required_level"] = reverse_level_map[new_required_level]
                current_level_idx = levels.index(level_map.get(goal["skill_gaps"][skill_id].get("current_level", "unlearned"), "未学习"))
                if levels.index(new_required_level) > current_level_idx:
                    goal["skill_gaps"][skill_id]["is_gap"] = True
                else:
                    goal["skill_gaps"][skill_id]["is_gap"] = False
                save_persistent_state()
                st.rerun()

            # 当前水平选择器
            new_current_level = st.pills(
                "**当前水平**",
                options=levels,
                selection_mode="single",
                default=current_level,
                disabled=False,
                key=f"current_{skill_name}__{method_name}",
            )
            if new_current_level != current_level:
                goal["skill_gaps"][skill_id]["current_level"] = reverse_level_map[new_current_level]
                required_level_idx = levels.index(level_map.get(goal["skill_gaps"][skill_id].get("required_level", "unlearned"), "未学习"))
                if levels.index(new_current_level) < required_level_idx:
                    goal["skill_gaps"][skill_id]["is_gap"] = True
                else:
                    goal["skill_gaps"][skill_id]["is_gap"] = False
                save_persistent_state()
                st.rerun()

            # 详细信息
            with st.expander("更多分析详情"):
                current_idx = levels.index(level_map.get(goal["skill_gaps"][skill_id].get("current_level", "unlearned"), "未学习"))
                required_idx = levels.index(level_map.get(goal["skill_gaps"][skill_id].get("required_level", "unlearned"), "未学习"))
                if current_idx < required_idx:
                    st.warning("当前水平低于所需水平！")
                    goal["skill_gaps"][skill_id]["is_gap"] = True
                else:
                    st.success("当前水平等于或高于所需水平")
                    goal["skill_gaps"][skill_id]["is_gap"] = False
                st.write(f"**原因**: {skill_info.get('reason', '')}")
                st.write(f"**置信度**: {skill_info.get('level_confidence', '')}")
            save_persistent_state()
            # 差距切换
            old_gap_status = skill_info.get("is_gap", False)
            gap_status = st.toggle(
                "标记为差距",
                value=skill_info.get("is_gap", False),
                key=f"gap_{skill_name}_{method_name}",
                disabled=not skill_info.get("is_gap", False),
            )
            if gap_status != old_gap_status:
                goal["skill_gaps"][skill_id]["is_gap"] = gap_status
                if not goal["skill_gaps"][skill_id]["is_gap"]:
                    goal["skill_gaps"][skill_id]["current_level"] = goal["skill_gaps"][skill_id].get("required_level", goal["skill_gaps"][skill_id].get("current_level"))
                try:
                    save_persistent_state()
                except Exception:
                    pass
                st.rerun()

