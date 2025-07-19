from datetime import datetime

class ReportGenerator:
    def generate_merge_report(self, success: bool, details: dict):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""
        Merge Report ({timestamp})
        Status: {'Success' if success else 'Failed'}
        Details:
        - Files Merged: {details.get('files', 0)}
        - Conflicts Detected: {details.get('conflicts', 0)}
        - Execution Time: {details.get('time', 0)}s
        """