# DARK8 OS - Master Programmer
"""
Code generation, analysis, and automation.
Build complete applications from natural language specifications.
"""

import json
from pathlib import Path
from typing import Dict, List

from dark8_core.config import config
from dark8_core.logger import logger


class ProjectScaffold:
    """Project structure templates"""

    TEMPLATES_DIR = Path(__file__).parent / "templates"

    DJANGO_SCAFFOLD = {
        "manage.py": "# Django management script (generated)",
        "requirements.txt": "django>=4.0\ndjango-rest-framework>=3.14\n",
        "config/settings.py": "# Django settings (generated)",
        "config/urls.py": "# Django URLs (generated)\nfrom django.contrib import admin\nfrom django.urls import path\nurlpatterns = [path('admin/', admin.site.urls)]\n",
        "app/models.py": "# Django models (generated)\nfrom django.db import models\n",
        "app/views.py": "# Django views (generated)\nfrom django.shortcuts import render\n",
        "app/serializers.py": "# DRF serializers (generated)\nfrom rest_framework import serializers\n",
    }

    FASTAPI_SCAFFOLD = {
        "requirements.txt": "fastapi>=0.104\nuvicorn>=0.24\npydantic>=2.0\n",
        "main.py": """from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from DARK8 FastAPI"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
""",
        "models.py": "from pydantic import BaseModel\nfrom typing import Optional\n",
    }

    REACT_SCAFFOLD = {
        "package.json": json.dumps(
            {
                "name": "dark8-react-app",
                "version": "0.1.0",
                "dependencies": {
                    "react": "^18.2.0",
                    "react-dom": "^18.2.0",
                    "react-scripts": "5.0.1",
                },
                "scripts": {
                    "start": "react-scripts start",
                    "build": "react-scripts build",
                    "test": "react-scripts test",
                },
            },
            indent=2,
        ),
        "public/index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DARK8 React App</title>
</head>
<body>
    <div id="root"></div>
    <script src="index.js"></script>
</body>
</html>
""",
        "src/App.jsx": """export default function App() {
    return (
        <div>
            <h1>Welcome to DARK8 React</h1>
        </div>
    );
}
""",
    }


class CodeGenerator:
    """Generate code for applications"""

    @staticmethod
    def generate_django_app(app_name: str, models: List[Dict]) -> Dict[str, str]:
        """Generate Django application structure"""
        files = {}

        # Base scaffold
        files.update(ProjectScaffold.DJANGO_SCAFFOLD)

        # Generate models
        models_code = "from django.db import models\n\n"
        for model in models:
            fields = model.get("fields", [])
            model_name = model.get("name", "Model")
            models_code += f"class {model_name}(models.Model):\n"
            for field in fields:
                field_type = field.get("type", "CharField")
                field_name = field.get("name", "field")
                models_code += f"    {field_name} = models.{field_type}()\n"
            models_code += "\n"

        files["app/models.py"] = models_code

        logger.info(f"✓ Generated Django app: {app_name}")
        return files

    @staticmethod
    def generate_fastapi_app(app_name: str, endpoints: List[Dict]) -> Dict[str, str]:
        """Generate FastAPI application"""
        files = {}
        files.update(ProjectScaffold.FASTAPI_SCAFFOLD)

        # Generate routes
        routes_code = "\nfrom fastapi import FastAPI\napp = FastAPI()\n\n"
        for endpoint in endpoints:
            method = endpoint.get("method", "GET").lower()
            path = endpoint.get("path", "/")
            description = endpoint.get("description", "")

            routes_code += f'@app.{method}("{path}")\n'
            routes_code += f'def {path.replace("/", "_")}():\n'
            routes_code += f'    """API endpoint: {description}"""\n'
            routes_code += f'    return {{"message": "Endpoint {path}"}}\n\n'

        files["main.py"] = routes_code

        logger.info(f"✓ Generated FastAPI app: {app_name}")
        return files

    @staticmethod
    def generate_react_app(app_name: str, components: List[str]) -> Dict[str, str]:
        """Generate React application"""
        files = {}
        files.update(ProjectScaffold.REACT_SCAFFOLD)

        # Generate components
        for component in components:
            component_name = component.replace(" ", "").capitalize()
            files[f"src/{component_name}.jsx"] = f"""export default function {component_name}() {{
    return <div><h2>{component_name}</h2></div>;
}}
"""

        logger.info(f"✓ Generated React app: {app_name}")
        return files


class CodeAnalyzer:
    """Analyze and review code quality"""

    @staticmethod
    async def analyze_python(code: str) -> Dict:
        """Analyze Python code"""
        try:
            from dark8_core.tools import ShellOperations

            # Write code to temp file
            temp_file = "/tmp/dark8_analyze.py"
            with open(temp_file, "w") as f:
                f.write(code)

            # Run pylint
            result = await ShellOperations.execute(f"pylint {temp_file} --disable=all --enable=E,F")

            return {
                "status": "analyzed",
                "errors": result,
            }
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return {"status": "error", "message": str(e)}


class ApplicationBuilder:
    """Build and package applications"""

    @staticmethod
    async def build_python_app(project_dir: str) -> Dict:
        """Build Python application"""
        try:
            from dark8_core.tools import ShellOperations

            logger.info(f"Building Python app: {project_dir}")

            # Install dependencies
            result = await ShellOperations.execute(
                f"cd {project_dir} && pip install -r requirements.txt"
            )

            return {
                "status": "success",
                "message": "Application built successfully",
                "build_output": result,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def build_docker(project_dir: str, app_name: str) -> str:
        """Generate Dockerfile"""
        dockerfile = """FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
"""

        dockerfile_path = Path(project_dir) / "Dockerfile"
        dockerfile_path.write_text(dockerfile)

        logger.info(f"✓ Dockerfile generated: {dockerfile_path}")
        return dockerfile


class MasterProgrammer:
    """Master Programmer Agent - generates complete applications"""

    def __init__(self):
        self.code_generator = CodeGenerator()
        self.analyzer = CodeAnalyzer()
        self.builder = ApplicationBuilder()

    async def build_application(self, spec: Dict) -> Dict:
        """
        Build complete application from specification.

        spec = {
            'name': 'my_app',
            'type': 'django|fastapi|react',
            'description': 'Application description',
            'features': [...],
            'database': 'postgresql|sqlite',
        }
        """
        app_name = spec.get("name", "dark8_app")
        app_type = spec.get("type", "fastapi")

        logger.info(f"[MASTER] Building {app_type} application: {app_name}")

        try:
            # Step 1: Generate code
            if app_type == "django":
                files = self.code_generator.generate_django_app(app_name, spec.get("models", []))
            elif app_type == "fastapi":
                files = self.code_generator.generate_fastapi_app(
                    app_name, spec.get("endpoints", [])
                )
            elif app_type == "react":
                files = self.code_generator.generate_react_app(app_name, spec.get("components", []))
            else:
                return {"status": "error", "message": f"Unknown app type: {app_type}"}

            # Step 2: Create project structure
            project_dir = config.DATA_DIR / app_name
            project_dir.mkdir(parents=True, exist_ok=True)

            for file_path, content in files.items():
                full_path = project_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content)

            # Step 3: Build
            build_result = await self.builder.build_python_app(str(project_dir))

            return {
                "status": "success",
                "app_name": app_name,
                "app_type": app_type,
                "project_dir": str(project_dir),
                "files_created": len(files),
                "build": build_result,
            }
        except Exception as e:
            logger.error(f"Build error: {e}")
            return {"status": "error", "message": str(e)}


__all__ = [
    "CodeGenerator",
    "CodeAnalyzer",
    "ApplicationBuilder",
    "MasterProgrammer",
    "ProjectScaffold",
]
