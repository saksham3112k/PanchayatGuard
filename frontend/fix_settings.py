with open('src/pages/Settings.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("|| window.innerWidth >= 1024", "")

with open('src/pages/Settings.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
