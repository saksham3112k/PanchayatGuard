with open('frontend/src/layouts/AppLayout.tsx', 'r') as f:
    content = f.read()

import re
match = re.search(r'\{showNotifs && \(.*?\n\s+\)\}', content, re.DOTALL)
if match:
    print(match.group(0))
