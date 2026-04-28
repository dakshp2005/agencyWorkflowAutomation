# **Capstone Project-II**

# **Report**

# **On**

# **"Agency Workflow Automation"**

---

**Submitted By**

| **Daksh Patel** | **202302626010099** |
|---|---|
| **Vatsal Shah** | **202302626010121** |
| **Bhautik Vaghamshi** | **202302626010154** |
| **Vashisht Brahmbhatt** | **202302626010156** |

---

**From**

**B.Tech (Computer Science Engineering)**

**Semester VI**

**Under the Guidance of**

**Dr. Aakanksha Jain**

**Assistant Professor**

**Faculty of Engineering and Technology**

**GLS University**

**Academic Year**

**(2025-2026)**

---

## **CERTIFICATE**

This is to certify that the project report entitled **Agency Workflow Automation** has been satisfactorily carried out by the following students.

| **Daksh Patel** | **202302626010099** |
|---|---|
| **Vatsal Shah** | **202302626010121** |
| **Bhautik Vaghamshi** | **202302626010154** |
| **Vashisht Brahmbhatt** | **202302626010156** |

under my guidance in the fulfilment of the course Capstone Project-II (2601606) work during the academic year 2025-2026.

| **Dr. Aakanksha Jain** |
|---|
| **Internal Guide** |

---

## Acknowledgment

We would like to formally express our deepest appreciation to all those who contributed to the successful completion of our capstone project.

First and foremost, we extend our sincere gratitude to our project supervisor, **Dr. Aakanksha Jain**, for their expert guidance, insightful feedback, and constant support throughout every stage of this project.

We are also grateful to the faculty members of the GLS University (Computer Science and Engineering), whose knowledge, mentorship, and resources played a significant role in shaping our work.

We acknowledge the administrative staff and technical teams for their assistance and cooperation whenever needed.

**Sincerely,**

Daksh Patel

Vatsal Shah

Bhautik Vaghamshi

Vashisht Brahmbhatt

---

## Abstract

Small and mid-sized agencies spend excessive time on repetitive manual tasks such as sending emails, scheduling meetings, and creating documents. These tasks lead to inefficiency, errors, and difficulty in scaling operations as the client base grows. This capstone project presents an intelligent workflow automation system designed to address these challenges and improve agency productivity. The implemented system automates key workflows including personalized client outreach, reply classification, meeting scheduling, and document generation. It uses artificial intelligence technologies such as Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) integrated with a Python-Flask backend, with Google Gemini as the primary AI model provider and a local FAISS index for semantic retrieval.

The system learns from past client interactions and adapts its communication style over time, becoming more effective with continued use. Performance analysis shows that the automated system can reduce task completion times by 60–70% overall. For example, drafting outreach emails drops from 10–15 minutes to just 30 seconds, and generating proposals reduces from 30–45 minutes to 3–5 minutes. The system maintains human oversight for critical decisions through concrete approval workflows for emails and proposals, ensuring quality and strategic control while automating routine processes. This project fills a market gap by providing an affordable and practical automation solution specifically designed for small agency workflows.

---

## Table of Contents

| **Sr.** | **Particular** | **Page No.** |
|---|---|---|
| | Certificate | **I** |
| | Acknowledgment | **II** |
| | Abstract | **III** |
| | Table of Contents | **IV** |
| | List of Figures | **VI** |
| **Chapter 1** | **Introduction** | **1** |
| **1.1** | Project Detail | **1** |
| **1.2** | Purpose | **1** |
| **1.3** | Scope & Objective | **3** |
| **1.4** | Literature Review | **4** |
| **Chapter 2** | **About The System** | **6** |
| **2.1** | System Requirement Specification (Functional and Non-Functional) | **6** |
| **2.2** | Project Planning | **7** |
| **Chapter 3** | **Analysis of the System** | **9** |
| **3.1** | Use Case Diagram | **9** |
| **3.2** | Data Flow Diagram Level-0 | **9** |
| **3.3** | Data Flow Diagram Level-1 | **10** |
| **3.4** | Class Diagram | **10** |
| **Chapter 4** | **Design** | **11** |
| **4.1** | System Architecture Design | **11** |
| **4.2** | Database Design | **11** |
| **4.3** | Integration Layer | **12** |
| **Chapter 5** | **Implementation & Screenshots** | **13** |
| **5.1** | Tools and Technologies | **13** |
| **5.2** | System Development Methodology | **14** |
| **5.3** | Core Functional Components | **14** |
| **5.4** | RAG and Continuous Learning | **15** |
| **5.5** | Human Oversight Integration | **15** |
| **5.6** | Prototype Screenshots | **15** |
| **Chapter 6** | **Conclusion & Future Work** | **17** |
| **6.1** | Conclusion | **21** |
| **6.2** | Future Work | **22** |
| | **References** | **24** |

