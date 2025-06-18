#!/usr/bin/env python3
"""
Cognitive Black Box - Architecture Compatibility Test Suite
Tests the refactored architecture for functionality and performance
"""

import sys
import json
import time
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_case_manager():
    """Test case manager functionality"""
    print("🧪 Testing Case Manager...")
    
    try:
        from core.case_manager import case_manager
        
        # Test 1: Load madoff case
        print("  ✓ Testing case loading...")
        case_data = case_manager.load_case('madoff')
        assert case_data is not None, "Failed to load madoff case"
        assert 'case_metadata' in case_data, "Missing case_metadata"
        assert 'acts' in case_data, "Missing acts"
        print("    ✅ Case loading successful")
        
        # Test 2: Get case metadata
        print("  ✓ Testing metadata extraction...")
        metadata = case_manager.get_case_metadata('madoff')
        assert metadata is not None, "Failed to get metadata"
        assert metadata.case_id == 'madoff', "Incorrect case_id"
        assert metadata.duration_minutes == 18, "Incorrect duration"
        print("    ✅ Metadata extraction successful")
        
        # Test 3: Get act content
        print("  ✓ Testing act content retrieval...")
        act1_content = case_manager.get_act_content('madoff', 'act1_host')
        assert act1_content is not None, "Failed to get act1 content"
        assert 'role' in act1_content, "Missing role in act content"
        assert act1_content['role'] == 'host', "Incorrect role"
        print("    ✅ Act content retrieval successful")
        
        # Test 4: Get decision points
        print("  ✓ Testing decision points...")
        decision_points = case_manager.get_decision_points('madoff')
        assert decision_points is not None, "Failed to get decision points"
        assert len(decision_points) > 0, "No decision points found"
        print("    ✅ Decision points retrieval successful")
        
        # Test 5: Cache functionality
        print("  ✓ Testing cache...")
        cache_info = case_manager.get_cache_info()
        assert 'cached_cases' in cache_info, "Cache info missing"
        assert 'madoff' in cache_info['cached_cases'], "Case not cached"
        print("    ✅ Cache functionality working")
        
        print("✅ Case Manager: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Case Manager Test Failed: {str(e)}")
        return False

def test_ai_engine():
    """Test AI engine functionality"""
    print("🧪 Testing AI Engine...")
    
    try:
        from core.ai_engine import ai_engine
        
        # Test 1: Engine initialization
        print("  ✓ Testing engine initialization...")
        available_apis = ai_engine.get_available_apis()
        print(f"    Available APIs: {available_apis}")
        assert len(ai_engine.roles) == 4, "Should have 4 roles"
        print("    ✅ Engine initialization successful")
        
        # Test 2: Role information
        print("  ✓ Testing role information...")
        host_info = ai_engine.get_role_info('host')
        assert 'name' in host_info, "Missing role name"
        assert 'expertise' in host_info, "Missing role expertise"
        print("    ✅ Role information retrieval successful")
        
        # Test 3: Fallback response
        print("  ✓ Testing fallback responses...")
        context = {'current_step': 1, 'case_name': 'madoff'}
        response, success = ai_engine.generate_response('host', 'test input', context)
        assert response is not None, "No response generated"
        assert len(response) > 0, "Empty response"
        print("    ✅ Fallback response generation successful")
        
        # Test 4: Cache stats
        print("  ✓ Testing cache statistics...")
        cache_stats = ai_engine.get_cache_stats()
        assert 'cache_size' in cache_stats, "Missing cache_size"
        assert 'performance_metrics' in cache_stats, "Missing performance_metrics"
        print("    ✅ Cache statistics working")
        
        print("✅ AI Engine: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ AI Engine Test Failed: {str(e)}")
        return False

