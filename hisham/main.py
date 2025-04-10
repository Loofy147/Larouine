import sys
from pathlib import Path
from hisham.config_manager import load_config
from hisham.github_integration import GitHubAPI
from hisham.report_generator import ReportGenerator
from hisham.utils import push_to_github, setup_repository

def main(config_path: str):
    # تحميل إعدادات المشروع من ملف التكوين
    config = load_config(config_path)

    # إعداد واجهة GitHub مع التوكن
    gh_api = GitHubAPI(config.github_settings.api_token)

    # إعداد مولد التقارير مع تحديد اسم ملف الخرج
    report = ReportGenerator("project_analysis.pdf")

    # عملية تحليل لكل مكون من المكونات المستهدفة
    for component in config.target_components:
        results = gh_api.search_repositories(component)
        # إضافة قسم التقرير لكل مكون بناءً على أفضل 3 نتائج
        report.add_component_section(component.name, results[:3])

    # إضافة عنوان رئيسي للتقرير وإنشاء التقرير النهائي
    report.add_header("Project Analysis Report")
    report.generate_report()

    # التفاعل مع GitHub: إعداد المستودع ودفع التقرير
    try:
        # يتم استنساخ المستودع من GitHub باستخدام الإعدادات الموجودة في التكوين
        setup_repository(config.github_settings.dict())
        # دفع التغييرات مع رسالة توضيحية
        push_to_github(config.github_settings.repo_name, "Add project analysis report")
    except Exception as e:
        print(f"GitHub integration error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_path>")
        sys.exit(1)

    main(sys.argv[1])