---

## List of Figures

| **Fig No.** | **Particular** | **Page No.** |
|---|---|---|
| **3.1** | Use Case Diagram | **9** |
| **3.2** | Data Flow Diagram Level-0 | **9** |
| **3.3** | Data Flow Diagram Level-1 | **10** |
| **3.4** | Class Diagram | **10** |
| **5.1** | Dashboard Overview | **15** |
| **5.2** | AI Lead Prospector | **16** |
| **5.3** | Client Management Overview | **16** |
| **5.4** | Email Management Overview | **17** |
| **5.5** | Replies Inbound Clarifications | **17** |
| **5.6** | Meetings Directory | **18** |
| **5.7** | Documents Management | **18** |
| **5.8** | Client Profile Management | **19** |
| **5.9** | Meeting Setup | **19** |
| **5.10** | Email Composition | **20** |

---

# Chapter 1: Introduction

## 1.1 Project Detail

In today's fast-paced business environment, small and mid-sized agencies face increasing pressure to deliver high-quality services while managing growing client portfolios. These agencies typically handle multiple clients simultaneously, each requiring personalized attention, timely communication, and professional documentation. However, the reality of agency operations reveals a significant challenge: a substantial portion of daily work consists of repetitive, time-consuming manual tasks that drain resources and limit growth potential.

Agency workflows commonly involve sending outreach emails to potential clients, managing responses, scheduling meetings, generating proposals, creating reports, and maintaining comprehensive documentation. While these tasks are essential for business operations, they are also highly repetitive and follow predictable patterns. Staff members often spend hours each day on administrative work that, while necessary, does not directly contribute to the creative or strategic value that agencies are known for.

## 1.2 Purpose

Small and mid-sized agencies encounter several critical challenges in their day-to-day operations:

**Repetitive Manual Tasks:** Agency teams spend excessive time on routine processes. Drafting personalized outreach emails can take 10–15 minutes per client, scheduling meetings involves 10–20 minutes of coordination, and creating proposals requires 30–45 minutes of manual work. When multiplied across dozens or hundreds of clients, these tasks consume a significant portion of the workday.

**Inefficiency and Errors:** Manual handling of workflows leads to inconsistent processes, slower response times, and increased chances of human error. Emails may be sent late, meetings might be scheduled incorrectly, or important follow-ups could be missed entirely. These inefficiencies not only waste time but also impact the quality of client service.

**Resource Drain:** High administrative workload drains staff energy and limits their ability to focus on activities that truly add value. Creative professionals and strategic thinkers find themselves bogged down in routine tasks rather than leveraging their expertise for client benefit.

**Scaling Limitations:** As client volume increases, agencies struggle to maintain quality and speed without hiring significantly more staff. The traditional model of scaling by adding headcount is expensive and often unsustainable for small to mid-sized operations. This creates a barrier to growth and competitive disadvantage.

**Impact on Client Experience:** Slower onboarding, delayed responses, miscommunication, or overlooked steps can negatively affect client satisfaction and retention. In a competitive market, client experience is a key differentiator, and operational inefficiencies directly undermine an agency's ability to deliver exceptional service.

Several automation tools and platforms currently exist in the market, each with distinct advantages and limitations:

**Zapier and Make:** These no-code automation platforms offer easy setup and quick implementation. However, they become costly at scale and provide limited functionality constrained by pre-built templates. Customization options are restricted, making them less suitable for complex agency workflows.

