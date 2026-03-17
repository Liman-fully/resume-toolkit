#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简历去重 + 归类 CLI 工具

用法示例：
  # 预览全库去重（默认 dry-run，安全）
  python main.py dedup

  # 真正执行去重
  python main.py dedup --execute

  # 审计特殊文件夹（如 _备份_重复简历）
  python main.py audit --folder _备份_重复简历
  python main.py audit --folder _备份_重复简历 --execute

  # 对某文件夹内的简历进行自动归类（预览）
  python main.py classify --folder _待分类
  python main.py classify --folder _待分类 --execute

  # 指定不同的简历库路径（跨机器）
  python main.py dedup --base /path/to/简历库

  # 查看帮助
  python main.py --help
  python main.py dedup --help
"""

import argparse
import os
import sys
from datetime import datetime

# 确保 resume_dedup 包可被找到
sys.path.insert(0, os.path.dirname(__file__))

from resume_dedup.config import BASE_DIR
from resume_dedup.dedup import audit_special_folder, run_dedup
from resume_dedup.classify import classify_folder


# ── 日志写入 ──────────────────────────────────────────────────

def write_log(base_dir: str, name: str, content: str) -> str:
    log_dir = os.path.join(base_dir, "_处理日志")
    os.makedirs(log_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(log_dir, f"{name}_{ts}.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(content)
    return log_path


# ── 子命令：dedup ─────────────────────────────────────────────

def cmd_dedup(args: argparse.Namespace) -> None:
    dry_run = not args.execute
    base_dir = args.base

    print(f"\n{'[DRY-RUN 预览模式]' if dry_run else '[执行模式]'} 全库去重")
    print(f"简历库路径：{base_dir}\n")

    result = run_dedup(base_dir=base_dir, dry_run=dry_run)
    print(result.summary())

    if result.deleted_count > 0:
        print(f"\n{'将删除' if dry_run else '已删除'}的文件：")
        for entry in result.deleted:
            keep = result.kept[result.deleted.index(entry) // 1] if result.kept else "?"
            print(f"  ✗ {entry}")
        print(f"\n  保留的文件（每组最优）：")
        for entry in result.kept:
            print(f"  ✓ {entry}")

    if result.errors:
        print(f"\n⚠ 出错文件（{len(result.errors)} 个）：")
        for e in result.errors:
            print(f"  {e}")

    if not dry_run:
        log_lines = [result.summary(), "\n\n删除列表："]
        for d, k in zip(result.deleted, result.kept):
            log_lines.append(f"  删除: {d}  (保留: {k})")
        if result.errors:
            log_lines.append("\n错误：")
            log_lines.extend(result.errors)
        log_path = write_log(base_dir, "dedup", "\n".join(log_lines))
        print(f"\n📄 日志已保存：{log_path}")

    if dry_run and result.deleted_count > 0:
        print(f"\n💡 加 --execute 参数即可真正执行删除。")


# ── 子命令：audit ─────────────────────────────────────────────

def cmd_audit(args: argparse.Namespace) -> None:
    dry_run = not args.execute
    base_dir = args.base
    folder = args.folder

    print(f"\n{'[DRY-RUN 预览模式]' if dry_run else '[执行模式]'} 审计文件夹：{folder}")
    print(f"简历库路径：{base_dir}\n")

    result = audit_special_folder(folder, base_dir=base_dir, dry_run=dry_run)
    print(result.summary())

    if result.unique_filenames:
        print(f"\n  独有文件样例（前10个）：")
        for f in result.unique_filenames[:10]:
            print(f"    {f}")

    if result.errors:
        print(f"\n⚠ 错误：")
        for e in result.errors:
            print(f"  {e}")

    if not dry_run:
        log_path = write_log(base_dir, f"audit_{folder.lstrip('_')}", result.summary())
        print(f"\n📄 日志已保存：{log_path}")

    if dry_run and result.verdict != "not_found":
        print(f"\n💡 加 --execute 参数即可真正执行。")


# ── 子命令：classify ──────────────────────────────────────────

def cmd_classify(args: argparse.Namespace) -> None:
    dry_run = not args.execute
    base_dir = args.base
    folder = args.folder

    print(f"\n{'[DRY-RUN 预览模式]' if dry_run else '[执行模式]'} 自动归类：{folder}")
    print(f"简历库路径：{base_dir}\n")

    result = classify_folder(folder, base_dir=base_dir, dry_run=dry_run)
    print(result.summary())

    if result.moved:
        print(f"\n{'将移动' if dry_run else '已移动'}的文件（前20条）：")
        for src_folder, fname, cat in result.moved[:20]:
            print(f"  {src_folder}/{fname}  →  {cat}/")
        if len(result.moved) > 20:
            print(f"  ... 共 {len(result.moved)} 条")

    if result.skipped:
        print(f"\n跳过的文件：")
        for src_folder, fname, reason in result.skipped:
            print(f"  {fname}: {reason}")

    if result.errors:
        print(f"\n⚠ 错误：")
        for e in result.errors:
            print(f"  {e}")

    if not dry_run:
        lines = [result.summary(), "\n\n移动列表："]
        for sf, fn, cat in result.moved:
            lines.append(f"  {sf}/{fn} -> {cat}/")
        log_path = write_log(base_dir, f"classify_{folder.lstrip('_')}", "\n".join(lines))
        print(f"\n📄 日志已保存：{log_path}")

    if dry_run and result.moved_count > 0:
        print(f"\n💡 加 --execute 参数即可真正执行。")


# ── 参数解析 ──────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="resume-dedup",
        description="简历库去重 & 自动归类工具（默认 dry-run，安全预览）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--base",
        default=BASE_DIR,
        help=f"简历库根目录（默认：{BASE_DIR}，也可设置环境变量 RESUME_BASE_DIR）",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # dedup
    p_dedup = sub.add_parser("dedup", help="扫描全库，删除重复简历")
    p_dedup.add_argument("--execute", action="store_true", help="真正执行删除（不加此参数为 dry-run）")
    p_dedup.set_defaults(func=cmd_dedup)

    # audit
    p_audit = sub.add_parser("audit", help="审计特殊文件夹（如 _备份_重复简历）")
    p_audit.add_argument("--folder", required=True, help="要审计的文件夹名（相对根目录）")
    p_audit.add_argument("--execute", action="store_true", help="真正执行（删除或移动）")
    p_audit.set_defaults(func=cmd_audit)

    # classify
    p_cls = sub.add_parser("classify", help="对指定文件夹内的简历进行自动归类")
    p_cls.add_argument("--folder", required=True, help="源文件夹名（如 _待分类）")
    p_cls.add_argument("--execute", action="store_true", help="真正执行移动")
    p_cls.set_defaults(func=cmd_classify)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # 验证 base 目录
    if not os.path.isdir(args.base):
        print(f"❌ 错误：简历库路径不存在：{args.base}")
        print(f"   请通过 --base 参数或 RESUME_BASE_DIR 环境变量指定正确路径。")
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
