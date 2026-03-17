"""
Web UI：浏览器操作界面
"""

from flask import Flask, render_template, request, jsonify
from pathlib import Path
import os
from resume_toolkit import organize_resumes, OrganizeResult, Config

app = Flask(__name__)

# 存储最后一次的操作结果
last_result: OrganizeResult = None


@app.route("/")
def index():
    """首页"""
    return render_template("index.html")


@app.route("/api/organize", methods=["POST"])
def organize():
    """执行整理操作"""
    global last_result

    data = request.json
    source_dir = data.get("source_dir")
    target_dir = data.get("target_dir")
    dry_run = data.get("dry_run", True)

    if not source_dir or not target_dir:
        return jsonify({"success": False, "error": "缺少源目录或目标目录"}), 400

    # 执行整理
    try:
        result = organize_resumes(
            source_dir=source_dir,
            target_dir=target_dir,
            dry_run=dry_run,
        )
        last_result = result

        return jsonify({
            "success": True,
            "summary": result.summary(),
            "details": {
                "scan_total": result.scan_result.total_files if result.scan_result else 0,
                "dedup_duplicates": result.dedup_result.duplicates_to_delete if result.dedup_result else 0,
                "moved": result.moved_count,
                "renamed": result.renamed_count,
                "manual_review": result.manual_review_count,
                "errors": result.errors,
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/config/categories", methods=["GET", "POST"])
def categories():
    """获取或更新分类规则"""
    config = Config()

    if request.method == "GET":
        from resume_toolkit.classifier import get_all_categories
        categories = get_all_categories(config)
        return jsonify({"success": True, "categories": categories})
    else:
        data = request.json
        category = data.get("category")
        keywords = data.get("keywords", [])

        if not category or not keywords:
            return jsonify({"success": False, "error": "缺少分类名或关键词"}), 400

        config.add_custom_category(category, keywords)
        return jsonify({"success": True, "message": f"已添加分类: {category}"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
