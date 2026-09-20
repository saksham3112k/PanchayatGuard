with open('src/pages/Grievances.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(
    r'<button className="bg-pg-blue text-white px-4 py-2 rounded font-bold flex items-center gap-2 hover:bg-blue-700 transition-colors">\s*<Plus className="w-4 h-4"/> New Grievance\s*</button>',
    '<button onClick={() => { setEditData(null); setIsModalOpen(true); }} className="bg-pg-blue text-white px-4 py-2 rounded font-bold flex items-center gap-2 hover:bg-blue-700 transition-colors">\\n            <Plus className="w-4 h-4"/> New Grievance\\n          </button>',
    content
)

with open('src/pages/Grievances.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
