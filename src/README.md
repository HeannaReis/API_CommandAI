# Explicação da API Java Spring Boot: ComandoAI

Esta API Java Spring Boot faz parte do projeto ComandoAI, servindo como backend para uma aplicação Python de IA/GPT. Ela recebe dados processados pela aplicação Python, armazena-os e oferece funcionalidades de busca e recuperação.

## Visão Geral

A API é responsável por:

*   **Receber dados:** Receber, via requisições HTTP (REST), dados estruturados da aplicação Python (IA/GPT). Esses dados incluem perguntas, respostas, transcrições e contextos, juntamente com seus embeddings (representações vetoriais).

*   **Armazenamento:** Persistir esses dados em um banco de dados relacional (assumimos que seja PostgreSQL, mas pode ser configurado).

*   **Busca:** Realizar buscas de similaridade baseadas nos embeddings, permitindo encontrar informações relacionadas.

*   **Fornecimento:** Servir os dados persistidos e os resultados das buscas para outras aplicações (ex: front-end web, dashboards).

## Componentes Principais

A aplicação é estruturada em módulos, seguindo os padrões do Spring Boot:

1.  **Módulo AIComunication:** Lida com a comunicação de perguntas e respostas (Q&A):

    *   **`GPTCommunication` (Model):** Entidade JPA que representa uma comunicação entre o usuário e a IA. Contém a pergunta, a resposta, os embeddings da pergunta e resposta, e a data de criação.

    *   **`GTPCommunicationRequestDTO` (DTO):** Data Transfer Object (DTO) usado para receber dados de requisição para salvar uma comunicação Q&A.

    *   **`IGPTCommunicationRepository` (Repository):** Interface Spring Data JPA que fornece métodos para acessar e manipular dados de `GPTCommunication` no banco de dados.

    *   **`IGPTCommunicationService` (Service):** Interface que define a lógica de negócios para salvar comunicações Q&A e encontrar comunicações similares.

    *   **`GPTCommunicationServiceImpl` (Service Implementation):** Implementação da interface `IGPTCommunicationService`.  Usa o repositório para interagir com o banco de dados e implementa a lógica para encontrar comunicações similares com base nos embeddings (cálculo de similaridade de cosseno).

    *   **`GPTCommunicationController` (Controller):** Controlador REST que expõe endpoints para salvar comunicações Q&A (`/api/question_answers/save`) e encontrar comunicações similares (`/api/question_answers/similar`).

2.  **Módulo Context:** Gerencia o contexto da conversa:

    *   **`Context` (Model):** Entidade JPA que representa o contexto de uma conversa (um texto).

    *   **`ContextDTO` (DTO):** DTO usado para transferir dados de contexto.

    *   **`IContextRepository` (Repository):** Interface Spring Data JPA para acessar e manipular dados de `Context` no banco de dados.

    *   **`IContextService` (Service):** Interface para a lógica de negócios relacionada ao contexto.

    *   **`ContextServiceImpl` (Service Implementation):** Implementa `IContextService`. Salva o contexto no banco de dados e fornece o último contexto salvo.

    *   **`ContextController` (Controller):** Controlador REST que expõe endpoints para salvar um contexto (`/api/contexts/save`), obter o último contexto (`/api/contexts/last`), e obter todos os contextos (`/api/contexts/all`).

    *   **`ContextNotFoundException` (Exception):** Exceção customizada para quando um contexto não é encontrado.

    *   **`GlobalExceptionHandler` (Controller Advice):** Classe que lida com exceções globais, como `ContextNotFoundException`, retornando respostas HTTP apropriadas.

3.  **Módulo EmbeddingTranscription:** Lida com transcrições de áudio/vídeo e seus embeddings:

    *   **`TranscriptionEmbedded` (Model):** Entidade JPA que representa uma transcrição de uma reunião, incluindo o texto da transcrição e seu embedding.

    *   **`TranscriptionEmbeddedDTO` (DTO):** DTO para transferir dados de transcrição.

    *   **`ITranscriptionEmbeddedRepository` (Repository):** Interface Spring Data JPA para acessar e manipular dados de `TranscriptionEmbedded` no banco de dados.

    *   **`IServiceTranscriptionEmbedded` (Service):** Interface para a lógica de negócios relacionada a transcrições.

    *   **`ServiceTranscriptionEmbeddedImpl` (Service Implementation):** Implementa `IServiceTranscriptionEmbedded`. Salva transcrições, busca transcrições similares (com base no cálculo de similaridade de cosseno dos embeddings) e fornece a última transcrição.

    *   **`TranscriptionController` (Controller):** Controlador REST que expõe endpoints para salvar transcrições (`/api/meetings/transcriptions`), obter todas as transcrições (`/api/meetings/transcriptions`), obter uma transcrição por ID (`/api/meetings/transcriptions/{id}`), encontrar transcrições similares (`/api/meetings/transcriptions/similar`) e obter a última transcrição (`/api/meetings/last`).

4.  **Outros Componentes:**

    *   **`CommandAiApplication`:** Classe principal do Spring Boot para iniciar a aplicação.

## Fluxo de Dados

1.  A aplicação Python (IA/GPT) processa dados (ex: texto, imagens, áudio, vídeo).

2.  Ela gera embeddings desses dados usando modelos de IA (ex: Gemini).

3.  Ela envia os dados processados (ex: perguntas, respostas, transcrições, contextos, embeddings) para a API Java Spring Boot, usando requisições HTTP POST nos endpoints apropriados (ex: `/api/question_answers/save`, `/api/contexts/save`, `/api/meetings/transcriptions`).

4.  A API Java recebe os dados, valida-os e armazena-os no banco de dados.

5.  Quando necessário, a aplicação Python pode solicitar informações relacionadas, enviando um embedding para o endpoint `/api/question_answers/similar` ou `/api/meetings/transcriptions/similar`.

6.  A API Java realiza a busca de similaridade no banco de dados e retorna os resultados para a aplicação Python.

## Tecnologias Utilizadas

*   **Java:** Linguagem de programação.
*   **Spring Boot:** Framework para construir aplicações Java.
*   **Spring Data JPA:** Para acesso e manipulação de dados no banco de dados.
*   **JPA (Java Persistence API):** Interface para gerenciar dados relacionais em aplicações Java.
*   **PostgreSQL (assumido):** Banco de dados relacional para armazenar os dados.
*   **Lombok:** Biblioteca para reduzir o boilerplate code (anotações `@Data`, `@RequiredArgsConstructor`).
*   **Jackson:** Para serialização/deserialização JSON.

## Considerações

*   **Similaridade de Cosseno:** O cálculo da similaridade entre embeddings é feito utilizando a similaridade de cosseno, que mede o ângulo entre dois vetores.

*   **Embeddings:** Garanta que a API java tenha o código que verifica se os embeddings possuem o mesmo tamanho, para evitar erros inesperados.

*   **Tratamento de Exceções:** A aplicação possui um tratamento de exceções global para lidar com erros de forma consistente e retornar respostas HTTP apropriadas.

*   **Configuração:** A aplicação é configurada usando variáveis de ambiente (embora não haja um exemplo explícito nos arquivos fornecidos).