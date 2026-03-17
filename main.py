"""
CLI 入口：命令行使用
"""

import argparse
from pathlib import Path
from resume_toolkit import organize_resumes, Config
from resume_toolkit.classifier import get_all_categories


def main():
    parser = argparse.ArgumentParser(description="简历整理工具 v2.0")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # organize 命令
    organize_parser = subparsers.add_parser("organize", help="整理简历")
    organize_parser.add_argument("--source", "-s", required=True, help="源目录")
    organize_parser.add_argument("--target", "-t", required=True, help="目标目录")
    organize_parser.add_argument("--execute", action="store_true", help="实际执行（默认为预览模式）")
    organize_parser.add_argument("--config", "-c", help="配置文件路径")

    # categories 命令
    categories_parser = subparsers.add_parser("categories", help="查看分类规则")

    # web 命令
    web_parser = subparsers.add_parser("web", help="启动 Web UI")
    web_parser.add_argument("--port", "-p", type=int, default=5000, help="端口号（默认 5000）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "organize":
        # 加载配置
        config = Config(args.config) if args.config else Config()

        # 执行整理
        result = organize_resumes(
            source_dir=args.source,
            target_dir=args.target,
            dry_run=not args.execute,
            config=config,
        )

        # 输出结果
        print(result.summary())

        if result.errors:
            print("\n⚠️ 错误:")
            for error in result.errors:
                print(f"  - {error}")

    elif args.command == "categories":
        # 显示所有分类
        config = Config()
        categories = get_all_categories(config)
        print("=== 分类规则 ===")
        for category, keywords in categories.items():
            print(f"{category}: {', '.join(keywords)}")

    elif args.command == "web":
        # 启动 Web UI
        import sys
        from web.app import app
        print(f"🌐 Web UI 启动中: http://localhost:{args.port}")
        app.run(debug=False, port=args.port)


if __name__ == "__main__":
    main()
