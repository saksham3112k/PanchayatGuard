with open('.gitignore', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('\ndist\n', '\n#dist\n')

with open('.gitignore', 'w', encoding='utf-8') as f:
    f.write(content)
