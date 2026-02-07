-- =============================================================================
-- Memory Schema / 記憶表結構 / 记忆表结构
-- Document-AI Open Source Blueprint
-- =============================================================================

-- Conversation Memory Table / 對話記憶表 / 对话记忆表
-- Stores conversation history for LLM context management
-- 儲存 LLM 上下文管理的對話歷史
-- 储存 LLM 上下文管理的对话历史
CREATE TABLE IF NOT EXISTS conversation_memory (
    id              BIGSERIAL PRIMARY KEY,
    session_id      UUID NOT NULL,                          -- Session identifier / 會話識別碼 / 会话识别码
    role            VARCHAR(20) NOT NULL,                   -- 'user' | 'assistant' | 'system'
    content         TEXT NOT NULL,                          -- Message content / 訊息內容 / 消息内容
    token_count     INTEGER DEFAULT 0,                      -- Token count / 令牌數 / 令牌数
    embedding       VECTOR(1536),                           -- OpenAI ada-002 embedding / 嵌入向量
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata        JSONB DEFAULT '{}'::jsonb               -- Extra metadata / 額外元資料 / 额外元数据
);

CREATE INDEX idx_conv_session ON conversation_memory(session_id);
CREATE INDEX idx_conv_created ON conversation_memory(created_at);

-- Summary Memory Table / 摘要記憶表 / 摘要记忆表
-- Stores condensed summaries of conversation segments
-- 儲存對話片段的濃縮摘要
-- 储存对话片段的浓缩摘要
CREATE TABLE IF NOT EXISTS summary_memory (
    id              BIGSERIAL PRIMARY KEY,
    session_id      UUID NOT NULL,
    summary_text    TEXT NOT NULL,                          -- Summary content / 摘要內容 / 摘要内容
    source_msg_ids  BIGINT[] DEFAULT '{}',                  -- Source message IDs / 來源訊息ID / 来源消息ID
    summary_type    VARCHAR(30) DEFAULT 'progressive',      -- 'progressive' | 'map_reduce' | 'refine'
    embedding       VECTOR(1536),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Entity Memory Table / 實體記憶表 / 实体记忆表
-- Stores extracted entities and their relationships
-- 儲存提取的實體及其關係
-- 储存提取的实体及其关系
CREATE TABLE IF NOT EXISTS entity_memory (
    id              BIGSERIAL PRIMARY KEY,
    session_id      UUID NOT NULL,
    entity_name     VARCHAR(255) NOT NULL,                  -- Entity name / 實體名稱 / 实体名称
    entity_type     VARCHAR(50) NOT NULL,                   -- PERSON | ORG | LOCATION | CONCEPT | PRODUCT
    description     TEXT,                                    -- Entity description / 實體描述 / 实体描述
    attributes      JSONB DEFAULT '{}'::jsonb,              -- Dynamic attributes / 動態屬性 / 动态属性
    first_seen      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_updated    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    mention_count   INTEGER DEFAULT 1                       -- Mention frequency / 提及頻率 / 提及频率
);

CREATE INDEX idx_entity_name ON entity_memory(entity_name);
CREATE INDEX idx_entity_type ON entity_memory(entity_type);

-- Knowledge Graph Triples / 知識圖譜三元組 / 知识图谱三元组
-- Stores subject-predicate-object triples for graph reasoning
-- 儲存主語-謂語-賓語三元組用於圖推理
-- 储存主语-谓语-宾语三元组用于图推理
CREATE TABLE IF NOT EXISTS kg_triples (
    id              BIGSERIAL PRIMARY KEY,
    subject_id      BIGINT REFERENCES entity_memory(id),    -- Subject entity / 主語實體 / 主语实体
    predicate       VARCHAR(255) NOT NULL,                  -- Relationship / 關係 / 关系
    object_id       BIGINT REFERENCES entity_memory(id),    -- Object entity / 賓語實體 / 宾语实体
    confidence      FLOAT DEFAULT 1.0,                      -- Confidence score / 信心分數 / 置信度分数
    source          VARCHAR(100),                           -- Extraction source / 提取來源 / 提取来源
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Document Export Log / 文件匯出記錄 / 文档导出记录
-- Tracks all document generations (Excel, PPTX, PDF, DOCX)
-- 追蹤所有文件生成（Excel、PPTX、PDF、DOCX）
-- 追踪所有文档生成（Excel、PPTX、PDF、DOCX）
CREATE TABLE IF NOT EXISTS document_export_log (
    id              BIGSERIAL PRIMARY KEY,
    session_id      UUID,
    doc_type        VARCHAR(10) NOT NULL,                   -- 'xlsx' | 'pptx' | 'pdf' | 'docx'
    file_path       TEXT NOT NULL,                          -- Output file path / 輸出檔案路徑 / 输出文件路径
    template_used   VARCHAR(255),                           -- Template name / 模板名稱 / 模板名称
    row_count       INTEGER,                                -- Rows exported / 匯出列數 / 导出行数
    llm_provider    VARCHAR(50),                            -- Which LLM generated content / 哪個LLM生成內容
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata        JSONB DEFAULT '{}'::jsonb
);

-- Embedding Store / 嵌入向量儲存 / 嵌入向量存储
-- Central embedding cache for all document chunks
-- 所有文件區塊的中央嵌入快取
-- 所有文档块的中央嵌入缓存
CREATE TABLE IF NOT EXISTS embedding_store (
    id              BIGSERIAL PRIMARY KEY,
    source_type     VARCHAR(30) NOT NULL,                   -- 'conversation' | 'document' | 'entity' | 'summary'
    source_id       BIGINT NOT NULL,                        -- FK to source table / 來源表外鍵 / 来源表外键
    chunk_text      TEXT NOT NULL,                          -- Text chunk / 文本區塊 / 文本块
    embedding       VECTOR(1536),                           -- Embedding vector / 嵌入向量
    model_name      VARCHAR(100) DEFAULT 'text-embedding-ada-002',
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_embed_source ON embedding_store(source_type, source_id);

-- LLM API Usage Log / LLM API 使用記錄 / LLM API 使用记录
-- Tracks API calls across all providers
-- 追蹤所有提供者的 API 呼叫
-- 追踪所有提供者的 API 调用
CREATE TABLE IF NOT EXISTS llm_api_usage (
    id              BIGSERIAL PRIMARY KEY,
    provider        VARCHAR(50) NOT NULL,                   -- 'openai' | 'anthropic' | 'google' | etc.
    model           VARCHAR(100) NOT NULL,                  -- Model name / 模型名稱 / 模型名称
    operation       VARCHAR(50) NOT NULL,                   -- 'chat' | 'embedding' | 'image' | 'audio'
    input_tokens    INTEGER DEFAULT 0,                      -- Input tokens / 輸入令牌 / 输入令牌
    output_tokens   INTEGER DEFAULT 0,                      -- Output tokens / 輸出令牌 / 输出令牌
    latency_ms      INTEGER,                                -- Response time / 回應時間 / 响应时间
    cost_usd        DECIMAL(10, 6),                         -- Estimated cost / 估計成本 / 估计成本
    status          VARCHAR(20) DEFAULT 'success',          -- 'success' | 'error' | 'timeout'
    error_message   TEXT,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_usage_provider ON llm_api_usage(provider, created_at);
