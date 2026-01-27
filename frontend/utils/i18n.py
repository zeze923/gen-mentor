# -*- coding: utf-8 -*-
"""国际化配置文件 - 中文翻译"""

# 通用文本
COMMON = {
    "back": "返回",
    "next": "下一步",
    "previous": "上一页",
    "next_page": "下一页",
    "submit": "提交",
    "save": "保存",
    "cancel": "取消",
    "delete": "删除",
    "edit": "编辑",
    "confirm": "确认",
    "close": "关闭",
    "add": "添加",
    "clear": "清空",
    "regenerate": "重新生成",
    "complete": "完成",
    "loading": "加载中...",
    "error": "错误",
    "success": "成功",
    "warning": "警告",
    "info": "信息",
}

# 导航菜单
NAVIGATION = {
    "onboarding": "入门引导",
    "goal_management": "目标管理",
    "learning_path": "学习路径",
    "knowledge_document": "继续学习",
    "resume_learning": "继续学习",
    "learner_profile": "我的档案",
    "my_profile": "我的档案",
    "dashboard": "学习分析",
    "analytics_dashboard": "学习分析",
    "skill_gap": "技能差距",
    "reset": "重置",
}

# 入门引导页面
ONBOARDING = {
    "title": "欢迎来到 GenMentor",
    "subtitle": "您的个性化学习助手",
    "learning_goal": "学习目标",
    "learning_goal_placeholder": "请输入您的学习目标，例如：我想学习 Python 编程",
    "learner_info": "学习者信息",
    "learner_info_placeholder": "请简要介绍您的背景、经验和学习偏好...",
    "occupation": "职业",
    "occupation_placeholder": "例如：学生、软件工程师、数据分析师等",
    "upload_resume": "上传简历（可选）",
    "start_journey": "开始学习之旅",
    "please_enter_goal": "请输入学习目标",
    "please_enter_info": "请输入学习者信息",
}

# 目标管理页面
GOAL_MANAGEMENT = {
    "title": "目标管理",
    "description": "管理您的学习目标：添加新目标，编辑或删除现有目标。",
    "add_new_goal": "🎯 添加新目标",
    "enter_goal": "输入您的新目标：",
    "existing_goals": "📋 现有目标",
    "no_goals": "暂无目标。请在上方添加新目标开始学习！",
    "goal": "目标",
    "current_active_goal": "当前活跃目标",
    "set_as_active": "设为活跃目标",
    "overall_progress": "总体进度：",
    "progress": "进度",
    "total_skills": "总技能数",
    "mastered_skills": "已掌握技能数",
    "in_progress_skills": "学习中技能数",
    "skill_info": "技能信息",
    "delete_success": "目标删除成功！",
    "update_success": "目标更新成功！",
    "refine": "优化",
    "refining": "优化中...",
    "skill_gap_dialog_title": "技能差距",
    "review_skill_gaps": "查看并确认您的技能差距。",
    "schedule_learning_path": "安排学习路径",
}

# 技能差距页面
SKILL_GAP = {
    "title": "技能差距",
    "description": "查看并确认您的技能差距。",
    "identifying": "正在识别技能差距...",
    "total_skills": "共有 {num_skills} 项技能，其中识别出 {num_gaps} 个技能差距。",
    "skill_name": "技能名称",
    "current_level": "当前水平",
    "required_level": "所需水平",
    "is_gap": "是否为差距",
    "confirm_gaps": "确认差距",
    "schedule_path": "安排学习路径",
}

# 学习路径页面
LEARNING_PATH = {
    "title": "学习路径",
    "description": "您的个性化学习路径",
    "scheduling": "正在安排学习路径...",
    "rescheduling": "正在重新安排学习路径...",
    "session": "课程",
    "sessions": "课程",
    "session_count": "课程数量：",
    "reschedule": "重新安排",
    "start_learning": "开始学习",
    "continue_learning": "继续学习",
    "completed": "已完成",
    "in_progress": "进行中",
    "not_started": "未开始",
    "associated_skills": "相关技能：",
    "feedback_placeholder": "请提供您对当前学习路径的反馈...",
}

