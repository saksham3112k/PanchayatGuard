with open('src/pages/Grievances.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("import { Search,", "import GrievanceModal from '../components/GrievanceModal';\nimport { Search,")

content = content.replace("const [loading, setLoading] = useState(true);", "const [loading, setLoading] = useState(true);\n  const [isModalOpen, setIsModalOpen] = useState(false);\n  const [editData, setEditData] = useState<any>(null);")

content = content.replace(
    '<button className="bg-pg-blue text-white px-4 py-2 rounded font-bold flex items-center gap-2 hover:bg-blue-700 transition-colors">\n            <Plus className="w-5 h-5" /> New Grievance\n        </button>',
    '<button onClick={() => { setEditData(null); setIsModalOpen(true); }} className="bg-pg-blue text-white px-4 py-2 rounded font-bold flex items-center gap-2 hover:bg-blue-700 transition-colors">\n            <Plus className="w-5 h-5" /> New Grievance\n        </button>'
)

content = content.replace(
    '<button className="text-pg-blue font-semibold hover:underline">View</button>',
    '<button onClick={() => { setEditData(g); setIsModalOpen(true); }} className="text-pg-blue font-semibold hover:underline">Update</button>'
)

content = content.replace(
    "</div>\n    </div>", 
    "</div>\n      <GrievanceModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} editData={editData} onSuccess={() => { setIsModalOpen(false); fetchGrievances(); }} />\n    </div>"
)

with open('src/pages/Grievances.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
