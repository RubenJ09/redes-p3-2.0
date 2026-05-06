"""Parser controlado para reglas en texto libre."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ParsedRule:
    source_device: str
    operator: str
    threshold: str
    action_device: str
    action_value: str


_OPERATOR_MAP = {
    ">": ">",
    "<": "<",
    "==": "==",
    "mayor que": ">",
    "menor que": "<",
    "igual a": "==",
}


def parse_rule_text(rule_text: str) -> ParsedRule:
    """Parsea reglas del tipo: si X mayor que 25 entonces Y OFF."""

    pattern = re.compile(
        r"^si\s+(?P<source>.+?)\s+(?P<operator>==|>|<|mayor que|menor que|igual a)\s+(?P<threshold>.+?)\s+entonces\s+(?P<action_device>\S+)\s+(?P<action_value>.+)$",
        re.IGNORECASE,
    )
    match = pattern.match(rule_text.strip())
    if not match:
        raise ValueError("Formato de regla no válido")

    operator = _OPERATOR_MAP[match.group("operator").lower()]
    return ParsedRule(
        source_device=match.group("source").strip(),
        operator=operator,
        threshold=match.group("threshold").strip(),
        action_device=match.group("action_device").strip(),
        action_value=match.group("action_value").strip(),
    )