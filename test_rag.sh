#!/bin/bash
cd /Users/henrylle/Projetos/formacaoaws/Tools_LLM
source venv/bin/activate

echo "=== Testando sistema RAG ==="
echo ""

cat << 'EOF' | python3 main.py 2>&1 | tail -50
/rag
/rag status
/rag enable
/rag status
/rag add Teste de conhecimento
/rag view
exit
EOF
