import os
import platform
import psutil
import datetime
import time
import glob

class ComputerEngine:
    def __init__(self, root_dir="."):
        self.root_dir = root_dir

    def get_operations(self):
        """Pillar 1: Commanding Operations."""
        return {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "uptime": str(datetime.timedelta(seconds=int(time.time() - psutil.boot_time()))) if hasattr(psutil, 'boot_time') else "Unknown",
            "cpu_usage": psutil.cpu_percent(),
            "ram_usage": psutil.virtual_memory().percent
        }

    def get_progress(self):
        """Pillar 2: Making Progress (Parses TODO.md or PROGRESS.md)."""
        todo_path = os.path.join(self.root_dir, "TODO.md")
        if not os.path.exists(todo_path):
            return {"status": "No TODO.md found", "percent": 0, "tasks": []}

        completed = 0
        total = 0
        tasks = []
        with open(todo_path, 'r') as f:
            for line in f:
                if "[ ]" in line:
                    total += 1
                    tasks.append({"task": line.replace("[ ]", "").strip(), "done": False})
                elif "[x]" in line.lower():
                    total += 1
                    completed += 1
                    tasks.append({"task": line.replace("[x]", "").replace("[X]", "").strip(), "done": True})
        
        percent = (completed / total * 100) if total > 0 else 0
        return {"status": f"{completed}/{total} Tasks Done", "percent": round(percent, 1), "tasks": tasks}

    def get_tech_endeavors(self):
        """Pillar 3: Understanding Technological Endeavors (Analysis)."""
        stats = {}
        total_size = 0
        file_count = 0
        
        for root, dirs, files in os.walk(self.root_dir):
            if ".git" in root or "__pycache__" in root or "node_modules" in root:
                continue
            for file in files:
                ext = os.path.splitext(file)[1] or "no-ext"
                stats[ext] = stats.get(ext, 0) + 1
                try:
                    total_size += os.path.getsize(os.path.join(root, file))
                except OSError:
                    pass
                file_count += 1

        return {
            "file_count": file_count,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "extensions": stats
        }

    def generate_report(self):
        """Pillar 4: Reporting."""
        ops = self.get_operations()
        prog = self.get_progress()
        tech = self.get_tech_endeavors()
        
        report = f"# COMPUTER STATUS REPORT - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        report += f"## 🖥️ System Operations\n- OS: {ops['system']} {ops['release']}\n- CPU: {ops['cpu_usage']}%\n- RAM: {ops['ram_usage']}%\n\n"
        report += f"## 📈 Project Progress\n- Completion: {prog['percent']}%\n- Summary: {prog['status']}\n\n"
        report += f"## 🛠️ Technological Endeavors\n- Total Files: {tech['file_count']}\n- Project Size: {tech['total_size_mb']} MB\n"
        
        return report
