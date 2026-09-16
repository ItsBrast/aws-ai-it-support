import streamlit as st
import requests
import os
from aws_requests_auth.aws_auth import AWSRequestsAuth

API_ID = os.environ.get("API_ID", "seu-api-id-aqui")
REGION = os.environ.get("AWS_REGION", "us-east-1")
API_HOST = f"{API_ID}.execute-api.{REGION}.amazonaws.com"
API_URL = f"https://{API_HOST}/ask"

API_TOKEN = os.environ.get("API_TOKEN", "")

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN", None)

if not AWS_ACCESS_KEY or not AWS_SECRET_KEY:
    st.error("As credenciais da AWS (Access Key / Secret Key) não foram encontradas nas variaveis de ambiente.")

if not API_TOKEN:
    st.warning("O token de acesso da API nao foi configurado.")

auth = AWSRequestsAuth(
    aws_access_key=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_token=AWS_SESSION_TOKEN,
    aws_host=API_HOST,
    aws_region=REGION,
    aws_service='execute-api'
)

st.set_page_config(page_title="Assistente TI", page_icon="")

st.title("Assistente de Suporte de TI")
st.markdown("Desenvolvido com AWS Bedrock, RAG e Seguranca IAM (SigV4).")

question = st.text_input("Qual e o seu problema tecnico?", placeholder="Ex: Minha VPN nao conecta...")

if st.button("Buscar Solucao"):
    if question:
        with st.spinner("Consultando a Base de Conhecimento na AWS..."):
            
            headers = {"x-api-token": API_TOKEN}
            payload = {"question": question}
            
            try:
                response = requests.post(API_URL, json=payload, headers=headers, auth=auth)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Resposta gerada com sucesso!")
                    
                    st.write(data.get("answer"))
                    
                    sources = data.get("sources", [])
                    if sources:
                        st.markdown("---")
                        st.subheader("Fontes Consultadas:")
                        for idx, src in enumerate(sources, 1):
                            uri = src.get("s3Location", {}).get("uri", "")
                            if uri:
                                filename = uri.split('/')[-1]
                                st.caption(f"{idx}. Documento de referencia: `{filename}`")
                
                elif response.status_code == 403:
                    st.error("Erro 403: Acesso bloqueado pelo IAM do API Gateway (Credenciais sem permissao ou invalidas).")
                elif response.status_code == 401:
                    st.error("Erro 401: Acesso negado pelo Lambda (Token do Lambda invalido).")
                else:
                    st.error(f"Erro na API: {response.status_code} - {response.text}")
                    
            except Exception as e:
                st.error(f"Erro de conexao: {e}")
    else:
        st.warning("Por favor, digite uma pergunta.")