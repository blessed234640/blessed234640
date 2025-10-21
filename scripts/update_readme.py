#!/usr/bin/env python3
"""
Скрипт для автоматического обновления README.md
"""
import requests
import datetime
import pytz

def get_github_stats(username):
    """Получение статистики с GitHub API"""
    try:
        # Пример: получение основных данных пользователя
        api_url = f"https://api.github.com/users/{username}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return {
                'public_repos': data.get('public_repos', 0),
                'followers': data.get('followers', 0),
                'following': data.get('following', 0),
                'total_commits': 0  # Это нужно получать отдельно
            }
        return {}
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {}

def update_readme():
    username = "blessed234640"
    stats = get_github_stats(username)
    
    # Текущее время
    moscow_tz = pytz.timezone('Europe/Moscow')
    current_time = datetime.datetime.now(moscow_tz)
    formatted_time = current_time.strftime("%d.%m.%Y %H:%M MSK")
    
    # Чтение текущего README
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Замена или добавление блока с временем обновления
    update_section = f"<!-- LAST_UPDATED: {formatted_time} -->"
    
    if "<!-- LAST_UPDATED:" in content:
        # Заменяем существующую метку
        import re
        content = re.sub(
            r'<!-- LAST_UPDATED:.*?-->',
            update_section,
            content
        )
    else:
        # Добавляем в начало файла
        content = update_section + "\n\n" + content
    
    # Запись обновленного README
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"README updated at {formatted_time}")
    print(f"Stats: {stats}")

if __name__ == "__main__":
    update_readme()