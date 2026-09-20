import re

with open('backend/app/routers/ai_insights_router.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '"transaction_id": tx.transaction_id,',
    '"transaction_id": tx.transaction_id,\n            "tx_pk": tx.id,'
)

with open('backend/app/routers/ai_insights_router.py', 'w', encoding='utf-8') as f:
    f.write(content)
