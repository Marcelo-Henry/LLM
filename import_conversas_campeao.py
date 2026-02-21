# import_conversas_campeao.py
import psycopg2
import os

# Conectar ao banco
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="seattle",
    user="postgres",
    password="postgres"
)

# Criar diretório se não existir
os.makedirs("rag/whatsapp_campeas", exist_ok=True)

# Buscar conversas campeãs
cur = conn.cursor()
cur.execute("""
    SELECT phone, titulo, descricao 
    FROM ia_conversas_campeao 
    WHERE ativo = true 
    ORDER BY ordem
""")

conversas_campeao = cur.fetchall()

for phone, titulo, descricao in conversas_campeao:
    print(f"\n📞 Processando: {titulo} ({phone})")
    
    # Buscar mensagens da conversa
    cur.execute("""
        SELECT 
            from_me,
            message_text,
            to_timestamp(timestamp/1000) as msg_time
        FROM whatsapp_mensagens
        WHERE phone = %s
          AND message_type = 'text'
          AND message_text IS NOT NULL
          AND message_text != ''
        ORDER BY timestamp
    """, (phone,))
    
    mensagens = cur.fetchall()
    
    # Montar conversa formatada
    conversa_texto = f"CONVERSA CAMPEÃ: {titulo}\n"
    if descricao:
        conversa_texto += f"Descrição: {descricao}\n"
    conversa_texto += f"Telefone: {phone}\n"
    conversa_texto += f"Total de mensagens: {len(mensagens)}\n"
    conversa_texto += "="*80 + "\n\n"
    
    for from_me, text, msg_time in mensagens:
        remetente = "Vendedor" if from_me else "Cliente"
        conversa_texto += f"{remetente}: {text}\n\n"
    
    # Salvar em arquivo
    filename = f"rag/whatsapp_campeas/{phone}_{titulo.replace(' ', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(conversa_texto)
    
    print(f"✅ Salva em {filename} ({len(mensagens)} mensagens)")

cur.close()
conn.close()

print(f"\n🎉 Total de conversas campeãs exportadas: {len(conversas_campeao)}")

