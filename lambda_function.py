import json
import boto3
import os
import time
from botocore.exceptions import ClientError

bedrock = boto3.client("bedrock-agent-runtime")
bedrock_runtime = boto3.client("bedrock-runtime")

KNOWLEDGE_BASE_ID = os.environ["KNOWLEDGE_BASE_ID"]
MODEL_ID = os.environ["MODEL_ID"]
API_TOKEN = os.environ.get("API_TOKEN")

def lambda_handler(event, context):
    print("Iniciando processamento da requisição")

    headers = event.get("headers", {})
    client_token = headers.get("x-api-token")

    if not client_token or client_token != API_TOKEN:
        print("Acesso negado: Token ausente ou inválido.")
        return {
            "statusCode": 401,
            "headers": {
                "Content-Type": "application/json; charset=utf-8"
            },
            "body": json.dumps(
                {"error": "Não autorizado."},
                ensure_ascii=False
            )
        }

    print("Autenticação validada com sucesso.")

    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json; charset=utf-8"
            },
            "body": json.dumps(
                {"error": "JSON inválido."},
                ensure_ascii=False
            )
        }

    question = body.get("question", "").strip()

    print(f"Pergunta recebida: {question}")

    if not question:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json; charset=utf-8"
            },
            "body": json.dumps(
                {"error": "A pergunta não foi informada."},
                ensure_ascii=False
            )
        }

    print("Consultando Knowledge Base...")
    start_kb_time = time.time()

    try:
        response = bedrock.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": question}
        )

        kb_latency = round(time.time() - start_kb_time, 2)

        print(
            f"Knowledge Base respondeu em {kb_latency} segundos."
        )

    except ClientError as e:
        print(f"Erro ao acessar Knowledge Base: {e}")

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json; charset=utf-8"
            },
            "body": json.dumps(
                {
                    "error": (
                        "Falha temporária ao consultar "
                        "a base de conhecimento."
                    )
                },
                ensure_ascii=False
            )
        }

    results = response.get("retrievalResults", [])

    print(f"Resultados encontrados: {len(results)}")

    if not results:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json; charset=utf-8"
            },
            "body": json.dumps(
                {
                    "question": question,
                    "answer": (
                        "Não encontrei informações suficientes "
                        "na base de conhecimento."
                    ),
                    "sources": []
                },
                ensure_ascii=False
            )
        }

    context_parts = [
        result.get("content", {}).get("text", "")
        for result in results
        if result.get("content", {}).get("text", "")
    ]

    context_text = "\n\n---\n\n".join(context_parts)

    print("Contexto montado com sucesso.")

    prompt = f"""
Você é um assistente de suporte de TI.

Responda à pergunta do usuário utilizando somente as informações
presentes no contexto fornecido.

Se a informação não estiver no contexto, diga claramente que
não encontrou essa informação na base de conhecimento.

Não invente procedimentos.

Contexto:
{context_text}

Pergunta do usuário:
{question}

Resposta:
"""

    print("Chamando Amazon Bedrock...")
    start_model_time = time.time()

    try:
        model_response = bedrock_runtime.converse(
            modelId=MODEL_ID,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            inferenceConfig={
                "maxTokens": 500,
                "temperature": 0.2
            }
        )

        model_latency = round(
            time.time() - start_model_time,
            2
        )

        print(
            f"Modelo respondeu em {model_latency} segundos."
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        print(
            f"Erro no Amazon Bedrock ({error_code}): {e}"
        )

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json; charset=utf-8"
            },
            "body": json.dumps(
                {
                    "error": (
                        "O serviço de IA está temporariamente "
                        "indisponível."
                    )
                },
                ensure_ascii=False
            )
        }

    output_message = model_response.get(
        "output",
        {}
    ).get(
        "message",
        {}
    )

    content_blocks = output_message.get(
        "content",
        []
    )

    answer = (
        content_blocks[0].get(
            "text",
            "Resposta gerada com sucesso."
        )
        if content_blocks
        else "Resposta gerada com sucesso."
    )

    print("Resposta gerada com sucesso.")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json; charset=utf-8"
        },
        "body": json.dumps(
            {
                "question": question,
                "answer": answer,
                "sources": [
                    result.get("location", {})
                    for result in results
                ]
            },
            ensure_ascii=False
        )
    }
