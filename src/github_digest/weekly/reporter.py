"""GitHub 周报生成"""
import httpx
from datetime import datetime, timedelta
from typing import List, Dict

class WeeklyReporter:
    def __init__(self, token: str, owner: str):
        self.token = token
        self.owner = owner
    
    def get_repos(self) -> List[Dict]:
        """获取仓库列表"""
        client = httpx.Client(headers={"Authorization": f"token {self.token}"})
        resp = client.get(f"https://api.github.com/users/{self.owner}/repos?per_page=100")
        return resp.json()
    
    def get_commit_stats(self, repo: str, days: int = 7) -> Dict:
        """获取提交统计"""
        since = (datetime.now() - timedelta(days=days)).isoformat()
        client = httpx.Client(headers={"Authorization": f"token {self.token}"})
        resp = client.get(
            f"https://api.github.com/repos/{self.owner}/{repo}/commits",
            params={"since": since}
        )
        commits = resp.json() or []
        return {
            "repo": repo,
            "commits": len(commits),
            "authors": list(set(c["commit"]["author"]["name"] for c in commits if c["commit"].get("author")))
        }
    
    def generate_report(self, days: int = 7) -> str:
        """生成周报"""
        repos = self.get_repos()
        stats = []
        
        for repo in repos:
            s = self.get_commit_stats(repo["name"], days)
            if s["commits"] > 0:
                stats.append(s)
        
        stats.sort(key=lambda x: x["commits"], reverse=True)
        
        md = f"""# 📊 GitHub 周报

**统计周期**: {(datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')} ~ {datetime.now().strftime('%Y-%m-%d')}

## 📈 代码改动统计

| 仓库 | 提交数 | 贡献者 |
|------|--------|--------|
"""
        for s in stats:
            md += f"| {s['repo']} | {s['commits']} | {', '.join(s['authors'][:3])} |\n"
        
        md += f"""
## 🚨 风险清单

### 🔴 高优先级
1. CI/CD 配置检查
2. 测试覆盖验证
3. 分支保护状态

### 🟡 中优先级
- 依赖版本更新
- 代码规范遵循

---
*由 GitHub Digest 自动生成*
"""
        return md
