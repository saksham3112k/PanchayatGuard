with open('src/pages/AIInsights.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
content = content.replace("import api from '../services/api';", "import api from '../services/api';\nimport TransactionDetails from '../components/TransactionDetails';")

# Add state
content = content.replace("const [loading, setLoading] = useState(true);", "const [loading, setLoading] = useState(true);\n  const [viewingTxId, setViewingTxId] = useState<number | null>(null);")

# Update button
content = content.replace('<button className="px-4 py-2 border border-gray-300 rounded text-sm font-semibold text-pg-blue hover:bg-blue-50 transition-colors">View Details</button>', '<button onClick={() => setViewingTxId(insight.tx_pk)} className="px-4 py-2 border border-gray-300 rounded text-sm font-semibold text-pg-blue hover:bg-blue-50 transition-colors">View Details</button>')

# Add Modal at end
content = content.replace("</div>\n    </div>", "</div>\n      {viewingTxId && <TransactionDetails isOpen={true} txId={viewingTxId} onClose={() => setViewingTxId(null)} />}\n    </div>")

with open('src/pages/AIInsights.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
