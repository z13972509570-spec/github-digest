"""GitHub Trending 抓取"""
import urllib.request
import re

def fetch_trending(since="daily"):
    """抓取 Trending 项目"""
    req = urllib.request.Request(
        f"https://github.com/trending?since={since}",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode("utf-8")
    
    # 简单提取 h2 a 链接
    pattern = r'<h2[^>]*><a[^>]*href="(/[^/]+/[^"]+)"[^>]*>'
    matches = re.findall(pattern, html)
    
    # 去重
    projects = []
    seen = set()
    for m in matches:
        if m not in seen and not m.startswith("/orgs"):
            seen.add(m)
            projects.append(m.strip("/"))
    
    return projects[:20]

if __name__ == "__main__":
    print("=== GitHub Trending ===")
    for p in fetch_trending():
        print(f"  - {p}")
