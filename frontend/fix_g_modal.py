with open('src/components/GrievanceModal.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("api.get('/panchayats').then(res => setPanchayats(res.data)).catch(console.error);", "api.get('/procurement/dropdowns').then(res => setPanchayats(res.data.panchayats)).catch(console.error);")

# Also fix the POST route just in case
content = content.replace("await api.post('/grievances', data);", "await api.post('/grievances/', data);")

with open('src/components/GrievanceModal.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
