from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import re
from typing import Optional
from dotenv import load_dotenv
import nltk
from textblob import TextBlob
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import unicodedata

# Carregar variáveis de ambiente
load_dotenv()

app = FastAPI(
    title="AutoU - Classificação Automática de Emails",
    description="API para classificação e análise automática de emails usando IA",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class EmailRequest(BaseModel):
    text: str

class EmailResponse(BaseModel):
    category: str
    suggested_response: str
    confidence: float
    keywords: list[str]

# Palavras-chave para classificação
PRODUCTIVE_KEYWORDS = [
    "problema", "erro", "bug", "suporte", "ajuda", "urgente", "crítico",
    "solicitação", "pedido", "requisição", "atualização", "status",
    "dúvida", "pergunta", "consulta", "informação", "detalhes",
    "reclamação", "reembolso", "cancelamento", "modificação",
    "técnico", "sistema", "aplicação", "software", "hardware",
    "conta", "pagamento", "fatura", "boleto", "transferência", 
    "serviço", "servicos", "catálogo", "catalogo", "apresentação",
    "apresentacao", "informacoes", "informações", "valor",
    "valores", "preço", "precos", "preco", "preços", 
    "contrato", "contratação", "contratacao", "proposta", "orçamento", "orcamento",
    "negociação", "negociacao", "documentação", "documentacao", "documento", "assinatura",
    "envio", "recebimento", "processamento", "aprovação", "aprovacao", "homologação", "homologacao",
    "implantação", "implantacao", "treinamento", "agendamento", "agendar", "marcação", "marcacao",
    "resposta", "retorno", "feedback", "solução", "solucao", "ajuste", "correção", "correcao",
    "atendimento", "relatório", "relatorio", "análise", "analise", "relacionamento", "progresso",
    "andamento", "finalização", "finalizacao", "conclusão", "conclusao", "implementação", "implementacao",
    "atualizar", "atualizado", "pendência", "pendencia", "regularização", "regularizacao",
    "cadastro", "recadastro", "alteração", "alteracao", "inclusão", "inclusao", "exclusão", "exclusao",
    "ajustes", "melhoria", "melhorias", "otimização", "otimizacao", "planejamento", "planejar",
    "cronograma", "prazo", "prazos", "entrega", "entregas", "disponibilidade", "disponível", "disponivel",
    "implementado", "implementada", "implantado", "implantada", "solicitado", "solicitada",
    "confirmar", "confirmação", "confirmacao", "comprovação", "comprovacao", "comprovante",
    "atualizações", "atualizacoes", "esclarecimento", "esclarecimentos", "explicação", "explicacao",
    "demanda", "demandas", "prioridade", "prioridades", "urgência", "urgencia", "emergência", "emergencia",
    "resolução", "resolucao", "resolvido", "resolvida", "tratativa", "tratativas", "monitoramento",
    "monitorar", "acompanhamento", "acompanhar", "protocolo", "registro", "registrar", "solicitante",
    "responsável", "responsavel", "responsáveis", "responsaveis", "departamento", "setor", "equipe",
    "colaborador", "colaboradora", "colaboradores", "cliente", "clientes", "usuário", "usuario", "usuários", "usuarios"
]

UNPRODUCTIVE_KEYWORDS = [
    "feliz", "natal", "ano novo", "parabéns", "comemoração",  "sucesso", "vida",
    "saúde", "prosperidade", "alegria", "amor", "paz",
    "bênção", "deus", "fé", "esperança", "carinho",
    "beijo", "saudação", "cumprimento", "saudade", "agradecer",
    # Palavras e perguntas irrelevantes
    "como vai", "tudo bem", "bom dia", "boa tarde", "boa noite",
    "espero que esteja bem", "espero que todos estejam bem",
    "como estão", "como está", "como estão as coisas",
    "tudo certo", "tudo tranquilo", "novidades", "alguma novidade",
    "só para saber", "apenas para saber", "curiosidade",
    "só queria saber", "apenas queria saber", "tudo ok",
    "tudo em ordem", "como foi o final de semana", "como foi o fim de semana",
    "como foi o feriado", "como foi o dia", "como foi a semana",
    "como estão as coisas por aí", "como estão as coisas ai",
    "como estão todos", "como está a família", "como está a equipe",
    "espero que esteja tudo bem", "espero que esteja tudo certo",
    "espero que esteja tudo tranquilo", "espero que esteja tudo em ordem",
    "só passando para", "apenas passando para", "passando para desejar",
    "passando para saber", "passando para perguntar",
    "tudo em paz", "tudo tranquilo por aí", "tudo tranquilo ai",
    "tudo ótimo", "tudo maravilhoso", "tudo excelente",
    "como posso ajudar", "posso ajudar em algo", "precisa de algo",
    "precisa de alguma coisa", "precisa de ajuda", "precisa de apoio",
    "precisa de suporte", "precisa de mim", "precisa de alguma informação",
    "precisa de alguma novidade", "precisa de alguma atualização",
    "só queria perguntar", "apenas queria perguntar",
    "só para perguntar", "apenas para perguntar",
    "só para confirmar", "apenas para confirmar",
    "só para avisar", "apenas para avisar",
    "só para lembrar", "apenas para lembrar",
    "só para agradecer", "apenas para agradecer",
    "só para cumprimentar", "apenas para cumprimentar",
    "só para desejar", "apenas para desejar",
    "tudo bem com você", "tudo bem com voces", "tudo bem com vocês",
    "tudo bem com a equipe", "tudo bem com a família",
    "como estão todos por aí", "como estão todos ai",
    "como estão todos vocês", "como estão todos voces",
    "como estão todos da equipe", "como estão todos da família",
]

def remove_accents(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = remove_accents(text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_keywords(text: str) -> list[str]:
    """Extrai palavras-chave do texto"""
    processed_text = preprocess_text(text)
    words = processed_text.split()
    
    # Filtrar palavras com mais de 3 caracteres
    keywords = [word for word in words if len(word) > 3]
    
    return keywords[:10]  # Retorna as 10 primeiras palavras-chave

def classify_email_with_hf(text: str) -> dict:
    processed = preprocess_text(text)
    words = set(processed.split())
    prod_words = set(PRODUCTIVE_KEYWORDS)
    unprod_words = set(UNPRODUCTIVE_KEYWORDS)
    if words & unprod_words:
        category = 'Improdutivo'
        confidence = 0.9
    elif words & prod_words:
        category = 'Produtivo'
        confidence = 0.9
    else:
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        if sentiment > 0.2:
            category = 'Improdutivo'
        elif sentiment < -0.2:
            category = 'Produtivo'
        else:
            category = 'Neutro'
        confidence = 0.6
    return {"category": category, "confidence": confidence, "method": "rule_based"}

def generate_response(text: str, category: str) -> str:
    email_text = text.lower()
    if category == "Produtivo" and any(palavra in email_text for palavra in ["serviço", "servicos", "catálogo", "catalogo", "apresentação", "apresentacao", "informação", "informacoes", "informações"]):
        return (
            "Olá! Agradecemos seu interesse nos serviços da AutoU. Em breve, nossa equipe enviará um catálogo ou apresentação com todas as informações solicitadas. Caso tenha dúvidas específicas, estamos à disposição!"
        )
    if category == "Produtivo":
        return (
            "Olá! Recebemos sua solicitação e estamos analisando o seu caso. Nossa equipe AutoU irá retornar com uma resposta detalhada em breve. Agradecemos pelo contato!"
        )
    elif category == "Improdutivo":
        return (
            "Olá! Agradecemos sua mensagem e os votos positivos. A equipe AutoU deseja tudo em dobro para você!"
        )
    else:
        return (
            "Olá! Recebemos sua mensagem. Caso precise de suporte, estamos à disposição. Equipe AutoU."
        )

@app.get("/")
async def read_root():
    """Endpoint raiz - serve a interface web"""
    return FileResponse("public/index.html")

@app.post("/api/analyze")
async def analyze_email(request: EmailRequest):
    try:
        text = request.text.strip()
        if not text:
            raise HTTPException(status_code=400, detail="Texto do email não pode estar vazio")
        keywords = extract_keywords(text)
        result = classify_email_with_hf(text)
        category = result["category"]
        confidence = result["confidence"]
        suggested_response = generate_response(text, category)
        return {
            "category": category,
            "suggested_response": suggested_response,
            "confidence": confidence,
            "keywords": keywords
        }
    except Exception as e:
        print(f"Erro na análise: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/api/health")
async def health_check():
    """Endpoint de verificação de saúde da API"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

# Servir arquivos estáticos
app.mount("/public", StaticFiles(directory="public"), name="public")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 