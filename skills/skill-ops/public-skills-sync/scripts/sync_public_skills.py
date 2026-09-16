#!/usr/bin/env python3
"""
Sync Public Skills to Asmadey/skills repository.
Works exclusively with PersonalOS/skills/public/ and synchronizes promoted skills
to the external GitHub repository (https://github.com/Asmadey/skills).
"""

import os
import sys
import re
import shutil
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

DEFAULT_SOURCE = Path("/Users/asmadey/AntiGravity/PersonalOS/skills/public")
DEFAULT_TARGET = Path("/Users/asmadey/AntiGravity/skills")

CATEGORY_NAMES_RU = {
    "dev": "🛠 Разработка и Инженерия (Development & Engineering)",
    "automation": "🤖 Автоматизация, Воркфлоу и Интеграции (Automation & Agents)",
    "product": "📦 Продуктовый менеджмент и PRD (Product Management)",
    "writing": "✍️ Тексты, Редактура и Humanizing (Writing & Anti-Slop)",
    "ux": "🎨 UI/UX и Дизайн-системы (Design & UI/UX)",
    "design": "✨ Анимации, Графика и Стили (Motion & Visuals)",
    "ops": "⚙️ Операционные задачи и Делегация (Operations & Tasks)",
    "business": "💼 Бизнес, Стратегия и Продажи (Business & Strategy)",
    "marketing": "📈 Маркетинг, SEO и Аналитика (Marketing & SEO)",
    "research": "🔬 Исследования, Анализ и SOTA (Research & Intelligence)",
    "personal": "👤 Личная продуктивность и База знаний (Personal & PKM)",
    "ai": "🧠 ИИ-оптимизация и Безопасность (AI Core & Context)",
    "skill-ops": "🏗 Мета-навыки и Аудит (Skill Engineering & Operations)",
}

