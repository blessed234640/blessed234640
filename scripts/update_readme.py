#!/usr/bin/env python3
"""
Скрипт для автоматического обновления README.md
"""
import requests
import datetime
import pytz
import re

def get_github_stats(username):
    """Получение статистики с GitHub API"""
    try:
        api_url = f"https://api.github.com/users/{username}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return {
                'public_repos': data.get('public_repos', 0),
                'followers': data.get('followers', 0),
                'following': data.get('following', 0)
            }
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

def update_readme():
    username = "blessed234640"
    stats = get_github_stats(username)
    
    moscow_tz = pytz.timezone('Europe/Moscow')
    current_time = datetime.datetime.now(moscow_tz)
    formatted_time = current_time.strftime("%d.%m.%Y %H:%M MSK")
    
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print("README.md not found!")
        return
    
    stats_block = f"""### 🚀 Динамическая статистика

<!-- LAST_UPDATED: {formatted_time} -->

> 📊 Статистика обновляется автоматически

- **Последнее обновление:** {formatted_time}
- **Публичные репозитории:** {stats.get('public_repos', 0)}
- **Подписчики:** {stats.get('followers', 0)}
- **Подписки:** {stats.get('following', 0)}

"""
    
    if "### 🚀 Динамическая статистика" in content:
        pattern = r'### 🚀 Динамическая статистика.*?<!-- LAST_UPDATED:.*?-->'
        content = re.sub(pattern, stats_block, content, flags=re.DOTALL)
    else:
        content = content.replace('# Артур Азимов', f'# Артур Азимов\n\n{stats_block}')
    
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"✅ README updated at {formatted_time}")

if __name__ == "__main__":
    update_readme()