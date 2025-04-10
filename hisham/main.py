import sys
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from hisham.config_manager import load_config
from hisham.github_integration import GitHubAPI
from hisham.report_generator import ReportGenerator
from hisham.utils import push_to_github, setup_repository

# إعداد السجل (Logging)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# كشف الميزات المتوفرة (مثال: مكتبات إضافية)
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

def analyze_component(gh_api, component):
    """
    تحليل مكون محدد باستخدام GitHub API.
    """
    logging.info(f"Analyzing component: {component.name}")
    try:
        results = gh_api.search_repositories(component)
        return component.name, results[:3]
    except Exception as e:
        logging.error(f"Error analyzing component {component.name}: {e}")
        return component.name, []

def generate_report(config, results):
    """
    إنشاء تقرير بناءً على نتائج التحليل.
    """
    report_filename = config.get("report_file", "project_analysis.pdf")
    report = ReportGenerator(report_filename)
    report.add_header("Project Analysis Report")
    for component_name, top_results in results:
        report.add_component_section(component_name, top_results)
    report.generate_report()
    logging.info(f"Report generated: {report_filename}")
    return report_filename

def main(config_path: str):
    # تحميل إعدادات المشروع
    try:
        config = load_config(config_path)
        logging.info("Configuration loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        sys.exit(1)

    # إعداد واجهة GitHub
    try:
        gh_api = GitHubAPI(config.github_settings.api_token)
        logging.info("GitHub API initialized.")
    except Exception as e:
        logging.error(f"Error initializing GitHub API: {e}")
        sys.exit(1)

    # تحليل المكونات باستخدام المعالجة المتوازية
    try:
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda c: analyze_component(gh_api, c), config.target_components))
    except Exception as e:
        logging.error(f"Error during components analysis: {e}")
        sys.exit(1)

    # إنشاء التقرير
    try:
        report_filename = generate_report(config, results)
    except Exception as e:
        logging.error(f"Error generating report: {e}")
        sys.exit(1)

    # دفع التقرير إلى GitHub
    try:
        setup_repository(config.github_settings.dict())
        push_to_github(config.github_settings.repo_name, f"Add {report_filename}")
        logging.info("Changes pushed to GitHub.")
    except Exception as e:
        logging.error(f"Error during GitHub integration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # التحقق من مدخلات سطر الأوامر
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_path>")
        sys.exit(1)

    main(sys.argv[1])