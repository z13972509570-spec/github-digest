"""风险分析器"""
from typing import List

class RiskAnalyzer:
    def analyze(self, repos: List[dict]) -> List[dict]:
        risks = []
        for repo in repos:
            if not repo.get("has_wiki"):
                risks.append({
                    "level": "MEDIUM",
                    "title": "CI/CD 未配置",
                    "description": f"{repo['name']} 可能缺少自动化流程"
                })
        return risks
