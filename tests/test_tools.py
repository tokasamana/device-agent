# test_tools.py
import pytest
from tools import search_device, get_device_detail


class TestSearchDevice:
    """search_device 函数的测试用例"""

    def test_search_by_location(self):
        """按位置搜索"""
        results = search_device("北京")
        assert len(results) > 0
        for d in results:
            assert "北京" in d["location"]

    def test_search_by_type(self):
        """按类型搜索"""
        results = search_device("温度传感器")
        assert len(results) > 0
        for d in results:
            assert d["type"] == "温度传感器"

    def test_search_by_status(self):
        """按状态搜索"""
        results = search_device("alarm")
        assert len(results) > 0
        for d in results:
            assert d["status"] == "alarm"

    def test_search_no_match(self):
        """无匹配结果"""
        results = search_device("不存在的设备xyz")
        assert results == []

    def test_search_case_insensitive(self):
        """大小写不敏感"""
        results_upper = search_device("BJ-001")
        results_lower = search_device("bj-001")
        assert len(results_upper) == len(results_lower)


class TestGetDeviceDetail:
    """get_device_detail 函数的测试用例"""

    def test_get_existing_device(self):
        """查询存在的设备"""
        device = get_device_detail("BJ-001")
        assert device is not None
        assert device["id"] == "BJ-001"
        assert "location" in device
        assert "type" in device

    def test_get_nonexistent_device(self):
        """查询不存在的设备"""
        device = get_device_detail("ZZ-999")
        assert device is None