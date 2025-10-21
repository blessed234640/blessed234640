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
        # Основные данные пользователя
        api_url = f"https://api.github.com/users/{username}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return {
                'public_repos': data.get('public_repos', 0),
                'followers': data.get('followers', 0),
                'following': data.get('following', 0)
            }
        else:
            print(f"API Error: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {}

def update_readme():
    username = "blessed234640"
    
    # Получаем статистику
    stats = get_github_stats(username)
    
    # Текущее время
    moscow_tz = pytz.timezone('Europe/Moscow')
    current_time = datetime.datetime.now(moscow_tz)
    formatted_time = current_time.strftime("%d.%m.%Y %H:%M MSK")
    
    # Чтение текущего README
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print("README.md not found!")
        return
    
    # Создаем блок с обновленной статистикой
    stats_block = f"""### 🚀 Динамическая статистика

<!-- LAST_UPDATED: {formatted_time} -->

> 📊 Статистика обновляется автоматически

- **Последнее обновление:** {formatted_time}
- **Публичные репозитории:** {stats.get('public_repos', 0)}
- **Подписчики:** {stats.get('followers', 0)}
- **Подписки:** {stats.get('following', 0)}

[![Update Stats](https://github.com/blessed234640/blessed234640/actions/workflows/update-stats.yml/badge.svg)](https://github.com/blessed234640/blessed234640/actions/workflows/update-stats.yml)
"""
    
    # Заменяем или добавляем блок статистики
    if "### 🚀 Динамическая статистика" in content:
        # Заменяем существующий блок
        pattern = r'### 🚀 Динамическая статистика.*?\[!\[Update Stats\]\(.*?\)\]\(.*?\)'
        content = re.sub(pattern, stats_block, content, flags=re.DOTALL)
    else:
        # Добавляем после заголовка
        content = content.replace('# Артур Азимов', f'# Артур Азимов\n\n{stats_block}')
    
    # Запись обновленного README
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"✅ README updated at {formatted_time}")
    print(f"📊 Stats: {stats}")

if __name__ == "__main__":
    update_readme()