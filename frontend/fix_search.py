with open('src/layouts/AppLayout.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add import for TransactionDetails
content = content.replace("import api from '../services/api';", "import api from '../services/api';\nimport TransactionDetails from '../components/TransactionDetails';")

# Add state for viewing transaction
content = content.replace("const [searchResults, setSearchResults] = useState<any[]>([]);", "const [searchResults, setSearchResults] = useState<any[]>([]);\n    const [viewingTxId, setViewingTxId] = useState<number | null>(null);")

# Handle Search Click function
search_handler = """
    const handleSearchClick = (res: any) => {
        setSearchQuery('');
        setSearchResults([]);
        if (res.type === 'Vendor') {
            navigate(`/vendors/${res.id}`);
        } else if (res.type === 'Transaction') {
            setViewingTxId(res.id);
        } else if (res.type === 'Panchayat') {
            navigate('/geo');
        }
    };
"""
content = content.replace("useEffect(() => {\n      if(user) {", search_handler + "\n    useEffect(() => {\n      if(user) {")

# Update onClick in JSX
content = content.replace(
    '<div key={i} className="px-4 py-2 hover:bg-gray-50 cursor-pointer">',
    '<div key={i} onClick={() => handleSearchClick(res)} className="px-4 py-2 hover:bg-gray-50 cursor-pointer">'
)

# Add TransactionDetails Modal at the bottom
content = content.replace(
    "</main>\n      </div>\n    </div>",
    "</main>\n        {viewingTxId && <TransactionDetails isOpen={true} txId={viewingTxId} onClose={() => setViewingTxId(null)} />}\n      </div>\n    </div>"
)

with open('src/layouts/AppLayout.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
