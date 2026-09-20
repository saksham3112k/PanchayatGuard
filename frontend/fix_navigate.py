with open('src/layouts/AppLayout.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("import { Outlet, Navigate, Link, useLocation } from 'react-router-dom';", "import { Outlet, Navigate, Link, useLocation, useNavigate } from 'react-router-dom';")
content = content.replace("const location = useLocation();", "const location = useLocation();\n  const navigate = useNavigate();")

with open('src/layouts/AppLayout.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
