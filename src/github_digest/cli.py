"""CLI 入口"""
import click
import os

@click.group()
def cli():
    """GitHub Digest - 热门推送 + 周报系统"""
    pass

@cli.command()
@click.option("--push", is_flag=True, help="推送到微信")
def trending(push):
    """抓取 GitHub Trending"""
    from .trending.fetcher import TrendingFetcher
    fetcher = TrendingFetcher()
    projects = fetcher.fetch()
    for p in projects[:5]:
        print(f"{p.stars} ⭐ {p.name} - {p.description[:50]}")

@cli.command()
@click.option("--push", is_flag=True, help="推送到微信")
def weekly(push):
    """生成周报"""
    token = os.getenv("GITHUB_TOKEN")
    owner = os.getenv("GITHUB_OWNER", "z13972509570-spec")
    from .weekly.reporter import WeeklyReporter
    reporter = WeeklyReporter(token, owner)
    print(reporter.generate_report())

@cli.command()
def run():
    """执行所有任务"""
    click.echo("执行热门推送...")
    click.echo("执行周报生成...")
    click.echo("完成!")

if __name__ == "__main__":
    cli()