# 知识文档页面
KNOWLEDGE_DOCUMENT = {
    "title": "学习内容",
    "back": "返回",
    "regenerate": "重新生成",
    "complete_session": "完成课程",
    "session": "课程",
    "associated_skills": "相关技能：",
    "stage_1": "阶段 1/4 - 探索知识点...",
    "stage_1_success": "阶段 1/4 🔍 知识点探索成功。",
    "stage_2": "阶段 2/4 - 起草知识点...",
    "stage_2_success": "阶段 2/4 📝 知识点起草成功。",
    "stage_3": "阶段 3/4 - 整合知识文档...",
    "stage_3_success": "阶段 3/4 📚 知识文档整合成功。",
    "stage_4": "阶段 4/4 - 生成文档测验...",
    "stage_4_success": "阶段 4/4 🎯 文档测验生成成功。",
    "failed_to_prepare": "准备知识内容失败。",
    "failed_api_none": "整合知识文档失败 - API 返回 None。",
    "test_knowledge": "💡 测试您的知识",
    "correct": "正确！",
    "incorrect": "不正确。",
    "explanation": "解释",
    "options": "选项",
    "true_or_false": "对或错？",
    "your_answer": "您的答案",
    "document_structure": "文档结构",
    "previous_page": "上一页",
    "next_page": "下一页",
    "feedback_title": "🌟 重视您的反馈！",
    "feedback_description": "您的反馈帮助我们改进学习体验。\n请花一点时间分享您的想法。",
    "clarity": "内容清晰度",
    "relevance": "与目标的相关性",
    "depth": "内容深度",
    "engagement": "参与度",
    "additional_comments": "其他意见",
    "submit_feedback": "提交反馈",
    "thank_you": "感谢您的反馈！",
    "updating_profile": "正在更新您的档案...",
    "profile_updated": "🎉 您的档案已更新！",
    "session_completed": "🎉 课程完成成功！",
    "creating_profile": "正在创建您的档案...",
    "profile_created": "🎉 您的档案已创建！",
}

# 学习者档案页面
LEARNER_PROFILE = {
    "title": "我的学习档案",
    "description": "查看和管理您的学习档案",
    "learning_goal": "学习目标",
    "skill_gaps": "技能差距",
    "cognitive_status": "认知状态",
    "overall_progress": "总体进度",
    "mastered_skills": "已掌握技能",
    "in_progress_skills": "学习中技能",
    "learning_preferences": "学习偏好",
    "preferred_content_types": "偏好的内容类型",
    "preferred_difficulty": "偏好的难度",
    "behavioral_patterns": "行为模式",
    "engagement_level": "参与度",
    "learning_pace": "学习节奏",
    "additional_notes": "其他备注",
}

# 仪表板页面
DASHBOARD = {
    "title": "学习分析",
    "description": "在这里跟踪您的学习进度并查看学习洞察。",
    "learning_progress": "学习进度",
    "view_progress": "查看每个课程的学习进度。",
    "overall_progress": "总体进度：",
    "skill_proficiency": "不同技能的熟练程度",
    "mastered_count": "您已掌握 {mastered} 项技能，目前正在学习 {in_progress} 项技能。",
    "current_level": "当前熟练程度",
    "required_level": "所需熟练程度",
    "session_timeseries": "课程学习时间序列",
    "view_over_time": "查看随时间变化的学习进度。",
    "session": "课程",
    "time": "时间",
    "mastery_timeseries": "掌握技能时间序列",
    "mastery_rate": "掌握率",
    "wait_for_path": "请等待学习路径安排完成后查看仪表板。",
    "no_goals": "未找到目标。请先创建一个目标。",
    "go_to_management": "前往目标管理",
}

# 熟练程度级别
PROFICIENCY_LEVELS = {
    "unlearned": "未学习",
    "beginner": "初级",
    "intermediate": "中级",
    "advanced": "高级",
}

# 提示和帮助文本
HINTS = {
    "goal_refinement": "点击'优化'按钮可以让 AI 帮助您完善学习目标",
    "skill_gap_help": "技能差距分析帮助识别您需要学习的内容",
    "learning_path_help": "学习路径是根据您的技能差距和学习偏好定制的",
}

# 错误消息
ERRORS = {
    "no_goal": "未找到目标",
    "no_session": "未找到课程",
    "api_error": "API 请求失败",
    "network_error": "网络错误",
    "unknown_error": "未知错误",
}

# 成功消息
SUCCESS = {
    "goal_added": "目标添加成功！",
    "goal_updated": "目标更新成功！",
    "goal_deleted": "目标删除成功！",
    "session_completed": "课程完成成功！",
    "profile_updated": "档案更新成功！",
}

# 确认对话框
DIALOGS = {
    "confirm_reset_title": "确认重置",
    "confirm_reset_message": "所有历史记录将被清除。您确定要重置吗？",
    "confirm_delete_title": "确认删除",
    "confirm_delete_message": "您确定要删除此目标吗？",
}

# 占位符文本
PLACEHOLDERS = {
    "enter_text": "请输入文本...",
    "search": "搜索...",
    "select": "请选择...",
}

def get_text(key, **kwargs):
    """获取翻译文本，支持格式化"""
    # 尝试从各个字典中查找
    for dict_name in [COMMON, NAVIGATION, ONBOARDING, GOAL_MANAGEMENT, 
                      SKILL_GAP, LEARNING_PATH, KNOWLEDGE_DOCUMENT, 
                      LEARNER_PROFILE, DASHBOARD, PROFICIENCY_LEVELS,
                      HINTS, ERRORS, SUCCESS, DIALOGS, PLACEHOLDERS]:
        if key in dict_name:
            text = dict_name[key]
            if kwargs:
                return text.format(**kwargs)
            return text
    return key  # 如果找不到，返回 key 本身
