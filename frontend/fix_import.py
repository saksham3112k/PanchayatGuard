with open('src/pages/Grievances.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("import api from '../services/api';", "import api from '../services/api';\nimport GrievanceModal from '../components/GrievanceModal';")

with open('src/pages/Grievances.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