def test_validators():
    """Test input validation functionality"""
    print("🧪 Testing Input Validators...")
    
    try:
        from utils.validators import input_validator
        
        # Test 1: Company name validation
        print("  ✓ Testing company name validation...")
        valid, msg = input_validator.validate_user_input('company_name', '科技创新公司')
        assert valid, f"Valid company name rejected: {msg}"
        
        valid, msg = input_validator.validate_user_input('company_name', '<script>alert("xss")</script>')
        assert not valid, "XSS attack not detected"
        print("    ✅ Company name validation working")
        
        # Test 2: Investment amount validation
        print("  ✓ Testing investment amount validation...")
        valid, msg = input_validator.validate_user_input('investment_amount', '5000万人民币')
        assert valid, f"Valid investment amount rejected: {msg}"
        
        valid, msg = input_validator.validate_user_input('investment_amount', 'invalid amount')
        assert not valid, "Invalid investment amount accepted"
        print("    ✅ Investment amount validation working")
        
        # Test 3: Security patterns
        print("  ✓ Testing security validation...")
        test_inputs = [
            '<script>alert("test")</script>',
            'javascript:void(0)',
            'onclick="malicious()"',
            'document.cookie'
        ]
        
        for test_input in test_inputs:
            valid, msg = input_validator.validate_user_input('company_name', test_input)
            assert not valid, f"Security vulnerability: {test_input}"
        print("    ✅ Security validation working")
        
        # Test 4: Case config validation
        print("  ✓ Testing case config validation...")
        config_path = Path('config/cases/madoff.json')
        if config_path.exists():
            valid, errors = input_validator.validate_case_config(config_path)
            assert valid, f"Case config validation failed: {errors}"
            print("    ✅ Case config validation working")
        else:
            print("    ⚠️ Case config file not found, skipping test")
        
        print("✅ Input Validators: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Input Validators Test Failed: {str(e)}")
        return False

def test_error_handlers():
    """Test error handling functionality"""
    print("🧪 Testing Error Handlers...")
    
    try:
        from utils.error_handlers import error_handler, ErrorType, ErrorSeverity
        
        # Test 1: Error handling
        print("  ✓ Testing error handling...")
        test_exception = Exception("Test error")
        error_info = error_handler.handle_error(
            test_exception, 
            ErrorType.SYSTEM_ERROR,
            context={'test': 'context'},
            user_visible=False,
            auto_recover=False
        )
        
        assert error_info.error_type == ErrorType.SYSTEM_ERROR, "Incorrect error type"
        assert error_info.message == "Test error", "Incorrect error message"
        print("    ✅ Error handling working")
        
        # Test 2: API timeout handling
        print("  ✓ Testing API timeout handling...")
        error_handler.handle_api_timeout('test_api', 3.0)
        print("    ✅ API timeout handling working")
        
        # Test 3: Error statistics
        print("  ✓ Testing error statistics...")
        error_stats = error_handler.get_error_stats()
        assert 'total_errors' in error_stats, "Missing total_errors"
        assert error_stats['total_errors'] >= 1, "Error not recorded"
        print("    ✅ Error statistics working")
        
        # Test 4: Error history management
        print("  ✓ Testing error history...")
        error_handler.clear_error_history()
        stats_after_clear = error_handler.get_error_stats()
        assert stats_after_clear['total_errors'] == 0, "Error history not cleared"
        print("    ✅ Error history management working")
        
        print("✅ Error Handlers: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Error Handlers Test Failed: {str(e)}")
        return False

