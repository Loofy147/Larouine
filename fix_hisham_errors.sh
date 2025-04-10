#!/bin/bash

# ملف الإصلاحات
FIX_PATCH=$(cat <<'EOL'
diff --git a/hisham/report_generator.py b/hisham/report_generator.py
--- a/hisham/report_generator.py
+++ b/hisham/report_generator.py
@@ -15,7 +15,8 @@
         self.elements.append(Spacer(1, 0.2*inch))
     
     def add_component_section(self, component: str, results: List[Dict]):
+        config_dict = self.config.dict()
         self.elements.append(
-            Paragraph(f"Component: {self.config.get('project_meta').get('name')}", self.styles["Heading2"])
+            Paragraph(f"Component: {config_dict['project_meta']['name']}", self.styles["Heading2"])
         )
         
         for idx, result in enumerate(results, 1):
diff --git a/main.py b/main.py
--- a/main.py
+++ b/main.py
@@ -23,7 +23,7 @@
     # GitHub integration
     try:
-        setup_repository(config.get('github_settings'))
-        push_to_github(config.get('github_settings').get('repo_name'), "Add analysis report")
+        setup_repository(config.github_settings.dict())
+        push_to_github(config.github_settings.repo_name, "Add analysis report")
     except Exception as e:
         print(f"GitHub error: {e}")
         sys.exit(1)
EOL
)

# تطبيق التعديلات
echo "$FIX_PATCH" | git apply -

echo "تم الإصلاح بنجاح!"
