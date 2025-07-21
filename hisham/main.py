import sys
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from hisham.config_manager import load_config
from hisham.github_integration import GitHubAPI
from hisham.report_generator import ReportGenerator
from hisham.utils import push_to_github, setup_repository

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Detect available features (e.g., additional libraries)
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

def analyze_component(gh_api, component):
    """
    Analyzes a specific component using the GitHub API.
    """
    if not hasattr(component, 'name'):
        logging.error("Component is missing 'name' attribute.")
        return None, []

    logging.info(f"Analyzing component: {component.name}")
    try:
        results = gh_api.search_repositories(component)
        return component.name, results[:3]
    except Exception as e:
        logging.error(f"Error analyzing component {component.name}: {e}")
        return component.name, []

def generate_report(config, results):
    """
    Generates a report based on the analysis results.
    """
    report_filename = config.report_file if hasattr(config, "report_file") else "project_analysis.pdf"
    report = ReportGenerator(report_filename)
    report.add_header("Project Analysis Report")
    for component_name, top_results in results:
        if component_name:
            report.add_component_section(component_name, top_results)
    report.generate_report()
    logging.info(f"Report generated: {report_filename}")
    return report_filename

def main(config_path: str):
    # Load project settings
    try:
        config = load_config(config_path)
        logging.info("Configuration loaded successfully.")
    except FileNotFoundError:
        logging.error(f"Configuration file not found at: {config_path}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        sys.exit(1)

    # Setup GitHub interface
    if not hasattr(config, "github_settings") or not hasattr(config.github_settings, "api_token"):
        logging.error("GitHub API token not found in configuration.")
        sys.exit(1)

    try:
        gh_api = GitHubAPI(config.github_settings.api_token)
        logging.info("GitHub API initialized.")
    except Exception as e:
        logging.error(f"Error initializing GitHub API: {e}")
        sys.exit(1)

    # Analyze components using parallel processing
    target_components = config.target_components if hasattr(config, "target_components") else []
    if not target_components:
        logging.warning("No target components found in configuration.")

    try:
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda c: analyze_component(gh_api, c), target_components))
    except Exception as e:
        logging.error(f"Error during components analysis: {e}")
        sys.exit(1)

    # Generate the report
    try:
        report_filename = generate_report(config, results)
    except Exception as e:
        logging.error(f"Error generating report: {e}")
        sys.exit(1)

    # Push the report to GitHub
    if hasattr(config, "github_settings") and hasattr(config.github_settings, "repo_name"):
        try:
            setup_repository(config.github_settings.dict())
            push_to_github(config.github_settings.repo_name, f"Add {report_filename}")
            logging.info("Changes pushed to GitHub.")
        except Exception as e:
            logging.error(f"Error during GitHub integration: {e}")
            sys.exit(1)
    else:
        logging.warning("repo_name not found in github_settings. Skipping push to GitHub.")


if __name__ == "__main__":
    # Check command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_path>")
        sys.exit(1)

    main(sys.argv[1])