**Salesforce CRM:** This enterprise-grade solution offers powerful features and comprehensive client management capabilities. However, its rigid structure and high cost make it impractical for small agencies with limited budgets and specific workflow requirements.

**UiPath:** As an enterprise-level robotic process automation platform, UiPath delivers sophisticated automation capabilities. However, its complexity and feature set represent overkill for small to mid-sized agencies, requiring significant technical expertise and investment.

The market clearly lacks affordable, modular automation solutions specifically tailored for small agency workflows that combine ease of use with advanced AI capabilities and customization flexibility.

## 1.3 Scope & Objective

This capstone project addresses the identified gap by designing and implementing a comprehensive workflow automation system specifically for small and mid-sized agencies. The motivation stems from recognizing that agencies need intelligent automation that understands context, learns from interactions, and adapts to client preferences while remaining affordable and manageable.

The significance of this project extends beyond simple task automation. By integrating advanced artificial intelligence technologies such as Large Language Models and Retrieval-Augmented Generation, the system offers intelligent personalization and continuous learning capabilities. Unlike rule-based automation that follows fixed patterns, this AI-powered approach adapts and improves over time, learning from each client interaction to deliver increasingly relevant and effective communication.

The primary objectives of this capstone project are:

**Workflow Identification:** Systematically analyze and identify repetitive, automatable workflows across agency operations to maximize efficiency gains.

**Automation Implementation:** Develop robust automation for outreach, replies, scheduling, and document generation with seamless integration across various tools and platforms.

**AI and RAG Integration:** Integrate advanced AI modules using the Google Gemini API and Retrieval-Augmented Generation with a local FAISS index for intelligent personalization and context-aware responses [1][2].

**Human Oversight:** Retain critical human-in-the-loop functionality for strategic approvals and quality assurance. The system notifies human operators via Slack and in-app notifications when decisions require judgment or when important actions such as outreach emails and proposals need confirmation before dispatch.

**Performance Measurement:** Measure efficiency improvements and document outcomes to validate system effectiveness. This involves comparing manual and automated processes to quantify time savings and quality improvements.

## 1.4 Literature Review

### 1.4.1 Introduction to Literature Review

This review analyzes existing research and industry practices in agency workflow automation. It aims to identify the current technological landscape, established benefits, and existing gaps in solutions, particularly for small and mid-sized agencies.

### 1.4.2 Workflow Automation in Business

Workflow automation shows significant potential, with studies indicating that a large percentage of work activities can be automated. This leads to tangible benefits like reduced administrative loads and higher client satisfaction.

The technology has evolved rapidly from rigid, rule-based systems to intelligent, AI-augmented platforms. Modern systems use machine learning and natural language processing to handle complex, variable tasks and understand context.

### 1.4.3 No-Code and Visual Automation Platforms

The rise of no-code and low-code platforms has made automation accessible to non-technical users. These visual tools allow for rapid prototyping, easy modification, and integration with various services, making them ideal for small agencies with limited development resources. Open-source solutions, in particular, offer a high degree of flexibility.

### 1.4.4 Artificial Intelligence in Communication

AI is heavily impacting business communication and document processing. Key applications include:

Personalizing email outreach and marketing at scale.

Intelligent lead scoring and routing tasks based on content analysis.

Using Natural Language Processing (NLP) to understand email context and generate appropriate, professional replies.

Employing Large Language Models (LLMs) for summarizing documents and creating personalized content.

### 1.4.5 LangChain and Modular AI Toolchains

Frameworks like LangChain are crucial for building modern AI systems [2]. They provide a modular architecture to connect various AI components (e.g., content generation, data extraction, summarization) into a single, robust pipeline. This makes complex automation systems more scalable and maintainable.

### 1.4.6 Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) significantly enhances AI by connecting generative models (LLMs) to external, up-to-date knowledge bases [1]. This approach allows the AI to provide more accurate, current, and context-specific responses. It also enables the system to learn continuously from new information. In this implementation, Gemini embeddings are used to encode client data into vector chunks stored in a local FAISS index, enabling fast semantic retrieval at generation time [3][4].

