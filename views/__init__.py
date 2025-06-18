"""
Cognitive Black Box - Views Module Package
Contains component-based rendering system based on S's Schema design
"""

__version__ = "2.0.0"
__author__ = "Claude (C) - Architecture Team"
__description__ = "View layer implementing S's component-based architecture"

# Import view components
try:
    from .component_renderer import component_renderer, ComponentRenderer
    
    __all__ = [
        'component_renderer',
        'ComponentRenderer'
    ]
    
    _VIEWS_MODULES_LOADED = True
    
except ImportError as e:
    _VIEWS_MODULES_LOADED = False
    _IMPORT_ERROR = str(e)
    
    # Provide fallback renderer
    class _FallbackRenderer:
        def __init__(self):
            self.available = False
            
        def render_act(self, act_data):
            """Fallback render method"""
            import streamlit as st
            st.error("组件渲染器暂不可用，请检查系统配置")
            return False
        
        def render_component(self, component):
            """Fallback component render"""
            import streamlit as st
            component_type = component.get('component_type', 'unknown')
            st.warning(f"组件类型 '{component_type}' 渲染器不可用")
    
    component_renderer = _FallbackRenderer()
    __all__ = ['component_renderer']

def get_module_status():
    """Get status of views module loading"""
    if _VIEWS_MODULES_LOADED:
        return {
            'status': 'success',
            'message': 'Views module loaded successfully',
            'component_renderer_available': True,
            'supported_components': _get_supported_components()
        }
    else:
        return {
            'status': 'error',
            'message': f'Views module loading failed: {_IMPORT_ERROR}',
            'fallback_active': True,
            'component_renderer_available': False
        }

def _get_supported_components():
    """Get list of supported component types"""
    if _VIEWS_MODULES_LOADED:
        try:
            # Get supported components from renderer
            return list(component_renderer.component_renderers.keys())
        except:
            return []
    else:
        return []

def validate_component_support(component_type):
    """Check if a component type is supported"""
    if not _VIEWS_MODULES_LOADED:
        return False
    
    try:
        supported = _get_supported_components()
        return component_type in supported
    except:
        return False

def get_renderer_info():
    """Get detailed renderer information"""
    info = {
        'version': __version__,
        'loaded': _VIEWS_MODULES_LOADED,
        'fallback_active': not _VIEWS_MODULES_LOADED
    }
    
    if _VIEWS_MODULES_LOADED:
        try:
            info.update({
                'supported_components': _get_supported_components(),
                'theme_colors_available': hasattr(component_renderer, 'theme_colors'),
                'magic_moments_support': True
            })
        except:
            info['initialization_error'] = True
    
    return info
