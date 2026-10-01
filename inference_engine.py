# inference_engine.py
from rules import RULES, extract_all_conditions

class InferenceEngine:
    def __init__(self, device="pc"):
        self.all_rules = RULES
        self.device = device
        self.rules = []
        self.all_conditions = []
        self.set_device(device)

    def set_device(self, device):
        """Переключает фильтр по типу устройства: 'pc' или 'laptop'."""
        self.device = device
        self.rules = [r for r in self.all_rules
                      if r.get("device") in (device, "both")]
        self.all_conditions = extract_all_conditions(self.rules)

    def diagnose_from_facts(self, facts):
        """
        Возвращает список словарей с правилами и процентом совпадения.
        Сортирует по убыванию процента.
        """
        result = []
        for rule in self.rules:
            total = len(rule["conditions"])
            if total == 0:
                continue
            matched = sum(1 for cond in rule["conditions"] if cond in facts)
            percent = int((matched / total) * 100)
            if matched > 0:
                result.append({
                    "rule": rule,
                    "matched": matched,
                    "total": total,
                    "percent": percent
                })
        result.sort(key=lambda x: x["percent"], reverse=True)
        return result
