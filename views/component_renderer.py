def _render_ai_challenge(self, component: Dict[str, Any]) -> None:
    """
    🎯 最简化的AI质疑组件 - 确保逻辑清晰
    """
    st.subheader(component.get('title', 'AI 个性化质疑'))
    
    # 🔧 简化变量，只用布尔值控制
    ai_success = False
    ai_content = ""
    debug_messages = []
    
    # 🔧 步骤1: 尝试AI调用
    try:
        debug_messages.append("✅ 开始AI调用流程")
        
        # 导入AI引擎
        from core.ai_engine import ai_engine
        debug_messages.append("✅ AI引擎导入成功")
        
        # 构建简单的中文prompt
        user_decisions = st.session_state.get('user_decisions', {})
        simple_prompt = "请用中文对麦道夫投资案例进行四重专业质疑：1.职能边界混淆 2.信息不对称陷阱 3.统计异常忽视 4.独立尽调缺失。要求严厉专业，每个质疑至少100字。"
        
        debug_messages.append(f"✅ Prompt构建: {len(simple_prompt)} 字符")
        
        # 🔧 关键：直接调用，不使用复杂逻辑
        with st.spinner("🤖 AI正在生成质疑内容..."):
            if hasattr(ai_engine, '_call_gemini_api'):
                ai_response = ai_engine._call_gemini_api(simple_prompt)
            else:
                context = {'case_name': 'madoff', 'user_decisions': user_decisions}
                ai_response, _ = ai_engine.generate_response('investor', simple_prompt, context)
            
            debug_messages.append(f"✅ AI调用完成")
            
            # 🔧 关键：立即检查并设置
            if ai_response and len(str(ai_response).strip()) > 50:
                ai_content = str(ai_response).strip()
                ai_success = True
                debug_messages.append(f"✅ AI成功: {len(ai_content)} 字符")
            else:
                debug_messages.append(f"❌ AI失败: 回复为空或过短")
    
    except Exception as e:
        debug_messages.append(f"❌ AI调用异常: {str(e)}")
    
    # 🔧 调试信息
    with st.expander("🔧 调试信息", expanded=False):
        for msg in debug_messages:
            st.text(msg)
        if ai_content:
            st.text(f"📄 AI内容预览: {ai_content[:100]}...")
    
    # 🔧 关键：最简单的显示逻辑
    if ai_success and ai_content:
        # 只显示AI内容
        st.success("🤖 AI个性化质疑分析完成")
        st.markdown(ai_content)
    else:
        # 只显示静态内容
        st.info("😊 AI服务暂时繁忙，为您提供专业的标准分析")
        self._render_static_investor_challenges()