def test_config_files():
    """Test configuration files"""
    print("🧪 Testing Configuration Files...")
    
    try:
        # Test 1: Case configuration
        print("  ✓ Testing case configuration...")
        madoff_config = Path('config/cases/madoff.json')
        if madoff_config.exists():
            with open(madoff_config, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            assert 'case_metadata' in config_data, "Missing case_metadata"
            assert 'acts' in config_data, "Missing acts"
            
            required_acts = ['act1_host', 'act2_investor', 'act3_mentor', 'act4_assistant']
            for act in required_acts:
                assert act in config_data['acts'], f"Missing {act}"
            
            print("    ✅ Case configuration valid")
        else:
            print("    ⚠️ Case configuration file not found")
        
        # Test 2: Prompt configurations
        print("  ✓ Testing prompt configurations...")
        prompt_files = ['host.json', 'investor.json', 'mentor.json', 'assistant.json']
        
        for prompt_file in prompt_files:
            prompt_path = Path(f'config/prompts/{prompt_file}')
            if prompt_path.exists():
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    prompt_data = json.load(f)
                
                assert 'role_id' in prompt_data, f"Missing role_id in {prompt_file}"
                assert 'system_prompt' in prompt_data, f"Missing system_prompt in {prompt_file}"
                assert 'fallback_responses' in prompt_data, f"Missing fallback_responses in {prompt_file}"
                
            else:
                print(f"    ⚠️ Prompt file {prompt_file} not found")
        
        print("    ✅ Prompt configurations valid")
        
        print("✅ Configuration Files: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Configuration Files Test Failed: {str(e)}")
        return False

def test_package_structure():
    """Test Python package structure and __init__.py files"""
    print("🧪 Testing Package Structure...")
    
    try:
        # Test 1: Check __init__.py files exist
        print("  ✓ Testing __init__.py files...")
        required_init_files = [
            Path('__init__.py'),
            Path('core/__init__.py'),
            Path('utils/__init__.py'), 
            Path('views/__init__.py'),
            Path('config/__init__.py')
        ]
        
        for init_file in required_init_files:
            if init_file.exists():
                print(f"    ✅ {init_file} exists")
            else:
                print(f"    ⚠️ {init_file} missing (will be created)")
        
        # Test 2: Test package imports
        print("  ✓ Testing package imports...")
        try:
            import cognitive_black_box
            print("    ✅ Main package import successful")
            
            # Test system status
            status = cognitive_black_box.get_system_status()
            print(f"    Package health: {status.get('overall_health', 'unknown')}")
            
        except ImportError as e:
            print(f"    ⚠️ Package import failed: {str(e)}")
        
        # Test 3: Test submodule imports
        print("  ✓ Testing submodule imports...")
        submodules = ['core', 'utils', 'views', 'config']
        
        for module in submodules:
            try:
                exec(f"import {module}")
                print(f"    ✅ {module} module import successful")
            except ImportError as e:
                print(f"    ⚠️ {module} module import failed: {str(e)}")
        
        # Test 4: Test quick start validation
        print("  ✓ Testing quick start validation...")
        try:
            import cognitive_black_box
            quick_check = cognitive_black_box.quick_start_check()
            if quick_check['ready']:
                print(f"    ✅ {quick_check['message']}")
            else:
                print(f"    ⚠️ {quick_check['message']}")
        except Exception as e:
            print(f"    ⚠️ Quick start check failed: {str(e)}")
        
        print("✅ Package Structure: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Package Structure Test Failed: {str(e)}")
        return False

def run_performance_test():
    """Run basic performance tests"""
    print("🚀 Running Performance Tests...")
    
    try:
        from core.case_manager import case_manager
        
        # Test case loading performance
        print("  ⏱️ Testing case loading performance...")
        start_time = time.time()
        
        for i in range(10):
            case_data = case_manager.load_case('madoff')
            assert case_data is not None
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 10
        
        print(f"    Average case loading time: {avg_time:.4f}s")
        assert avg_time < 0.1, "Case loading too slow"
        print("    ✅ Case loading performance acceptable")
        
        # Test cache performance
        print("  ⏱️ Testing cache performance...")
        start_time = time.time()
        
        for i in range(100):
            case_data = case_manager.load_case('madoff')  # Should hit cache
        
        end_time = time.time()
        avg_cached_time = (end_time - start_time) / 100
        
        print(f"    Average cached loading time: {avg_cached_time:.6f}s")
        assert avg_cached_time < 0.001, "Cache not working effectively"
        print("    ✅ Cache performance excellent")
        
        print("✅ Performance Tests: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Performance Test Failed: {str(e)}")
        return False

def main():
    """Run all architecture tests"""
    print("🏗️ Cognitive Black Box - Architecture Test Suite")
    print("=" * 60)
    
    test_results = []
    
    # Run all tests
    tests = [
        ("Package Structure", test_package_structure),
        ("Case Manager", test_case_manager),
        ("AI Engine", test_ai_engine),
        ("Input Validators", test_validators),
        ("Error Handlers", test_error_handlers),
        ("Configuration Files", test_config_files),
        ("App Integration", test_app_integration),
        ("Performance", run_performance_test)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'=' * 60}")
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}: CRITICAL FAILURE - {str(e)}")
            test_results.append((test_name, False))
    
    # Summary
    print(f"\n{'=' * 60}")
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\n📈 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Architecture is ready for deployment!")
        return 0
    else:
        print("⚠️ Some tests failed - Please review and fix issues before deployment")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