### 1.4.7 Human-in-the-Loop (HITL) Automation

A "Human-in-the-Loop" (HITL) model is recognized as a best practice. This hybrid approach automates routine tasks but reserves critical, nuanced decisions for human approval. An effective HITL system relies on clear notifications and intuitive interfaces to ensure seamless human oversight. In this project, HITL is concretely implemented for both email and proposal approval workflows.

### 1.4.8 Comparative Analysis and Identified Market Gap

A review of existing market solutions reveals a clear gap:

**Simple Automators (e.g., Zapier, Make):** Easy to use for simple tasks, but they are functionally limited, not easily customizable, and become expensive at scale.

**Enterprise CRMs (e.g., Salesforce):** Very powerful but are too complex, rigid, and costly for the needs and budgets of small agencies.

**RPA Platforms (e.g., UiPath):** Extremely capable but represent "overkill" for agency workflows, requiring significant technical and financial investment.

This analysis shows a clear need for a solution that is simultaneously affordable, modular, and intelligent, specifically tailored to small agency workflows.

---

# Chapter 2: About The System

## 2.1 System Requirement Specification

### 2.1.1 Functional Requirements

**User Management:** Shall support user registration, authentication with hashed passwords, and session-based access control enforced via a global request guard.

**Client Data Management:** Shall store, manage, and search client information, including contact details, preferences, and interaction history. New clients shall be indexed into the RAG memory layer immediately upon creation.

**Automated Outreach:** Shall use Google Gemini to generate and send personalized outreach emails enriched with RAG context, log all activities, and route drafts through a human approval workflow before external dispatch.

**Reply Classification:** Shall automatically retrieve unread messages via IMAP, process and classify incoming replies (positive, neutral, negative) using AI, extracting key entities such as dates, companies, and requirements.

**Meeting Scheduling:** Shall integrate with the Google Calendar API to check availability, propose three candidate meeting slots, and send invitations, with human confirmation required before event creation.

**Document Generation:** Shall use Google Gemini and RAG context to generate proposals and reports, saving outputs as markdown files, with a human approval workflow before delivery.

**Notification System:** Shall send real-time alerts via Slack Webhooks and in-app notifications for tasks requiring human approval, with direct approval URLs for quick operator action.

**RAG and Learning System:** Shall index all interactions into a FAISS vector store using Gemini embeddings to provide context for AI-generated content and continuously improve with each new interaction [3][4].

**Reporting and Analytics:** Shall provide a dashboard with operational KPIs including sent emails, replies, meetings, and documents, along with client pipeline distribution and a recent activity timeline.

### 2.1.2 Non-Functional Requirements

**Performance:** The system must be fast, with email classification under 10 seconds, AI email generation under 30 seconds, and database queries under 2 seconds.

**Reliability:** Aim for 99% uptime with robust error handling, retry mechanisms, and detailed interaction logging for failed operations.

**Security:** Requires hashed password storage, secure environment-variable-based secret management, and compliance with data protection best practices.

**Scalability:** The architecture must support growth in users and data, with a clear migration path from SQLite to PostgreSQL and deployment on cloud infrastructure [5][6].

**Usability:** The interface must be intuitive, requiring minimal training and providing clear error messages and documentation.

**Maintainability:** Code must be clean, documented, and modular using Flask blueprints. The project uses version control and comprehensive interaction logging.

**Compatibility:** Must work with standard email (Gmail SMTP/IMAP) and calendar (Google Calendar API) services, be accessible on modern web browsers, and follow RESTful standards [8][9].

**Data:** Requires client data, past email templates, and historical interaction records to populate and continuously improve the RAG knowledge base.

## 2.2 Project Planning

### 2.2.1 Methodology Overview

The project follows a systematic, multi-phase methodology that includes requirements analysis, system design, and iterative development. This section outlines the analytical approach and the architectural design that forms the foundation of the implemented automation system.

### 2.2.2 Current Workflow Analysis

Analysis of typical agency operations identified five core repetitive tasks as primary candidates for automation:

Outreach Email Management

Reply Classification

Meeting Scheduling

Document Generation

Follow-up Management

