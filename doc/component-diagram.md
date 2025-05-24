# Component Diagram

## System Architecture Overview

This diagram shows the components involved in the RAG chatbot solution and their interactions from the time a question is received until a response is generated.

```mermaid
graph TD
    %% User Interface Layer
    A[👤 User Input] --> B[🎯 Main Interface]
    B --> C{Menu Selection}

    %% Query Processing
    C -->|1,2,3| D[📋 Predefined Questions]
    C -->|4| E[❓ Additional Questions Menu]
    C -->|5| F[✍️ Custom Question Input]
    C -->|6| G[👋 Exit Application]

    D --> H[🔍 Query Processing]
    E --> H
    F --> H

    %% Data Sources
    I[🌐 promtior.ai] --> J[🕷️ Web Scraper]
    K[📄 AI Engineer.pdf] --> L[📑 PDF Processor]

    %% Content Processing Pipeline
    J --> M[🧹 Content Cleaning]
    L --> M
    M --> N[📚 Document Creation]
    N --> O[✂️ Text Splitter]
    O --> P[🧠 Embedding Model]
    P --> Q[💾 Vector Store - Chroma]

    %% RAG Pipeline
    H --> R[🔎 Vector Similarity Search]
    R --> Q
    Q --> S[📋 Context Retrieval]
    S --> T[🤖 LLM Processing]
    T --> U[💬 Response Generation]
    U --> V[📱 User Interface Display]

    %% Caching System
    Q --> W[⚡ Cache Manager]
    W --> X{Cache Valid?}
    X -->|Yes| Y[📊 Load Cached Store]
    X -->|No| Z[🔄 Rebuild Vector Store]
    Y --> Q
    Z --> Q

    %% Styling
    subgraph "Data Ingestion Layer"
        I
        K
        J
        L
    end

    subgraph "Processing Layer"
        M
        N
        O
        P
    end

    subgraph "Storage Layer"
        Q
        W
        X
        Y
        Z
    end

    subgraph "RAG Pipeline"
        R
        S
        T
        U
    end

    subgraph "User Interface Layer"
        A
        B
        C
        D
        E
        F
        G
        V
    end
```
