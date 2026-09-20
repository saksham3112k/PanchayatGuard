import re

with open('src/pages/Vendors.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "import { Search,", 
    "import VendorModal from '../components/VendorModal';\nimport { Search,"
)

content = content.replace(
    "const [loading, setLoading] = useState(true);", 
    "const [loading, setLoading] = useState(true);\n  const [isModalOpen, setIsModalOpen] = useState(false);"
)

content = content.replace(
    '<button className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-white bg-pg-blue rounded hover:bg-blue-700 shadow-sm">\n                  <Plus className="w-4 h-4" /> Add Vendor\n               </button>', 
    '<button onClick={() => setIsModalOpen(true)} className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-white bg-pg-blue rounded hover:bg-blue-700 shadow-sm">\n                  <Plus className="w-4 h-4" /> Add Vendor\n               </button>'
)

content = content.replace(
    "</div>\n    </div>", 
    "</div>\n      <VendorModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onSuccess={() => { setIsModalOpen(false); fetchVendors(); }} />\n    </div>"
)

content = content.replace('<button className="p-1 text-pg-blue hover:bg-blue-50 rounded"><Edit className="w-4 h-4"/></button>', '')
content = content.replace(',1', '₹')
content = content.replace(',1', '₹')

with open('src/pages/Vendors.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