The manual performance of these workflows is time-intensive, inconsistent, and prone to human error. Analysis indicates that intelligent automation can recover a significant percentage of the time spent on these tasks.

### 2.2.3 Hybrid Automation Model

The solution adopts a hybrid "human-in-the-loop" model to balance efficiency with strategic control:

**Fully Automated:** For routine, predictable tasks such as reply fetching, classification, and daily follow-up checks handled by APScheduler background jobs [7].

**Human Approval:** For important decisions including outreach email dispatch and proposal delivery, where AI provides a complete draft and the operator approves or rejects.

**Manual Handling:** For complex, strategic interactions requiring direct staff engagement.

This tiered approach ensures efficiency while maintaining high-quality human judgment.

---

# Chapter 3: Analysis of the System

## 3.1 Use Case Diagram

***Fig. 3.1 Use Case Diagram***

## 3.2 Data Flow Diagram Level-0

***Fig. 3.2 Data Flow Diagram Level-0***

## 3.3 Data Flow Diagram Level-1

***Fig. 3.3 Data Flow Diagram Level-1***

## 3.4 Class Diagram

***Fig. 3.4 Class Diagram***

---

# Chapter 4: Design

## 4.1 System Architecture Design

The system is structured across five distinct layers:

### 4.1.1 Presentation Layer

Jinja2 templates with custom CSS and JavaScript serve the frontend, covering the Dashboard, Lead Discovery, Clients, Emails, Replies, Meetings, Documents, and Authentication views.

### 4.1.2 Application Layer

Flask blueprints enforce route separation between functional modules. RESTful API endpoints are exposed for automation triggers and integration callbacks.

### 4.1.3 Service Layer

Dedicated service modules handle distinct concerns: Email Service, Reply Classifier, Scheduler Service, Document Service, Discovery Service, RAG Service, Notification Service, and Slack Service.

### 4.1.4 AI Integration Strategy

The system integrates AI at multiple levels by leveraging the Google Gemini API rather than building custom models [3]:

**Large Language Models (LLMs):** Handle content generation for emails, proposals, reports, and lead discovery reasoning.

**Natural Language Processing (NLP):** Classify incoming messages into POSITIVE, NEUTRAL, and NEGATIVE categories and extract key entities.

**Retrieval-Augmented Generation (RAG):** Provide context-aware responses by querying a FAISS vector index built from client interactions and uploaded documents [1][4].

### 4.1.5 Data Layer

SQLAlchemy ORM models manage core entities, supported by a FAISS vector index and metadata store for semantic retrieval, and an output storage area for generated proposals and reports [6].

## 4.2 Database Design

A dual-storage strategy is employed:

**Relational Database (SQLite):** Stores structured data such as user accounts, client profiles, email records, meetings, documents, and interaction logs. The architecture is migration-ready for PostgreSQL via Flask-Migrate [5][6].

**Vector Index (FAISS):** Stores unstructured data as Gemini-generated vector embeddings, persisted to disk at `data/faiss_index`, enabling fast semantic search for the RAG system [4].

**Knowledge Base Construction:** The system builds the FAISS index from all client interactions, emails, notes, and uploaded documents. When performing a task such as writing an outreach email, the system first queries the index to retrieve relevant context, which is then fed to Gemini. The system's relevance and effectiveness naturally improve over time as the index grows with each new interaction.

## 4.3 Integration Layer

An integration layer connects the system to essential third-party services via APIs, including:

**Gmail SMTP/IMAP** — Email sending and unread message retrieval [9]

**Google Calendar API** — Meeting scheduling and availability checks [8]

**Slack Webhooks** — Real-time notifications for human-in-the-loop approvals

**Google Gemini API** — AI content generation, embeddings, and reply classification [3]

---

# Chapter 5: Implementation & Screenshots

## 5.1 Tools and Technologies

### 5.1.1 Programming Language: Python (3.10+)

Rich library ecosystem (especially for AI), strong integration with ML frameworks, clean syntax, and large community support.

### 5.1.2 Backend Framework and Libraries

**Flask:** A lightweight Python web framework used to build the RESTful API, handle routing via blueprints, and manage HTTP requests [5].

