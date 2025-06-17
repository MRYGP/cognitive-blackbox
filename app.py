# cognitive-blackbox/app.py

import streamlit as st
import sys
import time
from pathlib import Path
from io import BytesIO

# --- 1. Project Setup & Module Imports ---
# This ensures the app can find custom utility modules
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Assuming utils are in a subfolder, adjust if necessary
# from utils.session_manager import session_manager
# from utils.ai_roles import ai_engine
# For now, create dummy classes to make the app runnable without the full backend
class DummySessionManager:
    def initialize_session(self, case_id):
        st.session_state.current_step = 1
        st.session_state.current_case = case_id
        return True
    def advance_step(self):
        if st.session_state.current_step < 4:
            st.session_state.current_step += 1
        return True
session_manager = DummySessionManager()


class CognitiveBlackBoxApp:
    """
    Cognitive Black Box MVP Application.
    This class orchestrates the user's 18-minute cognitive reframing experience.
    """
    
    def __init__(self):
        self.app_title = "🧠 认知黑匣子"
        self.app_description = "18分钟认知升级体验"
        self.available_cases = {
            'madoff': '麦道夫骗局 (光环效应)',
            'ltcm': '长期资本管理 (过度自信) - 即将推出', 
            'lehman': '雷曼兄弟 (确认偏误) - 即将推出'
        }

    def run(self):
        """Run the main application flow."""
        self._configure_page()
        self._initialize_session()
        self._show_header()
        self._main_app_logic()
        self._show_debug_sidebar()

    # --- 2. Page Configuration & Styling ---
    def _configure_page(self):
        st.set_page_config(
            page_title=self.app_title,
            page_icon="🧠",
            layout="centered", # Centered layout is better for reading
            initial_sidebar_state="collapsed"
        )
    
    def _inject_css(self):
        """Injects the complete CSS designed by Hoshino (S)."""
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
            .role-investor h3 { color: #C00000; font-weight: 700; }
            .role-mentor { background-color: #F3F9F3; border-color: #006A4E; font-family: 'Merriweather', serif; }
            .role-assistant { background-color: #F1FAFA; border-color: #007B7C; font-family: 'Lato', sans-serif; }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. Session and Header Management ---
    def _initialize_session(self):
        if 'initialized' not in st.session_state:
            success = session_manager.initialize_session('madoff')
            if success:
                st.session_state.initialized = True
            else:
                st.error("应用初始化失败，请刷新页面重试。")
                st.stop()

    def _show_header(self):
        st.title(self.app_title)
        st.caption(self.app_description)

    # --- 4. Main Application Logic & Step Rendering ---
    def _main_app_logic(self):
        self._inject_css()
        current_step = st.session_state.get('current_step', 1)

        # Simple router to call the correct rendering function
        render_functions = {
            1: self._show_step_1_host,
            2: self._show_step_2_investor,
            3: self._show_step_3_mentor,
            4: self._show_step_4_assistant,
        }
        
        render_function = render_functions.get(current_step)
        if render_function:
            # Magic Moment Transition FX
            if st.session_state.get('last_step') != current_step and current_step == 2:
                 st.balloons()

            render_function()
            st.session_state.last_step = current_step
        else:
            st.error(f"未知步骤: {current_step}。请重启体验。")

    def _show_step_1_host(self):
        st.header("第一幕: 决策代入")
        st.progress(25, text=f"当前进度: 1/4")

        with st.container():
            st.markdown("""
            <div class="role-container role-host">
                <h3>你好，决策者。</h3>
                <p>今天，我想与你分享一个 <b>价值650亿美元的教训</b>。这不是一个遥远的故事，而是一面镜子。</p>
                <hr>
                <h4>投资机会档案</h4>
                <p>让我们回到2005年。一个你信任的朋友，向你推荐了这个'独家'的机会，来配置 <b>3000万美元</b> 资金。</p>
                <ul>
                    <li><b>基金经理:</b> 伯纳德·麦道夫，前纳斯达克主席。</li>
                    <li><b>历史业绩:</b> 过去15年，年均回报稳定在10-12%。</li>
                    <li><b>客户构成:</b> 顶级银行、欧洲皇室、好莱坞明星。</li>
                    <li><b>投资策略:</b> 复杂且保密的“价差转换套利策略”。</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        st.session_state.user_decision_act1 = st.radio(
            "**你的专业判断是？**",
            ["全力投入", "大部分投入", "小部分试水", "放弃投资"],
            horizontal=True, key="decision_radio"
        )
        
        if st.button("完成判断，进入下一幕", type="primary", use_container_width=True):
            session_manager.advance_step()
            st.rerun()

    def _show_step_2_investor(self):
        st.header("第二幕: 现实击穿")
        st.progress(50, text=f"当前进度: 2/4")
        
        with st.container():
            st.markdown("""
            <div class="role-container role-investor">
                <h3>刚才你的分析，很专业。但让我告诉你一个残酷的现实。</h3>
                <p>你分析的“伯纳德·麦道夫”，就是美国历史上最大的金融诈骗犯。</p>
                <hr>
                <h4>质疑一：你为什么会信任一个“监管者”的投资能力？</h4>
                <p><b>市场监管能力 ≠ 资产管理能力。</b>你是否因为他的“光环”而降低了判断标准？</p>
                <h4>质疑二：你为什么会相信一条“不可能存在”的回报曲线？</h4>
                <p>异常的稳定，本身就是最大的风险信号。它违背了风险与收益的基本规律。</p>
            </div>
            """, unsafe_allow_html=True)
            
        col1, col2, col3 = st.columns(3)
        col1.metric("诈骗总额", "$650亿", "-100%")
        col2.metric("受害者", "37,000+", "遍及136国")
        col3.metric("诈骗时长", "20年+", "“完美”记录")

        if st.button("我明白了...进入下一步", type="primary", use_container_width=True):
            session_manager.advance_step()
            st.rerun()

    def _show_step_3_mentor(self):
        st.header("第三幕: 框架重构")
        st.progress(75, text=f"当前进度: 3/4")

        with st.container():
             st.markdown("""
            <div class="role-container role-mentor">
                <h3>你掉入了一个典型的思维陷阱——光环效应 (The Halo Effect)。</h3>
                <p>即将一个目标的某个突出优点，泛化到他所有不相关的特质上。要打破它，你需要一个强制性的“认知防火墙”。</p>
                <hr>
                <h4>四维独立验证矩阵</h4>
            </div>
            """, unsafe_allow_html=True)
        
        framework_graph = """
        digraph {
            graph [rankdir=LR, bgcolor=transparent];
            node [shape=box, style="rounded,filled", fillcolor="#E6F2FF", fontname="Lato"];
            "机会" -> "身份验证"; "机会" -> "能力验证"; "机会" -> "信息验证"; "机会" -> "独立验证";
            "身份验证" -> "决策"; "能力验证" -> "决策"; "信息验证" -> "决策"; "独立验证" -> "决策";
        }
        """
        st.graphviz_chart(framework_graph)

        if st.button("我掌握了，请给我实用的工具", type="primary", use_container_width=True):
            session_manager.advance_step()
            st.rerun()

    def _show_step_4_assistant(self):
        st.header("第四幕: 能力武装")
        st.progress(100, text="体验完成！")

        user_decision = st.session_state.get('user_decision_act1', '未知')
        
        feedback_map = {
            "全力投入": "您对权威表现出**高度信任**，需特别警惕**光环效应**。",
            "大部分投入": "您在权威面前保持了一定理性，但仍需加强**独立验证**能力。",
            "小部分试水": "您展现了优秀的风险控制意识，可尝试将流程**系统化**。",
            "放弃投资": "您具备优秀的风险嗅觉，现在需要的是**系统化的决策框架**来巩固它。"
        }
        feedback_text = feedback_map.get(user_decision, "您的决策展示了独特的思考，请持续精进。")
        
        with st.container():
            st.markdown(f"""
            <div class="role-container role-assistant">
                <h3>恭喜！你已完成本次认知升级。</h3>
                <p>基于您在第一幕中选择<b>“{user_decision}”</b>，我们的个性化提醒是：</p>
                <p><i>“{feedback_text}”</i></p>
            </div>
            """, unsafe_allow_html=True)

        card_content = """
        ### 🛡️ 高级决策安全系统
        **核心原则: 权威越强，越要验证。**
        - **身份验证:** 职位 ≠ 能力？
        - **能力验证:** 业绩可审计？
        - **信息验证:** 拒绝黑盒子？
        - **独立验证:** 有无反对意见？
        """
        st.success("您的专属工具已生成！", icon="✅")
        st.markdown(card_content)
        
        output = BytesIO(card_content.encode('utf-8'))
        st.download_button("下载决策安全卡片", output, "Decision_Card.md", "text/markdown", use_container_width=True)

        if st.button("重新开始体验", use_container_width=True):
            keys_to_clear = ['initialized', 'current_step', 'user_decision_act1', 'last_step']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    def _show_debug_sidebar(self):
        if st.sidebar.checkbox("显示调试信息"):
            st.sidebar.write(st.session_state)

def main():
    """Main function to run the application."""
    try:
        app = CognitiveBlackBoxApp()
        app.run()
    except Exception as e:
        st.error(f"应用出现严重错误: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
