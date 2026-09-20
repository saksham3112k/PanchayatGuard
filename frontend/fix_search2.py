with open('src/layouts/AppLayout.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

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

content = content.replace("const navigate = useNavigate();", "const navigate = useNavigate();\n" + search_handler)

with open('src/layouts/AppLayout.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