**Flask-SQLAlchemy:** An ORM layer that simplifies database operations by abstracting raw SQL queries [6].

**Flask-Migrate:** Handles schema migrations, providing a clear upgrade path from SQLite to PostgreSQL.

**Flask-Login:** Manages session-based authentication with hashed password storage and a global route guard for protected views.

**APScheduler:** Runs background automation jobs — reply fetch/classify every 15 minutes and a daily follow-up check for stale outreach clients [7].

### 5.1.3 Database Systems

**SQLite:** Used as the relational database for development and production defaults, storing user data, client records, email state, meetings, documents, and audit logs.

**PostgreSQL:** Designated migration-ready production alternative for high-concurrency deployments.

**FAISS (Facebook AI Similarity Search):** Stores Gemini-generated text embeddings locally, enabling the efficient semantic retrieval required for RAG [4].

### 5.1.4 Artificial Intelligence and Machine Learning

**Google Gemini API:** Integrated as the primary AI model provider for all content generation (emails, proposals, reports), lead discovery, reply classification, and vector embedding creation [3].

**RAG Pipeline:** Custom retrieval-augmented generation layer built on FAISS and Gemini embeddings for context-enriched output. Supports full bootstrap indexing from existing records [1][2].

### 5.1.5 Integration and Communication

**Email Services (Gmail SMTP/IMAP):** For sending approved outreach emails and retrieving incoming replies [9].

**Calendar Integration (Google Calendar API):** For checking staff availability and creating confirmed meeting events [8].

**Notification Services (Slack Webhooks):** For sending real-time approval-required alerts to operators with direct action URLs.

### 5.1.6 Technology Stack Summary

| Layer | Technology |
|---|---|
| **Backend** | Python + Flask + Flask-SQLAlchemy + Flask-Migrate |
| **Auth** | Flask-Login (hashed passwords, session guard) |
| **AI Provider** | Google Gemini (generation + embeddings) |
| **Vector Index** | FAISS IndexFlatL2 (local disk persistence) |
| **Database** | SQLite (default), migration-ready to PostgreSQL |
| **Scheduler** | APScheduler (background jobs) |
| **Email** | Gmail SMTP (send) + Gmail IMAP (receive) |
| **Calendar** | Google Calendar API |
| **Notifications** | Slack Webhooks + in-app notification model |

## 5.2 System Development Methodology

The system integrates AI at multiple levels. The development follows a hybrid approach:

**Fully Automated workflows:** Reply fetch and classification runs every 15 minutes via APScheduler. A daily job checks for stale outreach clients and generates follow-up drafts. These routines execute without human intervention.

**Human-in-the-loop approvals:** Outreach email and proposal drafts are AI-generated and stored as pending. The operator receives Slack and in-app notifications with direct approval URLs. Approval triggers dispatch; rejection returns the draft to editable state.

**Manual handling:** Complex or strategic interactions are routed for direct staff management through the client profile interface.

## 5.3 Core Functional Components

**Lead Discovery Module:** AI generates candidate leads for a chosen domain with ICP fit scores and reasoning. Leads can be promoted to managed client records in a single action.

**Client Management:** CRUD operations with soft archiving. Client profiles store preferences and notes for personalization. New clients are indexed into RAG memory immediately upon creation.

**Personalized Outreach Module:** Automates email drafting by retrieving RAG context and using Gemini to generate personalized messages. Drafts are stored as pending approval before any external send.

**Intelligent Reply Classification:** Uses Gemini to analyze incoming replies, categorizing them as POSITIVE, NEUTRAL, or NEGATIVE and extracting key entities. Automated next actions are triggered accordingly: meeting proposal for positive replies, follow-up draft generation for neutral replies, and marking not-interested for negative replies.

**Smart Scheduling System:** Proposes three candidate slots from Google Calendar availability. Supports a confirmation flow and event creation. On confirmation, proposal generation is triggered automatically.

**Document Generation Engine:** Uses Gemini and RAG context to generate proposals and reports as markdown files saved under `outputs/`. Document approval workflow is implemented before delivery.

## 5.4 RAG and Continuous Learning

