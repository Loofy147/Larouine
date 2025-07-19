from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


from hisham.config_manager import ProjectConfig


class ReportGenerator:
    def __init__(self, output_path: str, config: ProjectConfig):
        self.doc = SimpleDocTemplate(output_path, pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.elements = []
        self.config = config

    def add_header(self, text: str):
        self.elements.append(Paragraph(text, self.styles["Heading1"]))
        self.elements.append(Spacer(1, 0.2 * inch))

    def add_component_section(self, component: str, results: list):
        config_dict = self.config.dict()
        self.elements.append(
            Paragraph(f"Component: {config_dict['project_meta']['name']}", self.styles["Heading2"])
        )

        for idx, result in enumerate(results, 1):
            text = f"""
            <b>Option {idx}:</b> {result['name']}<br/>
            <b>Score:</b> {result['score']}/100<br/>
            <b>Stars:</b> {result['stars']} | <b>Forks:</b> {result['forks']}<br/>
            <b>URL:</b> <link href="{result['url']}">{result['url']}</link>
            """
            self.elements.append(Paragraph(text, self.styles["Normal"]))
            self.elements.append(Spacer(1, 0.1 * inch))

    def generate_report(self):
        self.doc.build(self.elements)
