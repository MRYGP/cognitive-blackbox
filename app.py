# cognitive-blackbox/app.py
"""
Cognitive Black Box - Streamlit Main Application Entry
This file contains the main application logic, based on Claude's implementation.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root directory to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Import custom modules (using dummy classes for standalone execution)
# from utils.session_manager import session_manager
# from utils.ai_roles import ai_engine
# from utils.data_models import CaseType, RoleType, create_case_session

# --- Dummy classes to make the app runnable ---
class DummySessionManager:
    def initialize_session(self, case_id):
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 1
        st.session_state.current_case = case_id
        return True
    def advance_step(self):
        if st.session_state.current_step < 4:
            st.session_state.current_step += 1
        return True
    def get_session_summary(self): return {"info": "Session summary placeholder"}
    def get_current_context(self): return {"info": "Current context placeholder"}

class DummyAIEngine:
    def get_available_apis(self): return ["DummyAPI"]
    def get_cache_stats(self): return {"hits": 0, "misses": 0}
    def clear_cache(self): pass
    def generate_response(self, role, text, context): return "AI response placeholder.", True

session_manager = DummySessionManager()
ai_engine = DummyAIEngine()
# --- End of Dummy classes ---


class CognitiveBlackBoxApp:
    """
    Cognitive Black Box main application class.
    Responsible for overall application flow control, preserving Claude's original design.
    """
    
    def __init__(self):
        """Initialize application"""
        self.app_title = "🧠 认知黑匣子"
        self.app_description = "18分钟认知升级体验"
        self.available_cases = {
            'madoff': '麦道夫庞氏骗局 - 光环效应',
            'ltcm': '长期资本管理 - 过度自信 (即将推出)', 
            'lehman': '雷曼兄弟 - 确认偏误 (即将推出)'
        }
    
    def run(self):
        """Run main application"""
        self._configure_page()
        self._initialize_session()
        self._show_header()
        self._main_app_logic()
        self._show_debug_info()

    def _configure_page(self):
        """Configure Streamlit page basic settings"""
        st.set_page_config(
            page_title=self.app_title,
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="auto"
        )
        self._inject_base_styles()

    def _inject_base_styles(self):
        """Inject basic CSS styles as designed"""
        # Using the final CSS provided by Hoshino
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Lato:wght@400;700&family=Lora:wght@400;700&family=Merriweather:wght@400;700&display=swap');
            .stApp { background-color: #F0F2F6; }
            .block-container { max-width: 800px; padding-top: 2rem; }
            .role-container {
                border-radius: 12px; padding: 2rem; margin-bottom: 2rem;
                border-left: 6px solid; box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            }
            .role-host { background-color: #FFFFFF; border-color: #2A52BE; font-family: 'Lora', serif; }
            .role-investor { background-color: #FFF5F5; border-color: #D93025; font-family: 'Inter', sans-serif; }
            .role-mentor { background-color: #F3F9F3; border-color: #006A4E; font-family: 'Merriweather', serif; }
            .role-assistant { background-color: #F1FAFA; border-color: #007B7C; font-family: 'Lato', sans-serif; }
        </style>
        """, unsafe_allow_html=True)
    
    def _initialize_session(self):
        """Initialize session state"""
        if 'initialized' not in st.session_state:
            success = session_manager.initialize_session('madoff')
            if success:
                st.session_state.initialized = True
                st.session_state.app_version = "0.1.0"
            else:
                st.error("应用初始化失败,请刷新页面重试")
                st.stop()

    def _show_header(self):
        """Show application header"""
        st.title(self.app_title)
        st.caption(self.app_description)
    
    def _main_app_logic(self):
        """Main application logic"""
        current_step = st.session_state.get('current_step', 1)
        
        render_functions = {1: self._show_step_1_host, 2: self._show_step_2_investor, 3: self._show_step_3_mentor, 4: self._show_step_4_assistant}
        render_function = render_functions.get(current_step)
        
        if render_function:
            render_function()
        else:
            st.error(f"Unknown step: {current_step}")

    def _show_step_1_host(self):
        """Step 1: Host - Decision Immersion"""
        st.header("第一幕: 决策代入")
        st.progress(25)
        
        with st.container():
            st.markdown('<div class="role-container role-host">', unsafe_allow_html=True)
            st.markdown("""
            ### 你好,决策者。
            我知道你身经百战，今天，我想与你分享一个 **价值650亿美元的教训**。
            ---
            2008年,华尔街爆出惊天丑闻:**前纳斯达克主席**被自己的儿子举报涉嫌金融诈骗。
            ### 投资机会档案
            让我们回到2005年，一个朋友向你推荐了这个机会，来配置 **3000万美元** 的资金。
            - **基金经理:** 伯纳德·麦道夫, 前纳斯达克主席
            - **历史业绩:** 过去15年, 年均回报稳定在10-12%
            - **客户构成:** 顶级银行、欧洲皇室、好莱坞明星
            - **投资策略:** 复杂且保密的"价差转换套利策略"
            """)
            
            if 'user_decision' not in st.session_state:
                st.session_state.user_decision = "小部分试水" # Default value
            
            st.session_state.user_decision = st.radio(
                "**你的专业判断是？**",
                ["全力投入", "大部分投入", "小部分试水", "放弃投资"],
                horizontal=True, index=2
            )
            
            if st.button("完成判断, 进入下一幕", type="primary", use_container_width=True):
                if session_manager.advance_step():
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

    def _show_step_2_investor(self):
        """Step 2: Investor - Reality Disruption"""
        st.header("第二幕: 现实击穿")
        st.progress(50)
        
        with st.container():
            st.markdown('<div class="role-container role-investor">', unsafe_allow_html=True)
            st.markdown("""
            ### 刚才你的分析，很专业。但让我告诉你一个残酷的现实。
            你刚才分析的“伯纳德·麦道夫”，就是美国历史上最大的金融诈骗犯。
            **650亿美元！** 这是确认的诈骗总金额。
            **37,000名受害者**，遍及136个国家。
            """)
            st.subheader("现在，让我用投资人的视角，问你四个专业问题:")
            
            user_decision = st.session_state.get('user_decision', '未知')
            
            if user_decision in ["全力投入", "大部分投入"]:
                q1_text = f"#### 质疑一: 我注意到你刚才选择了【{user_decision}】，你为什么会让一个监管者的光环，降低了你的投资判断标准？"
            else:
                q1_text = f"#### 质疑一: 你选择了【{user_decision}】，但即使谨慎也不等于免疫光环效应。你知道如何系统性地识别权威陷阱吗？"

            questions_list = [
                q1_text,
                "#### 质疑二: 你为什么会相信一条“不可能存在”的回报曲线？\n\n异常的稳定，本身就是最大的风险信号。",
                "#### 质疑三: 你为什么会接受一个完全不透明的“黑盒子”？\n\n真正的投资大师分享原则，而骗子才需要绝对的黑盒。",
                "#### 质疑四: 你为什么会让“别人”替你思考？\n\n当所有人都依赖他人判断时，这不是集体智慧，而是集体催眠。"
            ]
            
            for i, question in enumerate(questions_list, 1):
                with st.expander(f"展开质疑 {i}", expanded=True):
                    st.markdown(question)
            
            st.markdown('</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("总损失", "$650亿", "-100%")
        col2.metric("受害者", "37,000+", "136国")
        col3.metric("诈骗时长", "20年+", "“完美”记录")
        
        if st.button("我明白了...进入下一步，学习如何防范", type="primary", use_container_width=True):
            if session_manager.advance_step():
                st.rerun()

    def _show_step_3_mentor(self):
        """Step 3: Mentor - Framework Reconstruction"""
        st.header("第三幕: 框架重构")
        st.progress(75)
        
        with st.container():
            st.markdown('<div class="role-container role-mentor">', unsafe_allow_html=True)
            st.markdown("""
            ### 你掉入了一个典型的思维陷阱——光环效应 (The Halo Effect)。
            即，将一个目标的某个突出优点，泛化到他所有不相关的特质上。
            ### 如何打破“光环”？你需要一个强制性的“认知防火墙”。
            我称之为 **“四维独立验证矩阵”**。
            - **维度1: 身份验证** - 职位 ≠ 能力
            - **维度2: 能力验证** - 业绩必须可审计
            - **维度3: 信息验证** - 拒绝黑盒子操作
            - **维度4: 独立验证** - 主动寻找反对意见
            """)
            if st.button("我掌握了。请给我实用的工具", type="primary", use_container_width=True):
                if session_manager.advance_step():
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    def _show_step_4_assistant(self):
        """Step 4: Assistant - Capability Armament"""
        st.header("第四幕: 能力武装")
        st.progress(100)
        
        with st.container():
            st.markdown('<div class="role-container role-assistant">', unsafe_allow_html=True)
            user_decision = st.session_state.get('user_decision', '未知')
            
            feedback_map = {
                "全力投入": "您选择了**全力投入**，这表明您需要特别警惕**光环效应**的影响。",
                "大部分投入": "您选择了**大部分投入**，说明您仍容易被权威身份影响，需要加强**独立验证**能力。",
                "小部分试水": "您选择了**小部分试水**，展现了优秀的风险控制意识，建议将此流程系统化。",
                "放弃投资": "您选择了**放弃投资**，说明您具备优秀的风险嗅觉，现在需要的是系统化的决策框架。"
            }
            feedback_text = feedback_map.get(user_decision, "您的决策展示了独特的思考。")
            
            st.markdown(f"""
            ### 🎯 基于您的选择的个性化分析
            您的选择是：**{user_decision}**。
            
            {feedback_text}
            """)
            
            card_content = """
            ### 🛡️ 高级决策安全系统
            **核心原则: 权威越强，越要验证。**
            - **身份验证:** 权威与能力是否匹配?
            - **能力验证:** 业绩是否有第三方审计?
            - **信息验证:** 是否要求接受黑盒子?
            - **独立验证:** 是否寻找了反对意见?
            """
            st.success("您的专属决策工具已生成！")
            st.markdown(card_content)
            
            if st.button("重新开始体验", use_container_width=True):
                keys_to_clear = ['initialized', 'current_step', 'user_decision']
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _show_debug_info(self):
        """Show debug information in the sidebar."""
        if st.sidebar.checkbox("显示调试信息"):
            st.sidebar.subheader("🔧 调试信息")
            st.sidebar.json(session_manager.get_session_summary())
            st.sidebar.subheader("当前上下文")
            st.sidebar.json(session_manager.get_current_context())
            self._test_ai_integration()

    def _test_ai_integration(self):
        """A simple form in the sidebar to test AI integration."""
        st.sidebar.subheader("🤖 AI集成测试")
        test_role = st.sidebar.selectbox("选择角色", ['host', 'investor', 'mentor', 'assistant'])
        test_input = st.sidebar.text_input("测试输入", "你好")
        if st.sidebar.button("测试AI响应"):
            context = session_manager.get_current_context()
            response, success = ai_engine.generate_response(test_role, test_input, context)
            if success:
                st.sidebar.success("AI响应成功:")
                st.sidebar.write(response)
            else:
                st.sidebar.error("AI响应失败:")
                st.sidebar.write(response)

def main():
    """Main function to run the Streamlit application."""
    try:
        app = CognitiveBlackBoxApp()
        app.run()
    except Exception as e:
        st.error(f"应用运行出现严重错误: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
