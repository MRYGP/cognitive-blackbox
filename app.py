"""
Cognitive Black Box - Streamlit Main Application Entry
Architecture framework version - Waiting for STUDIO UI design specifications
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root directory to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Import custom modules
from utils.session_manager import session_manager
from utils.ai_roles import ai_engine
from utils.data_models import CaseType, RoleType, create_case_session

class CognitiveBlackBoxApp:
    """
    Cognitive Black Box main application class
    Responsible for overall application flow control, specific UI implementation awaits STUDIO design specifications
    """
    
    def __init__(self):
        """Initialize application"""
        self.app_title = "🧠 认知黑匣子"
        self.app_description = "18分钟认知升级体验"
        
        # Supported cases
        self.available_cases = {
            'madoff': '麦道夫庞氏骗局 - 光环效应',
            'ltcm': '长期资本管理 - 过度自信', 
            'lehman': '雷曼兄弟 - 确认偏误'
        }
        
        # Role theme configuration (awaiting STUDIO detailed specifications)
        self.role_themes = {
            'host': {'color': 'blue', 'name': '主持人'},
            'investor': {'color': 'red', 'name': '投资人'},
            'mentor': {'color': 'green', 'name': '导师'},
            'assistant': {'color': 'cyan', 'name': '助理'}
        }
    
    def run(self):
        """Run main application"""
        # Configure page basic settings
        self._configure_page()
        
        # Initialize session state
        self._initialize_session()
        
        # Show application header and description
        self._show_header()
        
        # Main application logic
        self._main_app_logic()
        
        # Show debug information (development phase)
        if st.sidebar.checkbox("显示调试信息", value=False):
            self._show_debug_info()
    
    def _configure_page(self):
        """Configure Streamlit page basic settings"""
        st.set_page_config(
            page_title=self.app_title,
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Inject basic CSS styles (awaiting STUDIO detailed style specifications)
        self._inject_base_styles()
    
    def _inject_base_styles(self):
        """Inject basic CSS styles"""
        # Only includes most basic styles, detailed role theme styles await STUDIO design
        base_css = """
        <style>
        /* Basic style framework */
        .main-header {
            text-align: center;
            padding: 2rem 0;
        }
        
        .role-container {
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .step-indicator {
            display: flex;
            justify-content: center;
            margin: 1rem 0;
        }
        
        /* Role-specific styles to be designed by STUDIO */
        .role-host { 
            /* Blue theme styles to be designed */ 
        }
        .role-investor { 
            /* Red theme styles to be designed */ 
        }
        .role-mentor { 
            /* Green theme styles to be designed */ 
        }
        .role-assistant { 
            /* Cyan theme styles to be designed */ 
        }
        
        /* Magic moment effect styles to be designed */
        .magic-moment {
            /* Effect styles to be designed by STUDIO */
        }
        </style>
        """
        
        st.markdown(base_css, unsafe_allow_html=True)
    
    def _initialize_session(self):
        """Initialize session state"""
        # Use session_manager for state management
        if not hasattr(st.session_state, 'initialized') or not st.session_state.initialized:
            # Default to using Madoff case
            success = session_manager.initialize_session('madoff')
            if success:
                st.session_state.initialized = True
                st.session_state.app_version = "0.1.0"
            else:
                st.error("应用初始化失败，请刷新页面重试")
                st.stop()
    
    def _show_header(self):
        """Show application header"""
        # Basic header structure, specific design awaits STUDIO specifications
        st.markdown(
            f"""
            <div class="main-header">
                <h1>{self.app_title}</h1>
                <p>{self.app_description}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Show progress indicator (basic version)
        self._show_progress_indicator()
    
    def _show_progress_indicator(self):
        """Show progress indicator"""
        current_step = getattr(st.session_state, 'current_step', 1)
        
        # Basic progress display, awaiting STUDIO visual design
        progress_html = f"""
        <div class="step-indicator">
            <p>当前进度: 第 {current_step}/4 步</p>
        </div>
        """
        
        st.markdown(progress_html, unsafe_allow_html=True)
    
    def _main_app_logic(self):
        """Main application logic"""
        current_step = getattr(st.session_state, 'current_step', 1)
        current_role = getattr(st.session_state, 'current_role', 'host')
        
        # Show corresponding content based on current step
        if current_step == 1:
            self._show_step_1_host()
        elif current_step == 2:
            self._show_step_2_investor()
        elif current_step == 3:
            self._show_step_3_mentor()
        elif current_step == 4:
            self._show_step_4_assistant()
        else:
            st.error(f"Unknown step: {current_step}")
    
    def _show_step_1_host(self):
        """Step 1: Host - Decision Immersion"""
        st.markdown("### 🎭 第一幕：决策代入")
        
        # Role container (awaiting STUDIO specific design)
        with st.container():
            st.markdown('<div class="role-container role-host">', unsafe_allow_html=True)
            
            # Specific interaction interface will be implemented based on STUDIO design specifications
            st.info("⏳ 等待STUDIO的UI设计规格...")
            
            # Temporary basic interaction (development phase)
            if st.button("临时：进入下一步", key="step1_next"):
                success = session_manager.advance_step()
                if success:
                    st.rerun()
                else:
                    st.error("步骤推进失败")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _show_step_2_investor(self):
        """Step 2: Investor - Reality Disruption"""
        st.markdown("### 🔥 第二幕：现实击穿")
        
        with st.container():
            st.markdown('<div class="role-container role-investor">', unsafe_allow_html=True)
            
            # "Magic moment" effect will be implemented here, awaiting STUDIO design
            st.info("⏳ 等待STUDIO的魔法时刻设计...")
            
            # Temporary interaction
            if st.button("临时：进入下一步", key="step2_next"):
                success = session_manager.advance_step()
                if success:
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _show_step_3_mentor(self):
        """Step 3: Mentor - Framework Reconstruction"""
        st.markdown("### 🧠 第三幕：框架重构")
        
        with st.container():
            st.markdown('<div class="role-container role-mentor">', unsafe_allow_html=True)
            
            st.info("⏳ 等待STUDIO的理论框架设计...")
            
            # Temporary interaction
            if st.button("临时：进入下一步", key="step3_next"):
                success = session_manager.advance_step()
                if success:
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _show_step_4_assistant(self):
        """Step 4: Assistant - Capability Armament"""
        st.markdown("### 🎯 第四幕：能力武装")
        
        with st.container():
            st.markdown('<div class="role-container role-assistant">', unsafe_allow_html=True)
            
            st.info("⏳ 等待STUDIO的工具生成设计...")
            
            # Experience completion
            st.success("🎉 18分钟认知升级体验即将完成！")
            
            if st.button("重新开始体验", key="restart"):
                # Reset session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _show_debug_info(self):
        """Show debug information (development phase)"""
        st.sidebar.markdown("## 🔧 调试信息")
        
        # Session summary
        session_summary = session_manager.get_session_summary()
        st.sidebar.json(session_summary)
        
        # Current context
        current_context = session_manager.get_current_context()
        st.sidebar.markdown("### 当前上下文")
        st.sidebar.json(current_context)
        
        # API status
        available_apis = ai_engine.get_available_apis()
        st.sidebar.markdown("### API状态")
        st.sidebar.write(f"可用API: {available_apis}")
        
        # Cache status
        cache_stats = ai_engine.get_cache_stats()
        st.sidebar.markdown("### 缓存状态")
        st.sidebar.json(cache_stats)
        
        # Manual controls
        st.sidebar.markdown("### 手动控制")
        if st.sidebar.button("清空缓存"):
            ai_engine.clear_cache()
            st.sidebar.success("缓存已清空")
        
        if st.sidebar.button("重置会话"):
            session_manager.initialize_session()
            st.sidebar.success("会话已重置")
    
    def _test_ai_integration(self):
        """Test AI integration (development phase)"""
        st.sidebar.markdown("### 🤖 AI测试")
        
        test_role = st.sidebar.selectbox(
            "选择角色",
            ['host', 'investor', 'mentor', 'assistant']
        )
        
        test_input = st.sidebar.text_input("测试输入", "你好")
        
        if st.sidebar.button("测试AI响应"):
            context = session_manager.get_current_context()
            response, success = ai_engine.generate_response(
                test_role, 
                test_input, 
                context
            )
            
            if success:
                st.sidebar.success("AI响应成功")
                st.sidebar.write(response)
            else:
                st.sidebar.error("AI响应失败")
                st.sidebar.write(response)

def main():
    """Main function"""
    try:
        app = CognitiveBlackBoxApp()
        app.run()
    except Exception as e:
        st.error(f"应用运行错误: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
