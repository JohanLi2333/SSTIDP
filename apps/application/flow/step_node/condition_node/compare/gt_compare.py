# coding=utf-8
"""
@project: maxkb
@Author：虎
@file： lt_compare.py
@date：2024/6/11 9:52
@desc: 大于比较器
"""

from typing import List

from application.flow.step_node.condition_node.compare.compare import Compare


class GTCompare(Compare):
    def support(self, node_id, fields: List[str], source_value, compare, target_value):
        if compare == "gt":
            return True

    def compare(self, source_value, compare, target_value):
        try:
            return float(source_value) > float(target_value)
        except Exception:
            return False
