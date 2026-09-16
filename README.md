# AI IT Support — AWS Generative AI

Aplicação de suporte de TI baseada em **Inteligência Artificial Generativa**, desenvolvida utilizando serviços da AWS para consultar uma base de conhecimento e fornecer respostas contextualizadas para problemas e dúvidas relacionados a suporte técnico.

O projeto utiliza **Amazon Bedrock** para geração das respostas, **Knowledge Bases** para Retrieval-Augmented Generation (RAG) e uma arquitetura serverless para disponibilizar a aplicação.

---

## 📌 Visão geral

O sistema funciona como um assistente virtual de suporte de TI capaz de consultar informações previamente disponibilizadas em uma base de conhecimento e gerar respostas utilizando modelos de linguagem.

O projeto foi desenvolvido com foco em:

* IA Generativa
* RAG (Retrieval-Augmented Generation)
* Arquitetura serverless
* Segurança de APIs
* Integração entre serviços AWS
* Automação de processos de suporte

---

## 🏗️ Arquitetura

```text
┌──────────────────────┐
│      Streamlit       │
│    Web Interface     │
└──────────┬───────────┘
           │
           │ HTTPS
           ▼
┌──────────────────────┐
│    Amazon API        │
│       Gateway        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   AWS Lambda         │
│  AI Support API      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Amazon Bedrock     │
│   Foundation Model   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Knowledge Base      │
│       RAG            │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Amazon S3      │
│  Knowledge Documents │
└──────────────────────┘
```

---

## 🔄 Fluxo da aplicação

1. O usuário envia uma pergunta através da interface desenvolvida em **Streamlit**.
2. A aplicação encaminha a requisição para uma API HTTP disponibilizada pelo **Amazon API Gateway**.
3. O API Gateway direciona a requisição para uma função **AWS Lambda**.
4. A Lambda processa a solicitação e realiza a integração com o **Amazon Bedrock**.
5. A **Knowledge Base** recupera as informações relevantes presentes na base de conhecimento.
6. O conteúdo recuperado é utilizado como contexto para a geração da resposta.
7. O modelo de IA gera a resposta contextualizada.
8. A resposta retorna pela Lambda → API Gateway → aplicação Streamlit.

---

## 🧠 Retrieval-Augmented Generation (RAG)

O projeto utiliza **RAG** para permitir que o modelo consulte informações externas antes de gerar uma resposta.

Em vez de depender exclusivamente do conhecimento interno do modelo, a aplicação utiliza uma **Knowledge Base** contendo documentos relacionados ao ambiente de suporte.

O processo pode ser representado por:

```text
Pergunta do usuário
        │
        ▼
   Recuperação
        │
        ▼
Documentos relevantes
        │
        ▼
Contexto para o modelo
        │
        ▼
Resposta contextualizada
```

Essa abordagem permite utilizar informações específicas do ambiente sem a necessidade de realizar o treinamento de um modelo do zero.

---

## ☁️ Serviços AWS utilizados

### Amazon Bedrock

Responsável pela integração com modelos de **Foundation Models (FMs)** e pela geração das respostas utilizando IA Generativa.

---

### Amazon Bedrock Knowledge Bases

Utilizada para implementar a arquitetura **RAG**, permitindo que o sistema consulte informações armazenadas na base de conhecimento antes de gerar uma resposta.

---

### AWS Lambda

Executa a lógica da API de forma **serverless**, processando as requisições e realizando a integração entre a aplicação, o API Gateway e o Amazon Bedrock.

---

### Amazon API Gateway

Disponibiliza a API HTTP responsável por receber as requisições da aplicação e encaminhá-las para a função Lambda.

---

### Amazon S3

Utilizado como armazenamento dos documentos utilizados como fonte para a **Knowledge Base**.

---

## 🖥️ Front-end

A interface foi desenvolvida utilizando **Streamlit**, permitindo que o usuário interaja com o assistente de suporte através de uma aplicação web.

Principais responsabilidades:

* Entrada das perguntas;
* Comunicação com a API;
* Exibição das respostas;
* Interface simples para interação com o assistente.

---

## 🔐 Segurança

O projeto considera mecanismos de segurança em diferentes camadas da arquitetura.

### API

A comunicação entre a aplicação e a API ocorre através de HTTPS.

### Autenticação

A API utiliza um mecanismo de autenticação baseado em token para validar as requisições.

### IAM

Os serviços AWS utilizam **AWS Identity and Access Management (IAM)** para controlar as permissões necessárias entre os componentes da arquitetura.

---

## 🛠️ Tecnologias

| Tecnologia              | Utilização                             |
| ----------------------- | -------------------------------------- |
| Python                  | Desenvolvimento da aplicação e backend |
| Streamlit               | Interface web                          |
| AWS Lambda              | Backend serverless                     |
| Amazon API Gateway      | Exposição da API                       |
| Amazon Bedrock          | IA Generativa                          |
| Bedrock Knowledge Bases | RAG                                    |
| Amazon S3               | Armazenamento dos documentos           |
| IAM                     | Controle de acesso                     |
| Boto3                   | Integração Python com AWS              |

---

## 💻 Backend

A função Lambda atua como camada de integração entre a API e os serviços de IA da AWS.

Responsabilidades principais:

* Receber requisições;
* Validar os dados recebidos;
* Processar a pergunta;
* Interagir com o Amazon Bedrock;
* Consultar a Knowledge Base;
* Retornar a resposta para o cliente.

---

## 🌐 API

A aplicação utiliza uma API HTTP para separar a interface do usuário da camada de processamento.

```text
Streamlit
    │
    │ HTTPS
    ▼
API Gateway
    │
    ▼
Lambda
    │
    ▼
Amazon Bedrock
```

Essa separação permite manter a interface desacoplada da lógica de processamento e dos serviços de IA.

---

## 📚 Base de conhecimento

Os documentos utilizados pelo sistema são armazenados no **Amazon S3** e disponibilizados para a Knowledge Base.

A arquitetura permite que novos conteúdos sejam incorporados à base de conhecimento, possibilitando que o assistente utilize informações adicionais nas respostas sem alterar diretamente o código da aplicação.

---

## 🎯 Objetivo do projeto

O projeto foi desenvolvido como uma aplicação prática de **IA Generativa aplicada ao suporte de TI**, explorando a integração de diferentes serviços da AWS em uma arquitetura serverless.

Além da geração de respostas, o projeto demonstra conceitos como:

* Foundation Models;
* Prompt Engineering;
* RAG;
* Embeddings;
* Knowledge Bases;
* APIs;
* Serverless;
* IAM;
* Integração entre serviços AWS;
* Desenvolvimento de aplicações utilizando IA Generativa.


## 🚀 Principais conceitos demonstrados

```text
Generative AI
     │
     ├── Foundation Models
     ├── Prompt Engineering
     ├── RAG
     ├── Knowledge Bases
     └── Embeddings
     
AWS
     │
     ├── Bedrock
     ├── Lambda
     ├── API Gateway
     ├── S3
     └── IAM
     
Application
     │
     ├── Python
     ├── Streamlit
     └── REST API
```

---

## 👨‍💻 Autor

**Bernardo Santos Ferreira**

Estudante de Engenharia de Software e profissional de suporte de TI, com foco em infraestrutura, observabilidade, computação em nuvem e Inteligência Artificial.

### Certificações

* AWS Certified AI Practitioner

### Atualmente estudando

* AWS Cloud Practitioner
* Cloud Computing
* Generative AI
* AWS
* Infrastructure & Observability

---

## 📄 Licença

Este projeto foi desenvolvido para fins de estudo, portfólio e demonstração técnica.
