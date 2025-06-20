"""
Case Selection Interface for Cognitive Black Box
Implements S's design specifications with responsive card layout
"""

import streamlit as st
from typing import Dict, List, Any

def render_case_selection_page():
    """
    Render the main case selection interface
    Following S's design specifications and Chroma-V's visual design
    """
    
    # Inject case selection specific CSS
    st.markdown("""
    <style>
        /* Case Selection UI Styles by Chroma-V */
        .case-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            padding: 2rem 0;
        }

        .case-card {
            aspect-ratio: 3 / 4;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            overflow: hidden;
            position: relative;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            background-size: cover;
            background-position: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }

        .case-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            border-color: rgba(255, 255, 255, 0.8);
        }

        .card-content {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1.5rem;
            background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.8) 70%, rgba(0,0,0,0.95) 100%);
            color: white;
        }

        .case-tag {
            background-color: rgba(255, 255, 255, 0.2);
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 0.5rem;
        }

        .case-title {
            font-size: 1.8rem;
            margin: 0.5rem 0;
            font-family: 'Georgia', serif;
            font-weight: 700;
        }

        .case-description {
            font-size: 1rem;
            opacity: 0.8;
            line-height: 1.4;
        }

        .card-action {
            margin-top: 1rem;
            font-weight: 700;
            opacity: 0;
            transform: translateY(10px);
            transition: all 0.3s ease;
            color: #FFD700;
        }

        .case-card:hover .card-action {
            opacity: 1;
            transform: translateY(0);
        }

        /* Theme backgrounds */
        .madoff-theme { 
            background: linear-gradient(135deg, rgba(42, 82, 190, 0.9), rgba(0, 0, 0, 0.7)),
                        url('https://images.unsplash.com/photo-1611174753733-e9a3a0886576?q=80&w=1887') center/cover;
        }
        
        .ltcm-theme { 
            background: linear-gradient(135deg, rgba(0, 255, 65, 0.8), rgba(0, 0, 0, 0.7)),
                        url('https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070') center/cover;
        }
        
        .coming-soon { 
            filter: grayscale(1); 
            cursor: not-allowed; 
        }
        
        .coming-soon .card-content { 
            background: linear-gradient(180deg, rgba(50,50,50,0) 0%, rgba(50,50,50,0.9) 100%);
        }

        /* Main header styles */
        .selection-header {
            text-align: center;
            margin-bottom: 3rem;
        }

        .selection-title {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #2A52BE, #059669);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }

        .selection-subtitle {
            font-size: 1.2rem;
            color: #666;
            max-width: 600px;
            margin: 0 auto;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="selection-header">
        <h1 class="selection-title">🧠 认知黑匣子</h1>
        <p class="selection-subtitle">
            通过历史上最震撼的商业失败案例，发现并修复你的认知盲区。
            每个案例18分钟，每次体验都是一次深刻的认知升级。
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Case cards using Streamlit columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_case_card(
            case_id="madoff",
            title="麦道夫案例：庞氏骗局之王",
            tag="光环效应",
            description="探索为什么最聪明的投资者也会被表面的成功蒙蔽双眼",
            theme_class="madoff-theme",
            available=True
        )
    
    with col2:
        render_case_card(
            case_id="ltcm", 
            title="LTCM案例：天才们的陨落",
            tag="过度自信",
            description="当诺贝尔奖得主的数学模型遇到现实世界的黑天鹅",
            theme_class="ltcm-theme",
            available=True
        )
    
    with col3:
        render_case_card(
            case_id="lehman",
            title="雷曼兄弟：太大而不能倒？",
            tag="系统性偏见", 
            description="158年的华尔街传奇如何在48小时内轰然倒塌",
            theme_class="coming-soon",
            available=False
        )

def render_case_card(case_id: str, title: str, tag: str, description: str, theme_class: str, available: bool):
    """
    Render individual case card
    
    Args:
        case_id: Unique identifier for the case
        title: Case title to display
        tag: Tag showing cognitive bias type
        description: Brief description of the case
        theme_class: CSS class for theme styling
        available: Whether the case is available for selection
    """
    
    card_html = f"""
    <div class="case-card {theme_class}">
        <div class="card-content">
            <span class="case-tag">{tag}</span>
            <h3 class="case-title">{title}</h3>
            <p class="case-description">{description}</p>
            <div class="card-action">
                {'点击开始体验 →' if available else '即将上线'}
            </div>
        </div>
    </div>
    """
    
    if available:
        if st.button(f"开始 {title.split('：')[0]} 案例", key=f"select_{case_id}", use_container_width=True):
            st.session_state.selected_case = case_id
            st.session_state.current_step = 1
            st.session_state.case_selection_made = True
            st.rerun()
    else:
        st.markdown(card_html, unsafe_allow_html=True)
        st.button("即将上线", disabled=True, use_container_width=True)

def get_case_metadata() -> Dict[str, Dict[str, Any]]:
    """
    Get metadata for all available cases
    
    Returns:
        Dict containing case metadata
    """
    return {
        "madoff": {
            "title": "麦道夫案例：庞氏骗局之王",
            "target_bias": "光环效应",
            "description": "探索为什么最聪明的投资者也会被表面的成功蒙蔽双眼",
            "duration_minutes": 18,
            "difficulty": "intermediate",
            "available": True
        },
        "ltcm": {
            "title": "LTCM案例：天才们的陨落", 
            "target_bias": "过度自信",
            "description": "当诺贝尔奖得主的数学模型遇到现实世界的黑天鹅",
            "duration_minutes": 18,
            "difficulty": "expert",
            "available": True
        },
        "lehman": {
            "title": "雷曼兄弟：太大而不能倒？",
            "target_bias": "系统性偏见",
            "description": "158年的华尔街传奇如何在48小时内轰然倒塌", 
            "duration_minutes": 18,
            "difficulty": "expert",
            "available": False
        }
    }
