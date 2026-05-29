# HW3 – Customer Service Data Analyst Agent

**Students:** Tal Maoz & [Partner Name]

## Project Overview

This project implements a Customer Service Data Analyst Agent for the Bitext Customer Service Dataset.

The agent is able to:

* Answer structured analytical questions about the dataset.
* Answer open-ended questions by analyzing dataset examples.
* Decline out-of-scope questions.
* Maintain conversation memory across sessions.
* Maintain a persistent user profile.
* Expose dataset tools through a FastMCP server.

The implementation uses:

* LangGraph
* LangChain
* FastMCP
* Nebius Token Factory LLMs
* Python

---

## Model Choice

The project uses:

**meta-llama/Llama-3.3-70B-Instruct**

through Nebius Token Factory.

### Why this model?

* Strong reasoning capabilities.
* Good tool-calling behavior.
* Reliable performance for ReAct agents.
* Supports analytical and summarization tasks.
* Compatible with LangChain and LangGraph workflows.

---

## Architecture

The system consists of four main components:

### 1. Router

Classifies incoming user requests into:

* Structured
* Unstructured
* Out-of-scope

### 2. ReAct Agent

Implemented with LangGraph.

The agent:

* Receives user questions.
* Chooses appropriate tools.
* Observes tool outputs.
* Produces final responses.

### 3. Memory Layer

Two types of memory are implemented:

#### Conversation Memory

Stores previous messages for a session.

Example:

* Show me 3 examples from REFUND
* Show me 3 more

The agent remembers the previous context.

#### User Profile Memory

Stores persistent user information.

Example:

* My name is Tal
* I prefer concise answers

The profile is saved and can be retrieved later.

### 4. MCP Server

Dataset tools are exposed through FastMCP.

Available tools:

* get_categories
* get_intents
* count_by_category
* get_examples
* get_intent_distribution

---

## Installation

Create and activate a virtual environment:

```bash
conda create -n hw3_agent python=3.12
conda activate hw3_agent
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
NEBIUS_API_KEY=YOUR_API_KEY
```

---

## Dataset

Place the Bitext dataset inside:

```text
data/bitext.csv
```

---

## Running the CLI Agent

Run:

```bash
python src/main.py --session test1
```

Example questions:

```text
What categories exist in the dataset?

How many refund requests did we get?

Summarize the FEEDBACK category.

Show me 3 examples from the REFUND category.

Show me 3 more.
```

---

## User Profile Memory

Example:

```text
My name is Tal

I am interested in refund analysis

I prefer concise answers

What do you remember about me?
```

---

## Running the MCP Server

Run:

```bash
python mcp_server.py
```

This starts a FastMCP server exposing dataset analysis tools.

Available MCP tools:

* get_categories
* get_intents
* count_by_category
* get_examples
* get_intent_distribution

---

## Project Structure

```text
HW3/
│
├── data/
│   └── bitext.csv
│
├── memory/
│
├── profiles/
│
├── src/
│   ├── agent.py
│   ├── data_loader.py
│   ├── profile_memory.py
│   ├── router.py
│   ├── tools.py
│   └── main.py
│
├── mcp_server.py
├── requirements.txt
├── .env
└── README.md
```
