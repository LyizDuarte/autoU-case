# 🤖 AutoU - Classificação Automática de Emails

Solução digital para classificação automática de emails, desenvolvida para empresas do setor financeiro que lidam com alto volume de emails diariamente.

## 🎯 Objetivo

Automatizar a leitura e classificação de emails, sugerindo classificações e respostas automáticas de acordo com o teor de cada email recebido, liberando tempo da equipe para focar em tarefas mais importantes.

## ✨ Funcionalidades

- **📧 Upload de Emails**: Suporte para arquivos .txt e .pdf
- **✏️ Inserção Direta**: Cole o conteúdo do email diretamente
- **🤖 Classificação Inteligente**: Análise automática baseada em palavras-chave e sentimento
- **📊 Categorização**: Produtivo, Improdutivo ou Neutro
- **💬 Respostas Automáticas**: Respostas institucionais por template
- **🎨 Interface Moderna**: Design neumórfico responsivo
- **☁️ Deploy na Nuvem**: Compatível com Vercel

## 🚀 Tecnologias

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **NLP**: NLTK, TextBlob
- **Deploy**: Vercel

## 📋 Pré-requisitos

- Python 3.8+

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd case-autoU
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Executando Localmente

### Desenvolvimento

```bash
python api/index.py
```
### Caso o comando acima retorne erros, tente esse:
```bash
python -m api.index
```

### Produção

```bash
uvicorn api.index:app --host 0.0.0.0 --port 8000
```

A aplicação estará disponível em: `http://localhost:8000`

## 📚 Endpoints da API

### `GET /`

- **Descrição**: Interface web principal
- **Resposta**: HTML da aplicação

### `POST /api/analyze`

- **Descrição**: Analisa e classifica um email
- **Body**:

```json
{
  "text": "Conteúdo do email aqui"
}
```

- **Resposta**:

```json
{
  "category": "Produtivo",
  "suggested_response": "Resposta automática gerada...",
  "confidence": 0.95,
  "keywords": ["palavra1", "palavra2"]
}
```

### `GET /api/health`

- **Descrição**: Verificação de saúde da API
- **Resposta**:

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## 🎨 Categorias de Classificação

### 📈 Produtivo

Emails que requerem uma ação ou resposta específica:

- Solicitações de suporte técnico
- Atualizações sobre casos em aberto
- Dúvidas sobre o sistema
- Reclamações e pedidos
- Problemas urgentes

### 📉 Improdutivo

Emails que não necessitam de uma ação imediata:

- Mensagens de felicitações
- Agradecimentos
- Cumprimentos informais
- Mensagens de marketing não solicitadas

### ⚪ Neutro

Emails que não se encaixam claramente nas categorias acima.

## 🚀 Deploy na Vercel

### 1. Prepare o projeto

```bash
# Certifique-se de que todos os arquivos estão commitados
git add .
git commit -m "Preparando para deploy"
```

### 2. Conecte ao Vercel

1. Acesse [vercel.com](https://vercel.com)
2. Conecte seu repositório GitHub

### 3. Deploy automático

O Vercel detectará automaticamente o `vercel.json` e fará o deploy.

## 🧪 Testando a Aplicação

### Exemplos de Emails para Teste

**Email Produtivo:**

```
Preciso de ajuda urgente com minha conta.
Não consigo acessar o sistema há 2 dias e tenho uma transação pendente.
Por favor, me ajudem a resolver isso o quanto antes.
```

**Email Improdutivo:**

```
Feliz Natal!
Desejo a todos vocês um ano novo cheio de alegria e prosperidade.
Obrigado por todo o suporte durante o ano.
```

**Email Neutro:**

```
Olá,
Gostaria de saber mais informações sobre os serviços oferecidos pela empresa.
Vocês podem me enviar um catálogo ou uma apresentação?
Obrigado!
```

## 🔍 Como Funciona

### 1. Processamento de Texto

- Pré-processamento (lowercase, remoção de acentos e caracteres especiais)
- Extração de palavras-chave
- Análise de sentimento (TextBlob)

### 2. Classificação

- **Palavras-chave**: Identifica termos produtivos ou improdutivos
- **Sentimento**: Usa polaridade para casos neutros

### 3. Geração de Resposta

- **Templates institucionais**: Respostas automáticas padronizadas por categoria
- **Sem uso de IA generativa**

## 🛠️ Estrutura do Projeto

```
case-autoU/
├── api/
│   └── index.py          # API FastAPI principal
├── public/
│   └── index.html        # Interface web
├── requirements.txt      # Dependências Python
├── vercel.json          # Configuração Vercel
└── README.md            # Este arquivo
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através dos canais oficiais da AutoU.

---

**Desenvolvido com ❤️ para automatizar e otimizar o processamento de emails**
