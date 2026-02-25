# DARK8 OS - Tool Implementations
"""
Core tools for agent execution.
File ops, shell, git, web client, etc.
"""

import asyncio
import os
from typing import Dict, Optional

from dark8_core.logger import logger


class FileOperations:
    """File system operations"""

    @staticmethod
    async def read_file(path: str, max_lines: Optional[int] = None) -> str:
        """Read file content"""
        try:
            with open(path, "r") as f:
                content = f.read()
                if max_lines:
                    return "\n".join(content.split("\n")[:max_lines])
                return content
        except Exception as e:
            return f"Error reading {path}: {e}"

    @staticmethod
    async def write_file(path: str, content: str, append: bool = False) -> str:
        """Write to file"""
        try:
            mode = "a" if append else "w"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, mode) as f:
                f.write(content)
            return f"✓ File written: {path}"
        except Exception as e:
            return f"Error writing {path}: {e}"

    @staticmethod
    async def list_dir(path: str = ".") -> str:
        """List directory contents"""
        try:
            items = os.listdir(path)
            return "\n".join(sorted(items))
        except Exception as e:
            return f"Error listing {path}: {e}"

    @staticmethod
    async def delete_file(path: str) -> str:
        """Delete file"""
        try:
            if os.path.isfile(path):
                os.remove(path)
                return f"✓ Deleted: {path}"
            else:
                return f"File not found: {path}"
        except Exception as e:
            return f"Error deleting {path}: {e}"

    @staticmethod
    async def copy_file(src: str, dst: str) -> str:
        """Copy file"""
        try:
            import shutil

            shutil.copy2(src, dst)
            return f"✓ Copied {src} → {dst}"
        except Exception as e:
            return f"Error copying: {e}"


class ShellOperations:
    """Safe shell command execution"""

    @staticmethod
    async def execute(command: str, timeout: int = 30) -> str:
        """
        Execute shell command safely in subprocess.
        Returns: stdout + stderr
        """
        try:
            logger.info(f"[SHELL] {command}")

            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
            except asyncio.TimeoutError:
                process.kill()
                return f"Command timeout (>{timeout}s)"

            output = stdout.decode() + stderr.decode()
            return output.strip()
        except Exception as e:
            return f"Error executing command: {e}"

    @staticmethod
    async def which(command: str) -> str:
        """Find command in PATH"""
        result = await ShellOperations.execute(f"which {command}")
        return result if result and "not found" not in result else None


class GitOperations:
    """Git version control operations"""

    @staticmethod
    async def clone(repo_url: str, target_dir: str) -> str:
        """Clone git repository"""
        try:
            cmd = f"git clone {repo_url} {target_dir}"
            return await ShellOperations.execute(cmd, timeout=60)
        except Exception as e:
            return f"Error cloning: {e}"

    @staticmethod
    async def commit(path: str, message: str) -> str:
        """Commit changes"""
        try:
            cmd = f"cd {path} && git add . && git commit -m '{message}'"
            return await ShellOperations.execute(cmd)
        except Exception as e:
            return f"Error committing: {e}"

    @staticmethod
    async def push(path: str) -> str:
        """Push to remote"""
        try:
            cmd = f"cd {path} && git push"
            return await ShellOperations.execute(cmd)
        except Exception as e:
            return f"Error pushing: {e}"


class WebClient:
    """HTTP/Web client operations"""

    @staticmethod
    async def fetch(url: str) -> str:
        """Fetch URL content"""
        try:
            import httpx

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                return response.text[:1000]  # First 1000 chars
        except Exception as e:
            return f"Error fetching {url}: {e}"

    @staticmethod
    async def post(url: str, data: Dict) -> str:
        """POST to URL"""
        try:
            import httpx

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(url, json=data)
                return response.text[:1000]
        except Exception as e:
            return f"Error posting to {url}: {e}"


class SystemOperations:
    """System information and operations"""

    @staticmethod
    async def get_system_info() -> Dict:
        """Get system information"""
        try:
            import psutil

            return {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage("/").percent,
                "platform": os.name,
            }
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {}


class ToolRegistry:
    """Registry of all available tools"""

    def __init__(self):
        self.tools = {
            "file_read": FileOperations.read_file,
            "file_write": FileOperations.write_file,
            "file_list": FileOperations.list_dir,
            "file_delete": FileOperations.delete_file,
            "file_copy": FileOperations.copy_file,
            "shell_execute": ShellOperations.execute,
            "shell_which": ShellOperations.which,
            "git_clone": GitOperations.clone,
            "git_commit": GitOperations.commit,
            "git_push": GitOperations.push,
            "web_fetch": WebClient.fetch,
            "web_post": WebClient.post,
            "sys_info": SystemOperations.get_system_info,
        }

    async def execute(self, tool_name: str, **kwargs) -> str:
        """Execute tool by name"""
        if tool_name not in self.tools:
            return f"Tool not found: {tool_name}"

        try:
            result = await self.tools[tool_name](**kwargs)
            return str(result)
        except Exception as e:
            logger.error(f"Tool error: {e}")
            return f"Tool error: {e}"


__all__ = [
    "FileOperations",
    "ShellOperations",
    "GitOperations",
    "WebClient",
    "SystemOperations",
    "ToolRegistry",
]