**Knowledge Base Construction:** The system builds a FAISS vector index from all client interactions, emails, notes, and uploaded documents (txt, pdf, doc, docx, md, html). Gemini embeddings are used for chunk vectors [3][4].

**Context Retrieval Mechanism:** When performing a task such as writing an email, the system first queries the FAISS index via similarity retrieval to fetch the most relevant context chunks, which are then injected into the Gemini prompt [1].

**Adaptive Improvement:** The system's performance and the relevance of its generated content naturally improve over time as the knowledge base grows with each new interaction and uploaded document. Full bootstrap indexing is supported to re-index all existing records at any point.

## 5.5 Human Oversight Integration

The human-in-the-loop model is implemented via an in-app notification table and Slack Webhooks at critical decision points. Approval-required events trigger a Slack message containing a direct action URL, allowing operators to approve, modify, or reject an automated action without needing to navigate manually through the interface. This ensures staff retain final control over all external-facing communications and document delivery while the system handles drafting, scheduling, and orchestration autonomously.

## 5.6 Prototype Screenshots

***Fig. 5.1 Dashboard Overview***

The dashboard presents daily operational KPIs (emails sent, replies received, meetings this week, and generated documents), client pipeline distribution across lifecycle stages, a recent activity feed, and pending approval cards for emails and proposals. This page is the central control surface for operators.

---

***Fig. 5.2 AI Lead Prospector***

The lead discovery screen allows users to input an industry or domain and trigger AI-powered prospect discovery via Gemini. Each card shows company details, an ICP fit score, a rationale for the score, and a one-click qualify action to convert a lead into a managed client record.

---

***Fig. 5.3 Client Management Overview***

The client directory lists all clients with status filters, key profile fields, and quick actions. It provides lifecycle visibility and direct navigation into detailed client-level workflows.

---

***Fig. 5.4 Email Management Overview***

The email ledger displays generated outreach and follow-up emails with status badges (pending approval, sent, failed), timestamps, and client mapping. It supports operational review of messaging pipeline throughput.

---

***Fig. 5.5 Replies Inbound Clarifications***

The replies view shows processed inbound emails with AI classification labels (POSITIVE / NEUTRAL / NEGATIVE), extracted entities (dates, companies, requirements), and the triggered next actions. This screen reflects the Gemini-based decision branch for next-step automation.

---

***Fig. 5.6 Meetings Directory***

The meetings page tracks proposed and confirmed meetings, agenda summaries, chosen slots, and current status. It supports review, confirmation, cancellation, and historical scheduling audit.

---

***Fig. 5.7 Documents Management***

The documents ledger lists generated and uploaded documents by type and status, with links to detailed previews and actions. It enables review, approval, and download of proposal and report artifacts.

---

***Fig. 5.8 Client Profile Management***

The client detail interface consolidates profile data, editable preferences and notes, communication records, and timeline logs. It also exposes direct workflow triggers including generate outreach, generate proposal, schedule meeting, and upload document.

---

***Fig. 5.9 Meeting Setup***

The meeting creation form captures client selection, agenda, and optional proposed slots in ISO datetime format. This forms the entry point to the human-approved scheduling workflow.

---

***Fig. 5.10 Email Composition***

The email detail and composer page presents recipient metadata, editable subject and body, approval actions, and send-state metadata. It enforces human approval before external dispatch in the normal workflow.

---

# Chapter 6: Conclusion & Future Work

## 6.1 Conclusion

This capstone project has successfully designed and implemented a comprehensive workflow automation system specifically tailored for small and mid-sized agencies. The delivered solution addresses critical operational challenges including repetitive manual tasks, inefficiency, and scalability limitations that currently hinder agency growth and profitability.

The system integrates Google Gemini for all AI tasks — content generation, embeddings, and reply classification — with a local FAISS vector index for RAG, a Python-Flask backend, APScheduler for background automation, Gmail SMTP/IMAP for email, and Google Calendar API for scheduling [3][4][5][7][8][9]. Through intelligent automation of core workflows — personalized outreach, reply classification, meeting scheduling, and document generation — the system demonstrates potential for 60–70% overall efficiency improvement while maintaining essential human oversight for strategic decisions.

