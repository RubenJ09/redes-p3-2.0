from decimal import Decimal, InvalidOperation
from rules.parser import ParsedRule

class RuleEngine:
    @staticmethod
    def matches(rule: ParsedRule, current_value: str) -> bool:
        if rule.operator == "==":
            return current_value == rule.threshold

        try:
            left = Decimal(current_value)
            right = Decimal(rule.threshold)
        except (InvalidOperation, TypeError):
            return False

        if rule.operator == ">":
            return left > right
        if rule.operator == "<":
            return left < right
        return False