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
                st.error("应用初始化失败,请刷新页面重试")
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
        st.markdown("### 🎭 第一幕:决策代入")
        st.progress(25, text="当前进度: 1/4")
        
        # Opening content
        opening_content = """
        ### 你好,决策者。
        
        我知道你身经百战,每一个决策都可能定义一个公司的未来。
        
        今天,我想与你分享一个 **价值650亿美元的教训**。这不是一个遥远的故事,而是一面镜子。
        
        ---
        
        2008年,华尔街爆出惊天丑闻:**前纳斯达克主席**,被自己的儿子举报涉嫌金融诈骗。受害者名单,让世界为之震惊...
        """
        
        with st.container():
            st.markdown('<div class="role-container role-host">', unsafe_allow_html=True)
            st.markdown(opening_content)
            
            # Investment opportunity
            opportunity_content = """
            ### 投资机会档案
            
            让我们回到2005年。假设你正在为公司寻找一个稳健的投资机会,来配置 **3000万美元** 的资金。
            
            **🎯 投资机会档案:**
            
            - **基金经理:** 伯纳德·麦道夫,前纳斯达克股票市场公司董事会主席
            - **历史业绩:** 过去15年,年均回报稳定在10-12%,波动极小
            - **客户构成:** 欧洲皇室、好莱坞明星、华尔街各大银行
            - **投资策略:** 复杂且保密的"价差转换套利策略"
            - **准入门槛:** 最低投资100万美元,需要推荐人引荐
            """
            st.markdown(opportunity_content)
            
            # Simple decision question
            st.subheader("你的专业判断是？")
            if 'user_decision' not in st.session_state:
                st.session_state.user_decision = None
                
            st.session_state.user_decision = st.radio(
                "基于以上信息,你的投资意向是？",
                ["全力投入", "大部分投入", "小部分试水", "放弃投资"],
                horizontal=True
            )
            
            if st.button("完成判断,进入下一幕", type="primary", use_container_width=True):
                success = session_manager.advance_step()
                if success:
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _show_step_2_investor(self):
        """Step 2: Investor - Reality Disruption"""
        st.markdown("### 🔥 第二幕:现实击穿")
        st.progress(50, text="当前进度: 2/4")
        
        with st.container():
            st.markdown('<div class="role-container role-investor">', unsafe_allow_html=True)
            
            # Harsh reality
            intro_content = """
            ### 刚才你的分析,很专业。但让我告诉你一个残酷的现实。
            
            你刚才分析的 "伯纳德·麦道夫",就是美国历史上最大的金融诈骗犯。
            
            **650亿美元！** 这是确认的诈骗总金额。
            
            **37,000名受害者**,遍及136个国家。
            
            你的所有判断,都基于一个精心编织了20年的谎言。
            """
            st.markdown(intro_content)
            
            st.subheader("现在,让我用投资人的视角,问你四个专业问题:")
            
            # Four questions
            # Get user's decision for dynamic questioning
            user_decision = getattr(st.session_state, 'user_decision', '未知')
            
            # Dynamic first question based on user's choice
            if user_decision in ["全力投入", "大部分投入"]:
                question_1 = f"""
                #### 质疑一:我注意到你刚才选择了【{user_decision}】
                
                你因为"前纳斯达克主席"的头衔就给予了高度信任。但请问:**市场监管能力 ≠ 资产管理能力。**
                
                这就像你认为"顶级裁判"一定是"顶级球员"一样荒谬。你的选择【{user_decision}】恰恰证明了职位光环对你的强大影响力。
                
                **你为什么会让一个监管者的光环,降低了你的投资判断标准？**
                """
            else:
                question_1 = f"""
                #### 质疑一:你选择了【{user_decision}】,但让我问你
                
                即使你保持了谨慎,但你的谨慎是基于什么？是系统性的分析框架,还是某种"直觉"？
                
                事实是,连那些选择谨慎的投资者,也有很多人被麦道夫骗了20年。**谨慎不等于免疫光环效应。**
                
                **真正的问题是:你知道如何系统性地识别权威陷阱吗？**
                """
            
            questions = [
                question_1,  # 动态的第一个质疑
                """
                #### 质疑二:你为什么会相信一条"不可能存在"的回报曲线？
                
                15年稳定在10-12%的收益？连巴菲特在熊市都会亏损超过30%！市场有周期,风险是常态,这是金融常识。
                
                一条几十年"不回调"的收益曲线,在统计学上只有一种可能:**庞氏骗局。** 它是用新投资者的钱,支付给老投资者。
                
                **你为什么忽视了这个最明显的数学警报？**
                """,
                """
                #### 质疑三:你为什么会接受一个完全不透明的"黑盒子"？
                
                你接受了"策略保密"的说辞。但麦道夫拒绝任何第三方审计,甚至拒绝分离客户资金的托管。
                
                这在专业投资领域是最高级别的危险信号。**真正的投资大师分享的是原则和哲学,而骗子才需要绝对的黑盒来隐藏他们的空无一物。**
                
                **你为什么放弃了作为决策者最基本的"尽职调查"权利？**
                """,
                """
                #### 质疑四:你为什么会让"别人"替你思考？
                
                你看到了顶级银行和名人的背书,就放松了警惕。但事实是,他们也和你一样,看到了同样的光环,听了同样的故事,犯了同样的错误。
                
                当所有人都依赖他人的判断时,这不是"集体智慧",而是"集体催眠"。
                
                **现在我问你:连这些世界顶级的聪明人都被骗了,你凭什么认为自己能幸免？**
                """
            ]
            
            for i, question in enumerate(questions, 1):
                with st.expander(f"展开质疑 {i}", expanded=True):
                    st.markdown(question)
            
            # Shock data
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("总损失", "650亿美元", delta="-100%")
            with col2:
                st.metric("受害者", "37,000人", delta="+136个国家")
            with col3:
                st.metric("诈骗时长", "20年", delta="完美记录")
            
            if st.button("我明白了...进入下一步,学习如何防范", type="primary", use_container_width=True):
                success = session_manager.advance_step()
                if success:
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _show_step_3_mentor(self):
        """Step 3: Mentor - Framework Reconstruction"""
        st.markdown("### 🧠 第三幕:框架重构")
        st.progress(75, text="当前进度: 3/4")
        
        with st.container():
            st.markdown('<div class="role-container role-mentor">', unsafe_allow_html=True)
            
            intro_content = """
            ### 你刚才的经历,在认知科学中有一个精确的名字。
            
            你并不是愚蠢,也不是不专业。你只是和全世界所有最聪明的人一样,掉入了同一个思维陷阱——**光环效应 (The Halo Effect)**。
            
            这个概念由心理学大师 **爱德华·桑代克** 早在1920年就已发现:**我们的大脑,会让我们将一个目标的某个突出优点,不自觉地泛化到他所有不相关的特质上。**
            
            麦道夫用他耀眼的"光环",让你关闭了本该开启的"怀疑"引擎。
            """
            st.markdown(intro_content)
            
            framework_content = """
            ### 如何打破"光环"？你需要一个强制性的"认知防火墙"。
            
            面对任何看似完美的权威或机会,你必须启动一套不依赖直觉的、系统性的验证流程。我称之为 **"四维独立验证矩阵"**。
            
            **四个关键维度:**
            
            🔍 **维度1: 身份验证** - 职位 ≠ 能力,监管者未必是好的投资者
            
            📊 **维度2: 能力验证** - 业绩必须可审计,拒绝"商业机密"
            
            🔍 **维度3: 信息验证** - 拒绝黑盒子操作,要求合理透明度
            
            🎯 **维度4: 独立验证** - 主动寻找反对意见和失败案例
            """
            st.markdown(framework_content)
            
            if st.button("我掌握了。请给我实用的工具", type="primary", use_container_width=True):
                success = session_manager.advance_step()
                if success:
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _show_step_4_assistant(self):
        """Step 4: Assistant - Capability Armament"""
        st.markdown("### 🎯 第四幕:能力武装")
        st.progress(100, text="体验即将完成: 4/4")
        
        with st.container():
            st.markdown('<div class="role-container role-assistant">', unsafe_allow_html=True)
            
            # Personalized feedback
            # Enhanced personalized feedback
            user_decision = getattr(st.session_state, 'user_decision', '未知')
            
            # Generate personalized feedback based on user's choice
            feedback_text = ""
            warning_level = ""
            
            if user_decision == "全力投入":
                feedback_text = """
                **⚠️ 高风险偏好特征识别**
                
                您在面对麦道夫这样的"完美机会"时选择了**全力投入**,这表明:
                - 您对权威身份的信任度很高
                - 您容易被"完美"的历史业绩吸引
                - 您需要特别警惕**光环效应**的影响
                
                **个性化建议**:未来遇到类似机会时,强制自己等待48小时再做决定。
                """
                warning_level = "高度警惕"
                
            elif user_decision == "大部分投入":
                feedback_text = """
                **📊 中高风险偏好特征**
                
                您选择了**大部分投入**,说明您在权威面前保持了一定理性,但仍然:
                - 容易被权威身份影响判断
                - 对"稳定收益"的吸引力较高
                - 需要加强**独立验证**能力
                
                **个性化建议**:建立"魔鬼代言人"机制,每个重大决策前找人唱反调。
                """
                warning_level = "适度警惕"
                
            elif user_decision == "小部分试水":
                feedback_text = """
                **✅ 谨慎型决策特征**
                
                您选择了**小部分试水**,展现了优秀的风险控制意识:
                - 对权威身份保持了相对理性
                - 具备一定的**怀疑精神**
                - 已经有了基本的风险分散概念
                
                **个性化建议**:继续保持这种谨慎,并系统化您的验证流程。
                """
                warning_level = "继续保持"
                
            elif user_decision == "放弃投资":
                feedback_text = """
                **🛡️ 高警惕性决策特征**
                
                您选择了**放弃投资**,说明您具备了优秀的风险嗅觉:
                - 对"完美机会"保持了高度警惕
                - 不容易被权威身份迷惑
                - 具备强烈的**独立思考**能力
                
                **个性化建议**:您的直觉很好,现在需要的是系统化的决策框架。
                """
                warning_level = "优秀水平"
            
            personalized_intro = f"""
            ### 🎯 基于您的选择的个性化分析
            
            **您的选择:{user_decision}**
            **风险警惕等级:{warning_level}**
            
            {feedback_text}
            """
            st.markdown(personalized_intro)
            """
            st.markdown(feedback_content)
            
            # Decision safety card
            # Decision safety card
            card_content = """### 🛡️ 高级决策安全系统

**核心原则: 权威越强越要验证, 机会越好越要谨慎**

#### 🔍 四维独立验证矩阵

**1. 身份验证:** 权威与能力是否匹配?
**2. 能力验证:** 业绩是否有第三方审计?
**3. 信息验证:** 是否要求接受黑盒子?
**4. 独立验证:** 是否寻找了反对意见?

#### ⚠️ 高危信号预警

- 这是商业机密无法透露
- 所有聪明人都在参与
- 过于完美的历史业绩曲线
- 拒绝第三方审计或托管

**智慧不是永不犯错而是在代价昂贵之前获得免疫力**"""
            
            st.success(card_content)
            st.balloons()
            
            if st.button("重新开始体验", use_container_width=True):
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