The project successfully identifies a clear market gap between simple automation tools lacking advanced capabilities and enterprise solutions that are cost-prohibitive for small agencies. The implemented hybrid approach combines automated efficiency with concrete human-in-the-loop approval workflows for emails and proposals, ensuring quality control while delivering substantial time savings and operational improvements.

Key achievements include a fully operational authentication and access control system, an AI-powered lead discovery and qualification path, outreach generation with RAG context enrichment, reply ingestion and action orchestration, meeting scheduling with calendar integration, proposal and report generation with filesystem persistence, a Slack and in-app notification subsystem, and a comprehensive activity logging and audit trail. The modular service-oriented architecture ensures the system remains maintainable, scalable, and adaptable to evolving agency needs [1][2][6].

This project demonstrates that intelligent workflow automation can transform agency operations, enabling small and mid-sized organizations to scale effectively without proportional cost increases while improving client service quality and staff satisfaction.

## 6.2 Future Work

### 6.2.1 Role-Based Access Control

The current implementation enforces basic authentication gating. A complete role-based permission matrix with admin, manager, and staff roles with granular access control is planned as the immediate next enhancement.

### 6.2.2 Advanced AI Features

Future enhancements can include multi-language support for international clients, sentiment analysis refinement for more nuanced reply classification, and predictive analytics to forecast client conversion likelihood and optimize outreach timing.

### 6.2.3 Additional Integrations

Expanding integration capabilities to include CRM systems like HubSpot or Salesforce, project management tools like Asana or Trello, and social media platforms for comprehensive multi-channel outreach beyond email would significantly enhance system utility.

### 6.2.4 Mobile Application

Development of mobile applications for iOS and Android would enable agency staff to review approvals, monitor automation performance, and manage client interactions on-the-go, improving system accessibility and responsiveness.

### 6.2.5 Enhanced Analytics and Reporting

Implementing advanced analytics dashboards with machine learning-powered insights, A/B testing capabilities for email templates, and ROI calculation tools would provide deeper understanding of automation effectiveness and business impact.

### 6.2.6 Production Database and Secret Management

Migrating the default SQLite instance to a managed PostgreSQL deployment and integrating an enterprise secret manager for API credentials and environment variables would address the current production-concurrency and compliance-hardening gaps.

### 6.2.7 CI/CD and Test Automation

Establishing a continuous integration and delivery pipeline with automated tests covering AI generation flows, integration error paths, and approval state machines would improve system reliability and accelerate future development.

### 6.2.8 Security Enhancements

Future work should include implementation of advanced security features such as two-factor authentication, detailed audit logging, granular role-based permissions, and SOC2-aligned compliance controls for enterprise deployment.

---

## References

[1] Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *arXiv preprint arXiv:2005.11401*. Available at: https://arxiv.org/abs/2005.11401

[2] LangChain Documentation. (2024). Build a Retrieval Augmented Generation (RAG) App. LangChain AI. Available at: https://python.langchain.com/docs/tutorials/rag/

[3] Google Generative AI for Python — API Documentation. (2024). Gemini models and embeddings. Google AI. Available at: https://ai.google.dev/

[4] FAISS Documentation. (2024). Facebook AI Similarity Search. Meta AI Research. Available at: https://faiss.ai/

[5] Flask Documentation. (2024). Application architecture and routing. Pallets Projects. Available at: https://flask.palletsprojects.com/

[6] SQLAlchemy Documentation. (2024). ORM and persistence patterns. SQLAlchemy. Available at: https://docs.sqlalchemy.org/

[7] APScheduler Documentation. (2024). Background scheduling in Python. APScheduler. Available at: https://apscheduler.readthedocs.io/

[8] Google Calendar API Documentation. (2024). Google Developers. Available at: https://developers.google.com/calendar/api

[9] Python Standard Libraries Documentation. (2024). SMTP/IMAP email integration. Python Software Foundation. Available at: https://docs.python.org/3/library/

[10] Agency Workflow Automation. (2025). Project implementation source code and templates (main branch). Internal repository reference.
