with open('src/layouts/AppLayout.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re
# 1. Add state for district
content = content.replace("const [searchResults, setSearchResults] = useState<any[]>([]);", "const [searchResults, setSearchResults] = useState<any[]>([]);\n    const [currentDistrict, setCurrentDistrict] = useState('Uttar Pradesh');")

# 2. Add useEffect to read prefs
use_effect = """
    useEffect(() => {
        const loadPrefs = () => {
            const p = JSON.parse(localStorage.getItem('pg_prefs') || '{"theme":"Light","district":"All Districts","showAi":true}');
            if (p.district && p.district !== 'All Districts') {
                setCurrentDistrict(p.district + ', UP');
            } else {
                setCurrentDistrict('Uttar Pradesh');
            }
            if (p.theme === 'Dark') {
                document.body.classList.add('dark-theme');
            } else {
                document.body.classList.remove('dark-theme');
            }
        };
        loadPrefs();
        window.addEventListener('theme_changed', loadPrefs);
        return () => window.removeEventListener('theme_changed', loadPrefs);
    }, []);
"""
content = content.replace("useEffect(() => {\n    const fetchUnread = async () => {", use_effect + "\n    useEffect(() => {\n    const fetchUnread = async () => {")

# 3. Replace Uttar Pradesh with state
content = content.replace("<span>Uttar Pradesh</span>", "<span>{currentDistrict}</span>")

with open('src/layouts/AppLayout.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

# Add dark-theme CSS to index.css
with open('src/index.css', 'a', encoding='utf-8') as f:
    f.write("\n\n/* Simple inverted dark mode for dashboard */\nbody.dark-theme {\n  filter: invert(1) hue-rotate(180deg);\n  background-color: #f3f4f6;\n}\nbody.dark-theme img, body.dark-theme .avatar {\n  filter: invert(1) hue-rotate(180deg);\n}\n")