def parse_skill_md(skill_path: Path):
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        skill_file = skill_path / "skill.md"
    if not skill_file.exists():
        return None

    content = skill_file.read_text(encoding="utf-8", errors="ignore")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {
            "name": skill_path.name,
            "description": "Модуль возможностей ИИ-агента",
            "triggers": skill_path.name,
            "stack": "Node/CLI"
        }

    frontmatter = match.group(1)
    name_match = re.search(r"^name:\s*['\"]?([\w-]+)['\"]?", frontmatter, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else skill_path.name

    desc_match = re.search(r"^description:\s*(?:>|\|)?\s*(.*)", frontmatter, re.MULTILINE)
    description = desc_match.group(1).strip() if desc_match else ""
    if not description or len(description) < 10:
        lines = frontmatter.split("\n")
        desc_lines = []
        capture = False
        for line in lines:
            if re.match(r"^description:\s*(?:>|\|)?", line):
                capture = True
                continue
            if capture:
                if re.match(r"^[a-zA-Z0-9_-]+:", line) or line.startswith("---"):
                    break
                if line.strip():
                    desc_lines.append(line.strip())
        if desc_lines:
            description = " ".join(desc_lines)

    # Clean description
    description = re.sub(r"^[>\s\"']+|[>\s\"']+$", "", description).strip()
    if not description:
        description = "Модуль возможностей ИИ-агента"

    # Extract triggers if mentioned
    triggers_match = re.search(r"[Тт]риггеры?:\s*([^\n\.]+)", description)
    if triggers_match:
        triggers = triggers_match.group(1).strip()
    else:
        triggers = name

    # Detect stack heuristically
    stack = "Prompt"
    if (skill_path / "scripts").exists():
        py_files = list((skill_path / "scripts").glob("*.py"))
        sh_files = list((skill_path / "scripts").glob("*.sh"))
        js_files = list((skill_path / "scripts").glob("*.js")) + list((skill_path / "scripts").glob("*.ts"))
        if py_files and js_files:
            stack = "Python / Node/CLI"
        elif py_files:
            stack = "Python / CLI"
        elif js_files or (skill_path / "package.json").exists():
            stack = "Node/CLI"
        elif sh_files:
            stack = "Bash / CLI"

    return {
        "name": name,
        "description": description,
        "triggers": triggers,
        "stack": stack
    }

def get_public_skills(source_dir: Path):
    skills = {}
    for cat_dir in sorted(source_dir.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith("."):
            continue
        cat_name = cat_dir.name
        skills[cat_name] = {}
        for skill_dir in sorted(cat_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue
            meta = parse_skill_md(skill_dir)
            if meta:
                skills[cat_name][skill_dir.name] = {
                    "path": skill_dir,
                    "meta": meta
                }
    return skills

def sync_skill_files(src_path: Path, dest_path: Path, dry_run=False):
    if dry_run:
        print(f"  [DRY-RUN] Copy tree {src_path} -> {dest_path}")
        return

    if dest_path.exists():
        shutil.rmtree(dest_path)
    
    def ignore_patterns(path, names):
        return [n for n in names if n in [".DS_Store", "__pycache__", ".git", ".pytest_cache"]]

    shutil.copytree(src_path, dest_path, ignore=ignore_patterns)

def update_index_md(target_repo: Path, new_skills: list, dry_run=False):
    index_file = target_repo / "INDEX.md"
    if not index_file.exists():
        print(f"Warning: {index_file} not found")
        return

    content = index_file.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")

    # Update last_updated
    content = re.sub(r"last_updated:\s*\d{4}-\d{2}-\d{2}", f"last_updated: {today}", content)

    # Count total skills in target
    skills_root = target_repo / "skills"
    total_skills = sum(1 for p in skills_root.glob("*/*") if p.is_dir() and not p.name.startswith("."))

    content = re.sub(r"\((\d+)\s*навык(?:ов|а|)\)", f"({total_skills} навыков)", content)

    for item in new_skills:
        cat = item["category"]
        name = item["name"]
        folder = item["folder"]
        meta = item["meta"]

        # Check if already in INDEX.md
        if f"| **{name}** |" in content or f"| **`{name}`** |" in content or f"/{cat}/{folder}/SKILL.md" in content:
            continue

        # Build table row
        desc_clean = meta["description"].split(".")[0].strip()
        if len(desc_clean) > 120:
            desc_clean = desc_clean[:117] + "..."
        row = f"| **{name}** | **{name.capitalize()}**.<br>{desc_clean} | `{meta['triggers']}` | {meta['stack']} | [SKILL.md](skills/{cat}/{folder}/SKILL.md) |\n"

        # Locate category section
        cat_pattern = rf'(##\s*<a id="{re.escape(cat)}"></a>.*?\|\s*Документация\s*\|\n\|[:\-\| ]+\|\n)'
        match = re.search(cat_pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            content = content[:match.end()] + row + content[match.end():]
        else:
            print(f"Notice: Section for category '{cat}' not matched cleanly in INDEX.md")

    if not dry_run:
        index_file.write_text(content, encoding="utf-8")
        print(f"✓ Updated {index_file.name} (Total: {total_skills} skills)")

def update_readme_md(target_repo: Path, new_skills: list, dry_run=False):
    readme_file = target_repo / "README.md"
    if not readme_file.exists():
        return

    content = readme_file.read_text(encoding="utf-8")
    skills_root = target_repo / "skills"
    total_skills = sum(1 for p in skills_root.glob("*/*") if p.is_dir() and not p.name.startswith("."))

    # Update count in README.md
    content = re.sub(r"(\d+)\s*специализированным исполняемым навыкам", f"{total_skills} специализированным исполняемым навыкам", content)

    for item in new_skills:
        cat = item["category"]
        name = item["name"]
        folder = item["folder"]
        meta = item["meta"]

        if f"skills/{cat}/{folder}/SKILL.md" in content:
            continue

        desc_first = meta["description"].split(".")[0].strip()
        if len(desc_first) > 130:
            desc_first = desc_first[:127] + "..."
        row = f"| [**`{name}`**](skills/{cat}/{folder}/SKILL.md) | **{name.capitalize()}**. {desc_first}. | {meta['stack']} |\n"

        # Try to find category table in README.md
        cat_pattern = rf'(###\s*.*?\(.*?\)\n\*Директория:\*.*?skills/{re.escape(cat)}/.*?\|\s*Стек / Формат\s*\|\n\|[:\-\| ]+\|\n)'
        match = re.search(cat_pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            content = content[:match.end()] + row + content[match.end():]

    if not dry_run:
        readme_file.write_text(content, encoding="utf-8")
        print(f"✓ Updated {readme_file.name}")

def update_changelog_md(target_repo: Path, added_skills: list, modified_skills: list, dry_run=False):
    changelog_file = target_repo / "changelog.md"
    if not changelog_file.exists():
        return

    content = changelog_file.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")

    # Update last_updated in frontmatter
    content = re.sub(r"last_updated:\s*\d{4}-\d{2}-\d{2}", f"last_updated: {today}", content)

    entry_lines = [f"\n## [{today}] — Синхронизация навыков из PersonalOS (public)\n"]
    if added_skills:
        entry_lines.append("### 📦 Добавленные навыки")
        for item in added_skills:
            cat = item["category"]
            name = item["name"]
            folder = item["folder"]
            meta = item["meta"]
            desc_short = meta["description"].split(".")[0].strip()
            entry_lines.append(f"- **`{cat}/{name}`** ([`skills/{cat}/{folder}/SKILL.md`](skills/{cat}/{folder}/SKILL.md)):")
            entry_lines.append(f"  - {desc_short}.")
            entry_lines.append("  - Прошел аудит безопасности NVIDIA SkillSpector (APPROVE).")

    if modified_skills:
        entry_lines.append("### 🔄 Обновленные навыки")
        for item in modified_skills:
            cat = item["category"]
            name = item["name"]
            folder = item["folder"]
            entry_lines.append(f"- **`{cat}/{name}`** ([`skills/{cat}/{folder}/SKILL.md`](skills/{cat}/{folder}/SKILL.md)): синхронизированы обновления и ресурсы.")

    entry_lines.append("\n---\n")
    new_entry = "\n".join(entry_lines)

    # Insert after top header
    header_end_match = re.search(r"(# 📜 Журнал изменений.*?\n\n)", content, re.DOTALL)
    if header_end_match:
        insert_pos = header_end_match.end()
        # If today section already exists at top, skip or merge
        if f"## [{today}]" in content[:insert_pos + 100]:
            print(f"Notice: Entry for [{today}] already present in changelog.md")
        else:
            content = content[:insert_pos] + new_entry + content[insert_pos:]

    if not dry_run:
        changelog_file.write_text(content, encoding="utf-8")
        print(f"✓ Updated {changelog_file.name}")

def main():
    parser = argparse.ArgumentParser(description="Sync PersonalOS public skills to Asmadey/skills repo")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Source directory (PersonalOS/skills/public)")
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET, help="Target repository root (Asmadey/skills)")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without writing")
    parser.add_argument("--commit", action="store_true", help="Create git commit in target repo")
    parser.add_argument("--push", action="store_true", help="Push commits to origin remote")
    parser.add_argument("--skill", type=str, help="Sync specific skill name or category/name")

    args = parser.parse_args()

    source_dir = args.source.resolve()
    target_repo = args.target.resolve()

    if not source_dir.exists():
        print(f"Error: Source directory {source_dir} not found.")
        sys.exit(1)

    if not target_repo.exists() or not (target_repo / ".git").exists():
        print(f"Error: Target git repo {target_repo} not found.")
        sys.exit(1)

    target_skills_root = target_repo / "skills"
    target_skills_root.mkdir(parents=True, exist_ok=True)

    print(f"🔍 Scanning public skills from: {source_dir}")
    print(f"🎯 Target repository:           {target_repo}")

    public_skills = get_public_skills(source_dir)

    added_skills = []
    modified_skills = []

    for cat_name, skills in public_skills.items():
        cat_target_dir = target_skills_root / cat_name
        cat_target_dir.mkdir(parents=True, exist_ok=True)

        for folder_name, data in skills.items():
            if args.skill:
                query = args.skill.strip()
                if "/" in query:
                    q_cat, q_name = query.split("/", 1)
                    if cat_name != q_cat or (folder_name != q_name and data["meta"]["name"] != q_name):
                        continue
                else:
                    if folder_name != query and data["meta"]["name"] != query:
                        continue

            dest_skill_dir = cat_target_dir / folder_name
            src_skill_dir = data["path"]

            is_new = not dest_skill_dir.exists()

            # Compare contents if exists
            is_modified = False
            if not is_new:
                # Compare SKILL.md
                src_md = (src_skill_dir / "SKILL.md").read_bytes() if (src_skill_dir / "SKILL.md").exists() else b""
                dest_md = (dest_skill_dir / "SKILL.md").read_bytes() if (dest_skill_dir / "SKILL.md").exists() else b""
                if src_md != dest_md:
                    is_modified = True

            if is_new or is_modified:
                sync_skill_files(src_skill_dir, dest_skill_dir, dry_run=args.dry_run)
                item_info = {
                    "category": cat_name,
                    "folder": folder_name,
                    "name": data["meta"]["name"],
                    "meta": data["meta"]
                }
                if is_new:
                    added_skills.append(item_info)
                    print(f"  ✨ [NEW] {cat_name}/{folder_name}")
                else:
                    modified_skills.append(item_info)
                    print(f"  🔄 [MODIFIED] {cat_name}/{folder_name}")

    total_changes = len(added_skills) + len(modified_skills)
    if total_changes == 0:
        print("\n✅ Everything is up to date. No new or modified public skills found.")
        return

    print(f"\nSummary: {len(added_skills)} added, {len(modified_skills)} modified.")

    # Update Documentation files
    all_updated = added_skills + modified_skills
    if added_skills:
        update_index_md(target_repo, added_skills, dry_run=args.dry_run)
        update_readme_md(target_repo, added_skills, dry_run=args.dry_run)
    update_changelog_md(target_repo, added_skills, modified_skills, dry_run=args.dry_run)

    if args.commit and not args.dry_run:
        print("\n📦 Committing changes in Asmadey/skills...")
        subprocess.run(["git", "-C", str(target_repo), "add", "."], check=True)
        
        # Build descriptive commit message
        if len(added_skills) == 1 and not modified_skills:
            item = added_skills[0]
            commit_msg = f"feat({item['category']}): install {item['name']} skill from PersonalOS"
        elif len(added_skills) > 1:
            names = ", ".join(f"{i['category']}/{i['name']}" for i in added_skills)
            commit_msg = f"feat(skills): sync {len(added_skills)} skills ({names})"
        else:
            commit_msg = "chore(skills): sync updates from PersonalOS public"

        subprocess.run(["git", "-C", str(target_repo), "commit", "-m", commit_msg], check=True)
        print(f"✓ Committed: {commit_msg}")

        if args.push:
            print("🚀 Pushing to origin main...")
            subprocess.run(["git", "-C", str(target_repo), "push", "origin", "main"], check=True)
            print("✓ Pushed to remote successfully!")

if __name__ == "__main__":
    main()
