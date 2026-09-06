import sys
import os
import re
from pathlib import Path

def get_skill_metadata(skill_path):
    skill_md = Path(skill_path) / "SKILL.md"
    if not skill_md.exists():
        return None, None
    
    content = skill_md.read_text()
    # Extract YAML frontmatter
    name_match = re.search(r"name:\s*['\"]?([\w-]+)['\"]?", content)
    desc_match = re.search(r"description:\s*(?:>|\|)?\s*(.*)", content)
    
    name = name_match.group(1).strip() if name_match else os.path.basename(skill_path)
    description = desc_match.group(1).strip() if desc_match else "Нет описания"
    
    # Handle multi-line descriptions if they start on next line or follow >
    if not description or len(description) < 5:
        # Simple heuristic for multi-line: find the description line and take the next non-empty line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "description:" in line:
                for next_line in lines[i+1:]:
                    if next_line.strip() and not next_line.strip().startswith(('---', 'name:', 'license:', 'category:')):
                        description = next_line.strip()
                        break
                break

    return name, description

def determine_category(name, description):
    content = (name + " " + description).lower()
    
    dev_keywords = ["development", "dev", "code", "architecture", "ревью", "разраб", "программирование", "react", "native", "go", "rust", "ui", "design system"]
    int_keywords = ["automation", "integration", "интеграция", "api", "airtable", "google", "slack", "jira", "notion", "supabase", "vercel", "автоматизация"]
    strat_keywords = ["strategy", "hypothesis", "jtbd", "стратегия", "гипотеза", "персона", "synthetic", "исследование"]
    anal_keywords = ["analytics", "аналитика", "wordstat", "вордстат", "search", "поиск", "tavily", "seo"]
    action_keywords = ["agent", "swarm", "telegram", "n8n", "cloud", "captcha", "капча", "автоматизация действий"]
    create_keywords = ["generator", "generation", "создание", "creation", "генерация", "контент", "pptx", "mcp", "skill"]

    if any(k in content for k in dev_keywords): return "🛠 Разработка и Инженерия (Development)"
    if any(k in content for k in int_keywords): return "🔌 Интеграции и Web-сервисы (Integrations)"
    if any(k in content for k in strat_keywords): return "🎯 Стратегия и Исследования (Strategy & Research)"
    if any(k in content for k in anal_keywords): return "📊 Аналитика и Сбор данных (Analytics)"
    if any(k in content for k in action_keywords): return "🤖 Автоматизация действий (Action Agents)"
    if any(k in content for k in create_keywords): return "🏗 Генерация контента и Создание навыков (Creation)"
    
    return "🛠 Разработка и Инженерия (Development)" # Default

def update_info_md(skill_name, description, category, python_support="Нет", api_key="Нет"):
    info_path = Path("/Users/asmadey/PersonalOS/skills/info.md")
    if not info_path.exists():
        print(f"Error: {info_path} not found")
        return

    content = info_path.read_text()
    
    # Check if skill already exists
    if f"| {skill_name} |" in content:
        print(f"Skill {skill_name} already exists in info.md")
        return

    new_row = f"| {skill_name} | {description} | При необходимости. | {python_support} | {api_key} |\n"
    
    # Find the category section and insert the row into its table
    category_pattern = rf"(## {re.escape(category)}.*?\n\|.*?\|.*?\n\|.*?\|.*?\|\n)"
    match = re.search(category_pattern, content, re.DOTALL)
    
    if match:
        new_content = content.replace(match.group(1), match.group(1) + new_row)
        info_path.write_text(new_content)
        print(f"Added {skill_name} to category: {category}")
    else:
        # If category not found, append to the end
        info_path.write_text(content + f"\n\n## {category}\n| Название скила | Описание | Триггер запуска | Python | API Key |\n| :--- | :--- | :--- | :--- | :--- |\n" + new_row)
        print(f"Created new category {category} and added {skill_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_info.py <skill_directory_path>")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    name, desc = get_skill_metadata(skill_dir)
    if not name:
        print(f"Error: Could not extract metadata from {skill_dir}/SKILL.md")
        sys.exit(1)
        
    category = determine_category(name, desc)
    update_info_md(name, desc, category)
