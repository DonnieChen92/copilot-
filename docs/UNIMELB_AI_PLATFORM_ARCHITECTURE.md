# UniMelb Exclusive AI Platform — Master Architecture & Migration Plan

> **Pilot Concept Author**: Jiadong Chen — UniMelb Graduate, Student ID: 723912
> **Date**: 12 February 2026, Melbourne, Australia
> **Classification**: Security-First | Anti-Hallucination | Zero-Assumption Design
> **Version**: 1.0.0-alpha

---

## Executive Summary

This document defines the architecture for **UniMelb AI** — a university-exclusive artificial
intelligence platform built on Microsoft Azure AI Foundry, Frontier Models, and Copilot. The
platform unifies Campus Management, Academic Faculty operations, Professional Staff workflows,
and Property Management into a single, government-regulated, security-first ecosystem.

The design is rooted in a **life-challenge programme** philosophy: acknowledging that real
hardship — financial difficulty, study pauses, restarts over 6+ months — must never be a
barrier to completing a degree or accessing knowledge. The platform therefore prioritises
**anti-hallucination** (zero-assumption, zero-faking-answer-rate) and **manual verification
against legislation and e-library sources** to ensure every AI-generated response can be
trusted by students, staff, and regulators.

---

## Table of Contents

1. [Vision & Principles](#1-vision--principles)
2. [Platform Architecture Overview](#2-platform-architecture-overview)
3. [Canvas-to-Teams Migration Plan (3 Plans)](#3-canvas-to-teams-migration-plan)
4. [Property Management Integration (MRI Property Tree)](#4-property-management-integration)
5. [Financial Forecast (3 Tiers)](#5-financial-forecast)
6. [Anti-Hallucination & Verification Framework](#6-anti-hallucination--verification-framework)
7. [Education Platform Integration](#7-education-platform-integration)
8. [Government Regulatory Compliance (AU/NZ/APAC)](#8-government-regulatory-compliance)
9. [Academic Faculty Research Support](#9-academic-faculty-research-support)
10. [Life Challenge Programme](#10-life-challenge-programme)
11. [Deployment Lifecycle (Alpha → Beta → Production)](#11-deployment-lifecycle)
12. [Roadmap & Milestones](#12-roadmap--milestones)

---

## 1. Vision & Principles

### 1.1 Core Vision

Build a **single unified AI platform** for the University of Melbourne that:

- Replaces fragmented Canvas/Spark AI/Aila tools with an integrated Microsoft Teams experience
- Connects academic research, campus operations, and property management under one roof
- Meets Australian government regulatory standards and can extend to NZ, Fiji, and APAC
- Provides **provably accurate** AI assistance through anti-hallucination verification
- Supports every user type: students, academic staff, professional staff, external suppliers,
  retail/commercial tenants, property agents, and government auditors

### 1.2 Design Principles

| # | Principle | Description |
|---|-----------|-------------|
| 1 | **Security First** | Zero-Trust architecture; every request authenticated and authorised via Azure AD/Entra ID |
| 2 | **Anti-Hallucination** | Every AI response tagged with confidence score, source citations, and verification status |
| 3 | **Zero Assumption** | No answer given without evidence trail; "I don't know" is a valid and preferred response |
| 4 | **Government Auditable** | Full Azure Monitor logging; immutable audit trail for regulatory review |
| 5 | **Life-Challenge Inclusive** | Financial pause/restart support; accessibility-first; no student left behind |
| 6 | **Single Identity** | One Microsoft Entra ID account = access to all platform services |
| 7 | **APAC Extensible** | Architecture supports multi-tenancy for NZ, Fiji, and broader APAC deployment |

---

## 2. Platform Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        UniMelb AI Platform (Top Level)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  MS Teams     │  │  Web Portal  │  │  iOS Apps    │  │  Desktop     │   │
│  │  (Primary)    │  │  (Azure)     │  │  (UniMelb +  │  │  (Win/Mac)   │   │
│  │              │  │              │  │   MyMBS)     │  │              │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
│         │                 │                 │                 │             │
│  ┌──────┴─────────────────┴─────────────────┴─────────────────┴──────┐     │
│  │                    API Gateway (Azure API Management)              │     │
│  │              + Azure Front Door (WAF / DDoS Protection)           │     │
│  └──────┬─────────────────┬─────────────────┬────────────────────────┘     │
│         │                 │                 │                               │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐                     │
│  │ Identity &   │  │ AI Engine    │  │ Integration  │                     │
│  │ Access       │  │ Layer        │  │ Hub          │                     │
│  │              │  │              │  │              │                     │
│  │ • Entra ID   │  │ • Azure AI   │  │ • Canvas LMS │                     │
│  │ • RBAC       │  │   Foundry    │  │ • Spark AI   │                     │
│  │ • MFA        │  │ • Copilot    │  │ • MRI Property│                    │
│  │ • Zero Trust │  │ • Frontier   │  │ • MS 365     │                     │
│  │ • Cond.Access│  │   Models     │  │ • Google Edu │                     │
│  └──────────────┘  │ • Anti-Halluc│  │ • OpenAI Edu │                     │
│                    │   Framework  │  │ • Apple Push │                     │
│                    └──────────────┘  └──────────────┘                     │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │                    Data & Compliance Layer                        │      │
│  │                                                                  │      │
│  │  • Azure Monitor (Full Logging)    • Azure SQL / Cosmos DB      │      │
│  │  • Azure Policy (Gov Compliance)   • Azure Blob (Documents)     │      │
│  │  • Defender for Cloud              • Azure Key Vault             │      │
│  │  • Immutable Audit Trail           • Backup & DR (geo-redundant)│      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 User Roles & Access Matrix

| Role | Teams | Web | iOS App | Property Mgmt | AI Chat | Admin |
|------|-------|-----|---------|---------------|---------|-------|
| Student | Full | Full | UniMelb App (904152776) | — | Full | — |
| Academic Staff | Full | Full | Both Apps | — | Full + Research | Faculty Admin |
| Professional Staff | Full | Full | Both Apps | Read | Full | Dept Admin |
| External Supplier | Limited | Portal | — | Assigned | Scoped | — |
| Retail Tenant | Limited | Portal | — | Tenant View | Scoped | — |
| Commercial Tenant | Limited | Portal | — | Tenant View | Scoped | — |
| Sub-tenant | Limited | Portal | — | Sub-view | Scoped | — |
| Property Agent (Lendlease/JLL/MICM) | Full | Portal | — | Agent View | Full | Property Admin |
| Government Auditor | Read-only | Audit Portal | — | Audit View | Logs Only | Audit |

### 2.2 iOS Mobile App Integration

| App | Apple ID | Purpose | Integration Method |
|-----|----------|---------|-------------------|
| **UniMelb Official** | `904152776` | Student portal, timetables, campus maps, notifications | APNS + REST API + SSO via Entra ID |
| **MyMBS App** | `1095799806` | Melbourne Business School: events, networking, MBS-specific content | APNS + REST API + SSO via Entra ID |

Both apps authenticate through **Microsoft Entra ID** (formerly Azure AD) using SAML 2.0/OIDC,
providing single sign-on across the entire platform.

---

## 3. Canvas-to-Teams Migration Plan

### Overview: Three Migration Plans

The migration from Canvas LMS to Microsoft Teams (with integrated AI) follows three
concurrent plans targeting different stakeholder groups. Each plan has defined stages.

### Plan A — Internal University (Staff + Academic Faculty)

**Scope**: All UniMelb academic and professional staff migrating from Canvas to Teams

| Stage | Name | Duration | Activities |
|-------|------|----------|------------|
| A1 | **Discovery & Audit** | Weeks 1–4 | Inventory all Canvas courses, content, integrations; map to Teams equivalents; identify Spark AI / Aila dependencies |
| A2 | **Pilot Cohort** | Weeks 5–12 | 50 staff across 3 faculties (Law, Engineering, IT) run dual Canvas+Teams; collect feedback |
| A3 | **Content Migration** | Weeks 13–20 | Automated migration of Canvas modules → Teams channels; grade books → Teams Assignments; Turnitin → Teams integration |
| A4 | **Training & Certification** | Weeks 21–26 | Staff complete Microsoft Educator certification; AI literacy programme; anti-hallucination awareness training |
| A5 | **Full Cutover** | Weeks 27–30 | Canvas set to read-only; Teams becomes primary; 24/7 support desk active |
| A6 | **Post-Migration Review** | Weeks 31–36 | KPI measurement; user satisfaction survey; remediation of issues |

### Plan B — External Suppliers, Retail & Commercial Tenants

**Scope**: Lendlease, JLL, MICM, retail tenants, commercial tenants, sub-tenants

| Stage | Name | Duration | Activities |
|-------|------|----------|------------|
| B1 | **Stakeholder Mapping** | Weeks 1–4 | Identify all external parties; classify as Supplier / Tenant / Sub-tenant / Agent; define data boundaries |
| B2 | **Portal Development** | Weeks 5–16 | Build Azure-hosted external portal with Teams Guest Access; integrate MRI Property Tree; role-based dashboards |
| B3 | **Agent Onboarding** | Weeks 17–22 | Lendlease, JLL, MICM onboarded to property management module; training on MRI integration; API key provisioning |
| B4 | **Tenant Migration** | Weeks 23–30 | Retail and commercial tenants migrated from legacy systems to Teams-integrated portal; lease data synced from MRI |
| B5 | **Sub-tenant Rollout** | Weeks 31–34 | Sub-tenants given scoped portal access; automated billing and maintenance request integration |
| B6 | **Go-Live & Support** | Weeks 35–40 | Full external ecosystem live; SLA monitoring; quarterly review cadence established |

### Plan C — Service Providers & Government Integration

**Scope**: Government regulators, auditors, APAC partners (NZ, Fiji, future)

| Stage | Name | Duration | Activities |
|-------|------|----------|------------|
| C1 | **Regulatory Framework** | Weeks 1–8 | Map TEQSA, ESOS Act, Privacy Act 1988, GDPR (for international), NZ Education Act requirements to platform controls |
| C2 | **Audit Infrastructure** | Weeks 9–16 | Deploy Azure Monitor + Log Analytics + Sentinel; create immutable audit dashboards; government auditor read-only access |
| C3 | **Compliance Certification** | Weeks 17–24 | Achieve ISO 27001, SOC 2 Type II, IRAP (Australian govt); prepare for APAC extension |
| C4 | **NZ Pilot Extension** | Weeks 25–32 | Deploy multi-tenant instance for NZ university partner; Fiji scoping study begins |
| C5 | **APAC Framework** | Weeks 33–40 | Publish APAC higher education AI governance framework; invite regional partners |

### Migration Data Flow

```
Canvas LMS                         Microsoft Teams + UniMelb AI
─────────                         ─────────────────────────────
Courses          ──────────►      Teams (one Team per course)
Modules          ──────────►      Channels + Tabs
Assignments      ──────────►      Teams Assignments + Rubrics
Grades           ──────────►      Teams Gradebook + Azure SQL
Discussion Boards──────────►      Teams Posts + Channels
Quizzes          ──────────►      MS Forms + AI-assisted grading
SpeedGrader      ──────────►      Teams Feedback + Copilot review
Canvas Inbox     ──────────►      Teams Chat + Outlook
Turnitin         ──────────►      Turnitin Teams Integration
Spark AI / Aila  ──────────►      UniMelb AI Copilot (Azure Foundry)
Calendar         ──────────►      Outlook + Teams Calendar
Files            ──────────►      SharePoint + OneDrive
Analytics        ──────────►      Power BI + Azure Monitor
```

---

## 4. Property Management Integration

### 4.1 MRI Property Tree — Full System Model

The platform integrates with **MRI Software's Property Tree** as the reference property
management system, covering both Residential and Commercial property for UniMelb's campus
estate.

```
┌──────────────────────────────────────────────────────────────────┐
│                   MRI Property Tree Integration                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────┐    ┌─────────────────────┐             │
│  │   RESIDENTIAL        │    │   COMMERCIAL          │             │
│  │                     │    │                       │             │
│  │  • Student Housing  │    │  • Retail Tenancies   │             │
│  │  • Staff Residences │    │  • Office Leases      │             │
│  │  • Visitor Accomm.  │    │  • Lab/Research Space │             │
│  │  • Maintenance Mgmt │    │  • Event Venues       │             │
│  │  • Bond Management  │    │  • Food & Beverage    │             │
│  │  • Rent Collection  │    │  • Sub-tenant Mgmt    │             │
│  └──────────┬──────────┘    └──────────┬────────────┘             │
│             │                          │                          │
│  ┌──────────┴──────────────────────────┴────────────┐            │
│  │              MRI API Gateway (REST + GraphQL)      │            │
│  └──────────────────────┬───────────────────────────┘            │
│                         │                                        │
│  ┌──────────────────────┴───────────────────────────┐            │
│  │           UniMelb AI Integration Layer            │            │
│  │                                                   │            │
│  │  • Sync Engine (bidirectional)                    │            │
│  │  • Azure Service Bus (event-driven)               │            │
│  │  • Property AI Assistant (Copilot)                │            │
│  │  • Maintenance Prediction (ML)                    │            │
│  │  • Lease Analytics (Power BI)                     │            │
│  └───────────────────────────────────────────────────┘            │
│                                                                  │
│  Agent Access (via Teams + Portal):                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                        │
│  │ Lendlease│ │   JLL    │ │   MICM   │                        │
│  │ (Facility│ │ (Valuatn,│ │ (Residen- │                        │
│  │  Mgmt)   │ │  Leasing)│ │  tial)   │                        │
│  └──────────┘ └──────────┘ └──────────┘                        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 Deployment Environments

| Environment | Purpose | Data | Access |
|-------------|---------|------|--------|
| **Alpha (Dev)** | Development & unit testing | Synthetic/mock data | Developers only |
| **Beta (Staging)** | Integration testing & UAT | Anonymised production clone | Dev + QA + select users |
| **Test** | Daily automated regression | Synthetic + edge cases | CI/CD pipeline |
| **Training** | Staff and agent training | Curated training dataset | All onboarding users |
| **Daily Use** | Standard operations | Live production data | All authorised users |
| **Live / Production** | Real-time operations | Live data (primary) | All users per RBAC |
| **Backup** | Disaster recovery | Geo-redundant replica | DR team + automated failover |

### 4.3 Technology Evolution Path

```
Alpha (Python/TypeScript)  →  Beta (C#/.NET + Azure)  →  Production (C/C++ optimised core)
        ↓                           ↓                            ↓
   Rapid prototyping          Enterprise hardening         Performance-critical paths
   FastAPI + React            ASP.NET Core + Blazor        Native Azure SDKs
   SQLite + mock MRI          Azure SQL + MRI staging      Azure SQL HA + MRI Production
   Local Docker               AKS (Kubernetes)             AKS multi-region + CDN
```

---

## 5. Financial Forecast

### 5.1 Three-Tier Financial Model

#### Tier 1 — Conservative (Minimum Viable Platform)

| Category | Year 1 (AUD) | Year 2 (AUD) | Year 3 (AUD) |
|----------|-------------|-------------|-------------|
| Azure Infrastructure | $180,000 | $210,000 | $240,000 |
| Microsoft 365 E5 Education (est. 12,000 users) | $360,000 | $360,000 | $360,000 |
| Azure AI Foundry (Frontier models) | $120,000 | $150,000 | $180,000 |
| Copilot for Microsoft 365 (staff subset) | $180,000 | $240,000 | $300,000 |
| MRI Property Tree Licences | $85,000 | $85,000 | $85,000 |
| Canvas wind-down (parallel running) | $200,000 | $100,000 | $0 |
| Staff (2 FTE platform engineers) | $300,000 | $310,000 | $320,000 |
| Training & Change Management | $80,000 | $40,000 | $30,000 |
| Security & Compliance (IRAP, ISO 27001) | $60,000 | $30,000 | $30,000 |
| Contingency (10%) | $156,500 | $152,500 | $154,500 |
| **Total** | **$1,721,500** | **$1,677,500** | **$1,699,500** |

#### Tier 2 — Standard (Full Platform with APAC Readiness)

| Category | Year 1 (AUD) | Year 2 (AUD) | Year 3 (AUD) |
|----------|-------------|-------------|-------------|
| Azure Infrastructure (multi-region) | $320,000 | $380,000 | $420,000 |
| Microsoft 365 E5 Education (20,000 users) | $600,000 | $600,000 | $600,000 |
| Azure AI Foundry (Frontier + fine-tuned) | $250,000 | $300,000 | $350,000 |
| Copilot for Microsoft 365 (all staff) | $360,000 | $360,000 | $360,000 |
| OpenAI Education Tier | $48,000 | $60,000 | $72,000 |
| Google Workspace Education Plus | $96,000 | $96,000 | $96,000 |
| MRI Property Tree (full suite) | $150,000 | $150,000 | $150,000 |
| Canvas wind-down | $200,000 | $100,000 | $0 |
| Staff (5 FTE: 2 eng, 1 data, 1 security, 1 PM) | $750,000 | $775,000 | $800,000 |
| External agents integration (Lendlease/JLL/MICM) | $120,000 | $60,000 | $40,000 |
| Training & Change Management | $150,000 | $80,000 | $60,000 |
| Security, Compliance, Gov Audit | $120,000 | $80,000 | $60,000 |
| NZ/Fiji Pilot Preparation | $0 | $80,000 | $160,000 |
| Contingency (15%) | $469,500 | $468,150 | $475,200 |
| **Total** | **$3,633,500** | **$3,589,150** | **$3,643,200** |

#### Tier 3 — Premium (Full APAC Research Platform)

| Category | Year 1 (AUD) | Year 2 (AUD) | Year 3 (AUD) |
|----------|-------------|-------------|-------------|
| Azure Infrastructure (APAC multi-region) | $500,000 | $600,000 | $720,000 |
| Microsoft 365 E5 (50,000+ users inc. partners) | $1,500,000 | $1,500,000 | $1,500,000 |
| Azure AI Foundry (full frontier catalogue) | $480,000 | $600,000 | $720,000 |
| Copilot for Microsoft 365 (universal) | $600,000 | $600,000 | $600,000 |
| OpenAI Enterprise + Research | $120,000 | $150,000 | $180,000 |
| Google Workspace Education Plus (full) | $180,000 | $180,000 | $180,000 |
| MRI Property Tree (enterprise, multi-campus) | $250,000 | $250,000 | $250,000 |
| Canvas wind-down + data archival | $250,000 | $125,000 | $50,000 |
| Staff (12 FTE full team) | $1,800,000 | $1,860,000 | $1,920,000 |
| External ecosystem (agents + tenants) | $200,000 | $120,000 | $80,000 |
| Training, Change Mgmt, Life Challenge Programme | $300,000 | $200,000 | $150,000 |
| Security, Compliance, IRAP, ISO, SOC 2 | $200,000 | $150,000 | $120,000 |
| APAC Expansion (NZ + Fiji + partners) | $100,000 | $300,000 | $500,000 |
| Research AI Compute (GPU clusters) | $400,000 | $500,000 | $600,000 |
| Anti-Hallucination R&D | $150,000 | $180,000 | $200,000 |
| Contingency (15%) | $1,054,500 | $1,072,500 | $1,105,500 |
| **Total** | **$8,084,500** | **$8,387,500** | **$8,875,500** |

### 5.2 Life Challenge Programme — Financial Pause/Restart Model

```
Student Financial Journey (Jiadong Chen Model):
──────────────────────────────────────────────────
   ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
   │  ACTIVE   │─────►│  PAUSE   │─────►│ RESTART  │─────►│ COMPLETE │
   │  Study    │      │  (≤6mo)  │      │  Study   │      │  Graduate│
   │           │      │          │      │          │      │          │
   │ Full AI   │      │ Limited  │      │ Full AI  │      │ Alumni   │
   │ access    │      │ read-only│      │ access + │      │ lifetime │
   │           │      │ AI access│      │ catch-up │      │ access   │
   └──────────┘      └──────────┘      └──────────┘      └──────────┘
        │                  │                  │                  │
   100% platform       Core tools         100% + AI         Research
   access              preserved          tutoring           portal
```

The platform **never fully disconnects** a student during financial hardship. During a
pause period (up to 6 months, extendable to 12 February 2026 and beyond):

- AI chat remains available in read-only/limited mode
- Course materials remain accessible
- No data is deleted; progress is preserved
- Financial support pathways are surfaced automatically
- Re-enrolment triggers full access restoration with AI-powered catch-up summaries

---

## 6. Anti-Hallucination & Verification Framework

### 6.1 Zero-Assumption Design

```
User Query
    │
    ▼
┌────────────────────────────────┐
│  Stage 1: Multi-Model Query    │  Query sent to 3+ AI models simultaneously
│  (Azure Foundry Frontier)      │  (GPT-4o, Claude Opus, Gemini Pro)
└──────────────┬─────────────────┘
               │
               ▼
┌────────────────────────────────┐
│  Stage 2: Cross-Verification   │  Compare responses; identify consensus
│  (Consensus Engine)            │  and divergence points
└──────────────┬─────────────────┘
               │
               ▼
┌────────────────────────────────┐
│  Stage 3: Source Citation       │  Every claim must cite:
│  (Evidence Extraction)         │  - Academic paper (DOI)
│                                │  - Legislation (section/clause)
│                                │  - UniMelb e-library resource
│                                │  - Official documentation URL
└──────────────┬─────────────────┘
               │
               ▼
┌────────────────────────────────┐
│  Stage 4: Confidence Scoring   │  Score: 0.0 → 1.0
│  (Anti-Hallucination Engine)   │  < 0.6 = "Unverified — manual check required"
│                                │  0.6–0.8 = "Partially verified"
│                                │  > 0.8 = "High confidence — sources attached"
└──────────────┬─────────────────┘
               │
               ▼
┌────────────────────────────────┐
│  Stage 5: Manual Verification  │  For legal/regulatory queries:
│  Queue (Human-in-the-Loop)     │  - Auto-check against AustLII (legislation)
│                                │  - Cross-ref UniMelb e-library
│                                │  - Flag for human expert review if < 0.6
└──────────────┬─────────────────┘
               │
               ▼
┌────────────────────────────────┐
│  Stage 6: Azure Monitor Log    │  Every query/response pair logged:
│  (Immutable Audit Trail)       │  - Timestamp, user, models used
│                                │  - Confidence score, sources cited
│                                │  - Verification status
│                                │  - Latency, token usage, cost
└────────────────────────────────┘
```

### 6.2 AI Chatbot Integration (Single Account)

All leading AI chatbots accessible through one `@unimelb.edu.au` account:

| Provider | Tier | Purpose | Integration |
|----------|------|---------|-------------|
| Microsoft Copilot | Education | Primary assistant | Native Teams integration |
| Azure OpenAI (GPT-4o, o3) | Enterprise | Research + complex reasoning | Azure AI Foundry |
| Anthropic Claude (Opus, Sonnet) | Enterprise | Extended thinking, safety | Azure AI Foundry |
| Google Gemini | Education | Multimodal, fast queries | Google Workspace EDU |
| OpenAI ChatGPT | Education / Teams / Enterprise | General + research | API via Azure |
| DeepSeek | Research | Cost-effective reasoning | Azure AI Foundry |
| Perplexity | Enterprise | Web-grounded search | API integration |

---

## 7. Education Platform Integration

### 7.1 Microsoft Education Stack

| Product | Licence Tier | Users | Purpose |
|---------|-------------|-------|---------|
| Microsoft 365 Education A5 | Institution | All staff + students | Full productivity suite |
| Microsoft Teams for Education | Included in A5 | All | Collaboration + classes |
| Copilot for Microsoft 365 | Add-on | Staff (phased to students) | AI assistant |
| Azure AI Foundry | Enterprise | Platform | AI model hosting |
| Power BI Pro | Included in A5 | Staff | Analytics + reporting |
| Intune for Education | Included in A5 | Devices | Device management |
| Defender for Endpoint | Included in A5 | All | Security |

### 7.2 Google Education Stack

| Product | Tier | Users | Purpose |
|---------|------|-------|---------|
| Google Workspace for Education Plus | Institution | All | Gmail, Drive, Docs, Meet |
| Google Classroom | Included | Academic | Course management (legacy support) |
| Gemini for Education | Add-on | Staff + students | AI assistant |
| Google Cloud (GCP) | Research | Faculty | Research compute |

### 7.3 OpenAI Education Tiers

| Tier | Users | Features |
|------|-------|----------|
| **Free** | All students (default) | Basic ChatGPT access, limited queries |
| **Student** | Verified students | Enhanced limits, GPT-4o access |
| **Business** | Professional staff | Team workspaces, admin controls |
| **Team** | Department-level | Shared workspaces, custom GPTs |
| **Enterprise** | Institution-wide | SSO, data residency, audit logs |
| **Research** | Faculty + PhD candidates | API access, fine-tuning, extended limits |
| **Labs** | Selected research groups | Experimental models, early access |

---

## 8. Government Regulatory Compliance

### 8.1 Australian Regulatory Framework

| Regulation | Requirement | Platform Control |
|------------|-------------|-----------------|
| **Privacy Act 1988** (Cth) | APPs for personal data handling | Azure data residency (Australia East); encryption at rest + transit |
| **TEQSA** (Higher Education Standards) | Quality assurance for education delivery | AI accuracy monitoring; anti-hallucination framework |
| **ESOS Act 2000** | Protection for international students | Multilingual AI support; PRISMS integration capability |
| **AI Ethics Framework** (Dept of Industry) | Responsible AI principles | Transparency, fairness, accountability logging |
| **Security of Critical Infrastructure Act** | If classified as critical | Azure Sentinel + Defender; IRAP assessment |
| **Spam Act 2003** | Electronic communications | Consent-based notifications only |
| **Consumer Data Right** (CDR) | If financial data involved | Scoped to property management billing |

### 8.2 APAC Extension Compliance

| Jurisdiction | Key Regulations | Status |
|-------------|----------------|--------|
| **New Zealand** | Privacy Act 2020, Education and Training Act 2020 | Year 2 pilot |
| **Fiji** | Online Safety Act 2018, Higher Education Act 2008 | Year 2 scoping |
| **Singapore** | PDPA, AI Governance Framework | Year 3 consideration |
| **APAC Framework** | APEC CBPR, Cross-Border Privacy Rules | Year 3 implementation |

### 8.3 Monitoring & Audit Architecture

```
Azure Monitor                    Azure Sentinel (SIEM)
    │                                  │
    ├── Application Insights ──────────┤
    ├── Log Analytics Workspace ───────┤
    ├── Diagnostic Logs ───────────────┤
    ├── AI Model Inference Logs ───────┤
    ├── Property Mgmt Audit Logs ──────┤
    └── Compliance Dashboard ──────────┘
              │
              ▼
    Government Auditor Portal
    (Read-only, immutable, exportable)
```

---

## 9. Academic Faculty Research Support

### 9.1 Supported Faculties (Priority)

| Faculty | AI Use Cases | Special Requirements |
|---------|-------------|---------------------|
| **Melbourne Law School** | Legal research, case analysis, legislation lookup, moot court prep | AustLII integration; anti-hallucination critical; citation accuracy |
| **Engineering** | Simulation, CAD assistance, research paper analysis, lab data processing | GPU compute; MATLAB/Python integration; large dataset support |
| **Computing & IT (FEIT)** | Code generation, security research, ML/DL training, thesis support | GitHub Copilot; Azure DevOps; custom model fine-tuning |
| **Melbourne Business School** | Market analysis, financial modelling, case study generation | MyMBS App integration; Bloomberg data; Excel Copilot |
| **Arts & Humanities** | Translation, archival research, digital humanities, social analysis | Multilingual models; cultural sensitivity; bias detection |
| **Medicine** | Clinical research, literature review, drug interaction analysis | HIPAA-equivalent controls; de-identification; PubMed integration |

### 9.2 Human & Social Harmony Research

The platform explicitly supports research into:

- Social cohesion and community building
- Mental health and wellbeing in higher education
- Cultural diversity and inclusion
- Life hardship and resilience studies
- Financial stress and student support systems
- Cross-cultural communication and understanding

These areas receive priority AI resource allocation and enhanced anti-hallucination
safeguards given the sensitive nature of the research.

---

## 10. Life Challenge Programme

### 10.1 Philosophy (Jiadong Chen — Student ID: 723912)

> *"It is to ensure to use a life hardship experiences to still not giving up as a
> life challenge — life change programme."*

This programme recognises that university study intersects with real life: financial
difficulty, health challenges, family obligations, and personal growth. The platform
is designed so that **technology never becomes another barrier**.

### 10.2 Programme Stages

| Stage | State | Duration | Platform Access | Support Features |
|-------|-------|----------|----------------|-----------------|
| **Finance** | Active but under financial stress | Ongoing | Full access; fee deferral integration | AI-powered financial aid finder; Centrelink integration guide; scholarship matcher |
| **Pause** | Study leave / intermission | Up to 6 months (extendable) | Read-only course materials; limited AI chat; progress preserved | Automated check-in messages; mental health resources; return-to-study planning AI |
| **Restart** | Returning to study | From pause end date | Full access restored + AI catch-up | Personalised catch-up plan; missed content summaries; peer mentoring match |
| **Milestone** | 12 February 2026 (Melbourne) | Target completion | Full access + celebration | Achievement recognition; alumni network onboarding; career AI assistant activation |

### 10.3 Key Date

**12 February 2026, Melbourne, Australia** — Target milestone for the Life Challenge
Programme pilot cohort, demonstrating that with the right support infrastructure,
every student can complete their journey regardless of the hardships faced along the way.

---

## 11. Deployment Lifecycle

### 11.1 Alpha → Beta → Production (Language Evolution)

| Phase | Language Stack | Infrastructure | Data | Duration |
|-------|---------------|---------------|------|----------|
| **Alpha** | Python 3.12+ (FastAPI), TypeScript (React) | Local Docker, SQLite, mock APIs | Synthetic / test data | Months 1–3 |
| **Beta** | C# (.NET 8), TypeScript (Next.js), Python (ML) | Azure AKS (staging), Azure SQL, MRI staging | Anonymised production clone | Months 4–8 |
| **Production (C)** | C# (.NET 8 core), C/C++ (performance-critical AI inference), TypeScript (frontend) | Azure AKS (multi-region), Azure SQL HA, MRI production | Live data with geo-redundant backup | Month 9+ |

### 11.2 Environment Matrix

```
┌──────────────────────────────────────────────────────────────────────┐
│  Dev (Alpha)  →  Test  →  Training  →  Staging (Beta)  →  Production│
│                                                                      │
│  Local Docker    CI/CD    Curated       Azure AKS         Azure AKS │
│  SQLite          Auto     Training DB   (AU East)         (AU East + │
│  Mock MRI        pytest   Safe MRI      Azure SQL          SE Asia)  │
│  Synthetic       Daily    Sandbox       MRI Staging        MRI Live  │
│  data            runs     environment   Anonymised data    Live data │
│                                                                      │
│  Backup: Azure Blob (7-day incremental) + Geo-redundant (AU + APAC) │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 12. Roadmap & Milestones

| Quarter | Milestone | Key Deliverables |
|---------|-----------|-----------------|
| **Q1 2026** | Alpha Launch | Core platform scaffold; Azure AI Foundry connected; Canvas migration pilot (Plan A Stage A1–A2); Anti-hallucination v1 |
| **Q2 2026** | Beta & External Onboarding | Full Canvas migration (Plan A Stage A3–A5); Property management beta (Plan B Stage B1–B3); MRI integration live; Government audit portal v1 (Plan C Stage C1–C2) |
| **Q3 2026** | Production & Compliance | Full production deployment; ISO 27001 + IRAP certification; All external agents onboarded; OpenAI/Google EDU tiers active; Life Challenge Programme pilot complete |
| **Q4 2026** | APAC Expansion | NZ pilot deployment; Fiji scoping complete; APAC governance framework published; Full AI chatbot integration (all providers); Research compute cluster live |
| **Q1 2027** | Maturity | Self-optimising AI model selection; Full anti-hallucination v2 with legislation auto-check; APAC partner network established; Annual review and next-gen planning |

---

## Appendix A — Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Identity | Microsoft Entra ID (Azure AD) | SSO, MFA, RBAC, Conditional Access |
| Frontend | React / Next.js / Teams Tabs | Web + Teams experience |
| Mobile | iOS (Swift) — apps 904152776, 1095799806 | UniMelb + MyMBS native apps |
| API Gateway | Azure API Management | Rate limiting, auth, routing |
| Backend | FastAPI (Alpha) → ASP.NET Core (Beta+) | API services |
| AI Engine | Azure AI Foundry + Copilot Studio | Model orchestration |
| AI Models | GPT-4o, Claude Opus/Sonnet, Gemini, DeepSeek | Frontier inference |
| Database | Azure SQL + Cosmos DB | Relational + document store |
| Vector Store | Azure AI Search (vector) + ChromaDB | RAG / embeddings |
| Property Mgmt | MRI Property Tree (API) | Residential + Commercial |
| Monitoring | Azure Monitor + Sentinel + Application Insights | Logging, SIEM, alerts |
| Compliance | Azure Policy + Defender for Cloud | Regulatory enforcement |
| CI/CD | GitHub Actions + Azure DevOps | Build, test, deploy |
| Infrastructure | Azure AKS (Kubernetes) | Container orchestration |
| Backup | Azure Backup + Geo-redundant Storage | Disaster recovery |

---

*This document is a living architecture. It will evolve as the platform moves through
Alpha, Beta, and Production phases. All changes are version-controlled and audit-logged.*

**Pilot Concept by**: Jiadong Chen (Student ID: 723912) — University of Melbourne Graduate
**Date**: 12 February 2026, Melbourne, Australia
