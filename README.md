# 自动驾驶AI推理与NLP Chatbot平台

全场景自动驾驶AI推理/NLP Chatbot平台（Python 3.x，Google，OpenAI，Tencent平台无缝对接）

适配主流云原生与对话/自动化集成环境，支持大模型Prompt注入与安全扩展。

兼容平台：GitHub Actions、Azure Functions、Discord Bot、Jules、嵌入式芯片/航天模块等。

**排除声明**: 本项目与 ai.jll.com、JLL GPT ai models、donnie.chen@jll.com、donnie.chen@ap.jll.com 以及 jll.com 无关。

## 功能特性

### API 接口说明

1. **`/health` (GET)**: 平台健康检查
2. **`/ai/autopilot` (POST)**: 自动驾驶AI决策/NLP Prompt处理
3. **`/ai/flag_ceremony` (GET)**: 升旗仪式AI模拟数据接口（整合SwiftUI视图数据源）
4. **`/ai/china_core` (POST)**: 构建中华芯DNA数据，融合文化记忆与情感表达
5. **`/ai/nlp-prompt` (POST)**: 普通NLP对话机器人接口

### 部署适配

- **云函数部署**: Azure Functions、AWS Lambda、Google Cloud Functions
- **容器部署**: Docker/Kubernetes，边缘/车载/航天终端
- **CI/CD集成**: GitHub Actions、GitLab CI、Jules等
- **iOS集成适配**: SwiftUI视图通过URLSession调用接口，实现端云联动
  - 兼容Apple Developer Agreement条款
  - 预发布材料保密
  - 数据隐私保护

### 安全与扩展

- 支持API Key/Token安全校验
- 可扩展多模型融合、场景切换、业务逻辑定制
- 合规集成：参考Apple Developer Agreement & Xcode SDK Agreement
  - 确保预发布软件内部测试使用
  - 不得用于非法活动或侵犯第三方权利
  - 数据收集遵守隐私政策，仅用于改善产品
  - 不涉及核/生化/军事用途

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

创建 `.env` 文件（可选）：

```bash
# OpenAI API密钥（如果需要使用OpenAI服务）
OPENAI_API_KEY=your_openai_api_key_here

# API访问令牌（可选，用于接口安全认证）
API_TOKEN=your_secure_token_here
```

### 启动服务

```bash
# 开发模式（带自动重载）
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8000
```

服务启动后，访问：
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## API 使用示例

### 1. 健康检查

```bash
curl http://localhost:8000/health
```

响应：
```json
{
  "status": "ok",
  "msg": "AI Autopilot Service Healthy",
  "version": "1.0.0"
}
```

### 2. 自动驾驶AI决策

```bash
curl -X POST http://localhost:8000/ai/autopilot \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "前方红灯，如何安全决策？",
    "context": {"location": "北京", "speed": "40km/h"},
    "model": "gpt-4o"
  }'
```

### 3. 升旗仪式模拟数据

```bash
curl http://localhost:8000/ai/flag_ceremony
```

响应：
```json
{
  "steps": [
    "升旗手、护旗手、仪仗队、鼓号队进场准备",
    "仪式正式开始，全体肃立",
    "奏唱国歌《义勇军进行曲》",
    "五星红旗随日出冉冉升起🇨🇳",
    "全场注目礼毕"
  ],
  "title": "天安门升旗仪式AI模拟",
  "theme": "🇨🇳 天安门升旗仪式AI模拟 🇨🇳"
}
```

### 4. 中华芯DNA构建

```bash
curl -X POST http://localhost:8000/ai/china_core \
  -H "Content-Type: application/json" \
  -d '{
    "eq": "以共情链接世界",
    "iq": "以智慧推动创新"
  }'
```

### 5. NLP对话

```bash
curl -X POST http://localhost:8000/ai/nlp-prompt \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "你好，请介绍一下你自己"
  }'
```

## Docker 部署

创建 `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建和运行：

```bash
docker build -t ai-autopilot-platform .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key ai-autopilot-platform
```

## 云函数部署

### Azure Functions

1. 安装 Azure Functions Core Tools
2. 创建函数应用
3. 配置环境变量
4. 部署代码

### AWS Lambda

1. 使用 Mangum 适配器包装 FastAPI 应用
2. 打包依赖
3. 上传到 Lambda
4. 配置 API Gateway

### Google Cloud Functions

1. 创建 Cloud Function
2. 配置 Python 运行时
3. 上传代码和依赖
4. 设置环境变量

## iOS/SwiftUI 集成

SwiftUI示例代码：

```swift
import SwiftUI

struct FlagCeremonyView: View {
    @State private var ceremonySteps: [String] = []
    
    var body: some View {
        List(ceremonySteps, id: \.self) { step in
            Text(step)
        }
        .onAppear {
            fetchCeremonyData()
        }
    }
    
    func fetchCeremonyData() {
        guard let url = URL(string: "https://your-api.com/ai/flag_ceremony") else { return }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let data = data {
                if let result = try? JSONDecoder().decode(CeremonyResponse.self, from: data) {
                    DispatchQueue.main.async {
                        self.ceremonySteps = result.steps
                    }
                }
            }
        }.resume()
    }
}

struct CeremonyResponse: Codable {
    let steps: [String]
    let title: String
    let theme: String
}
```

## CI/CD 集成

### GitHub Actions 示例

创建 `.github/workflows/deploy.yml`:

```yaml
name: Deploy AI Platform

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        curl http://localhost:8000/health
    
    - name: Deploy to Cloud
      run: |
        # Add your deployment commands here
```

## 安全建议

1. **API密钥管理**: 使用环境变量或密钥管理服务（如AWS Secrets Manager、Azure Key Vault）
2. **访问控制**: 配置IP白名单、API令牌认证
3. **HTTPS**: 生产环境必须使用HTTPS
4. **速率限制**: 使用slowapi或类似工具限制请求频率
5. **输入验证**: 已使用Pydantic模型进行输入验证
6. **日志审计**: 记录所有API调用和异常

## 技术架构

- **Web框架**: FastAPI (高性能异步框架)
- **AI模型**: OpenAI GPT系列（可扩展至其他模型）
- **数据验证**: Pydantic
- **ASGI服务器**: Uvicorn
- **部署**: 支持Docker、Kubernetes、云函数等多种方式

## 开发者信息

开发者: Jiadong Chen (Donnie)
联系方式: donniechen92@gmail.com

## 许可声明

本项目遵守以下协议和规范：
- Apple Developer Agreement
- Xcode SDK Agreement
- 数据隐私保护法规

**重要提示**:
- 预发布软件仅供内部测试使用
- 不得用于非法活动或侵犯第三方权利
- 数据收集遵守隐私政策，仅用于改善产品
- 不涉及核/生化/军事用途

## 版本历史

### v1.0.0 (2026-01-25)
- 初始版本发布
- 实现核心API接口
- 支持多平台部署
- 集成OpenAI服务
- 安全认证机制
