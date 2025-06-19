def _render_ai_tool_generation(self, component: Dict[str, Any]) -> None:
        """
        🔧 P0 FIXED: Enhanced AI tool generation with improved prompt and context
        """
        st.subheader(component.get('title', '定制您的专属决策系统'))
        
        ai_config = component.get('ai_config', {})
        
        # 🔧 ENHANCED: Better user input collection
        st.markdown("#### 为您的决策系统命名")
        user_system_name = st.text_input(
            "给您的决策系统起个名字：",
            value=st.session_state.get('user_system_name', '高级决策安全系统'),
            key='user_system_name_input'
        )
        st.session_state.user_system_name = user_system_name
        
        st.markdown("#### 确定您的核心原则")
        user_core_principle = st.text_input(
            "用一句话描述您的核心决策原则：",
            value=st.session_state.get('user_core_principle', '权威越强，越要验证'),
            key='user_core_principle_input'
        )
        st.session_state.user_core_principle = user_core_principle
        
        # 🔧 ENHANCED: Show what will be generated
        with st.expander("📋 预览：您将获得什么", expanded=False):
            st.markdown("""
            **您的专属决策系统将包含：**
            - 🎯 个性化的决策验证清单
            - 🔍 基于您经历设计的风险识别工具  
            - 🛡️ 针对您决策模式的预警系统
            - 📊 可立即使用的决策评估矩阵
            - 📚 实施指导和使用建议
            """)
        
        if st.button("🚀 生成我的专属决策系统", type="primary", use_container_width=True):
            # 🔧 P0 FIXED: Build comprehensive context with all required fields
            context = {
                'current_step': st.session_state.get('current_step', 4),
                'case_name': 'madoff',
                'user_system_name': user_system_name,
                'user_core_principle': user_core_principle,
                'user_decisions': st.session_state.get('user_decisions', {}),
                'user_background': self._infer_user_background(),
                'session_insights': self._extract_session_insights(),
                'capability_test_response': st.session_state.get('capability_test_response', ''),
                'personalization_active': st.session_state.get('personalization_active', True)
            }
            
            # 🔧 P0 FIXED: Improved prompt construction
            enhanced_prompt = f"""
请为用户设计一个完整的个性化决策安全系统。

**用户信息：**
- 系统名称：{user_system_name}
- 核心原则：{user_core_principle}
- 决策背景：{context.get('user_background', '高级管理者')}

**用户在麦道夫案例中的决策表现：**
{self._summarize_user_decisions(context.get('user_decisions', {}))}

**设计要求：**
1. 系统必须体现用户的核心原则："{user_core_principle}"
2. 针对用户在案例中的决策模式进行个性化设计
3. 提供立即可用的检查清单、评估工具和实施指导
4. 内容要专业、实用、易于在实际工作中应用
5. 确保系统名称"{user_system_name}"贯穿整个设计

请生成一个完整的、个性化的决策安全系统，包含：
- 🎯 核心决策原则
- 🔍 四维验证清单
- ⚖️ 杠铃风险管理策略
- ⚠️ 高危信号预警系统
- 🎯 认知升级要点

格式要求：使用Markdown格式，结构清晰，便于下载和使用。
"""
            
            with st.spinner("🤖 AI正在基于您的决策模式，量身定制专属系统..."):
                ai_tool_content, success = ai_engine.generate_response(
                    'assistant',
                    enhanced_prompt,
                    context
                )
            
            if success:
                st.success("🎉 您的专属决策系统已生成完成！")
                
                # 🔧 NEW: Add system info display
                st.info(f"**系统名称**: {user_system_name}  \n**核心原则**: {user_core_principle}")
                
                # Show the generated content
                st.markdown(ai_tool_content)
                
                # 🔧 ENHANCED: Better download options
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 下载完整系统 (Markdown)",
                        data=ai_tool_content,
                        file_name=f"{user_system_name.replace(' ', '_')}_决策系统.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                with col2:
                    # Create a simple checklist version
                    checklist_content = self._extract_checklist_from_content(ai_tool_content, user_system_name)
                    st.download_button(
                        label="📋 下载检查清单 (TXT)",
                        data=checklist_content,
                        file_name=f"{user_system_name.replace(' ', '_')}_检查清单.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                # 🔧 NEW: Usage encouragement
                st.markdown("---")
                st.success("💡 **建议**：请将这套系统保存到您的手机或电脑中，在下次面临重要决策时立即使用！")
                
            else:
                st.warning("⚠️ AI服务暂时繁忙，为您提供专业的通用系统模板")
                # 🔧 ENHANCED: Better fallback content
                self._render_enhanced_fallback_tool(user_system_name, user_core_principle)
