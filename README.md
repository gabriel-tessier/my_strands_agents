Hello world and tests using strands agent python sdk.

## Agents

### `my_strands_agents.agent`

Hello-world copy-paste from the [Strands Agents Quick Start](https://github.com/strands-agents/sdk-python).
Demonstrates a custom `letter_counter` tool alongside the built-in `calculator` and `current_time` tools.

### `my_strands_agents.code_review`

Vibe-coded, local AI-powered code review agent using:

- Strands Agents SDK
- Ollama
- Parallel file review
- Repository walking tool
- Ignore file support (`.reviewignore`)

## 🚀 Installation

### 1. Install Python dependencies

```shell
pip install -e ".[dev]"
```

### 2. Install and run Ollama

```shell
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

### 3. Pull the required models

```shell
ollama pull llama3.1:8b               # for the hello-world agent
ollama pull deepseek-coder-v2:latest  # for code review
```

## 📁 Project Structure

```
my_strands_agents/
├── __init__.py
├── agent.py                  # letter_counter tool + hello-world main()
├── code_review/
│   ├── __init__.py
│   ├── agent.py              # build_agent, review_code, load_prompt, main()
│   └── parallel.py           # review_files_in_parallel
├── prompts/
│   ├── django_code_review.prompt
│   ├── diagrams_icons_metadata_review.prompt
│   └── diagrams_project_review.prompt
└── tools/
    ├── __init__.py
    └── repo_walker.py        # walk_repository tool

tests/
├── test_agent.py
├── test_code_review.py
├── test_parallel.py
└── test_repo_walker.py

pyproject.toml
.reviewignore                 # optional – exclude paths from review
```

## 📝 Ignore File (`.reviewignore`)

Create a `.reviewignore` file in the repository you are reviewing to exclude files or directories.
Glob patterns (as understood by `pathlib.Path.match`) are supported.

## 🧠 Running the Agents

### Hello-world agent

```shell
python -m my_strands_agents.agent
# or after pip install -e .
strands-agent
```

### ▶ Review a single file

```shell
code-review path/to/file.py
```

### ▶ Review an entire repository

```shell
code-review /path/to/repo
```

### ▶ Use a custom prompt file

```shell
code-review repo/ --prompt /path/to/my.prompt
```

### ⚡ Parallel Review

```shell
code-review repo/ --parallel --workers 8
```

### 🧪 Add Extra Context (Optional)

```shell
code-review repo/ --context "This is the billing service."
```

## 🧪 Running Tests

```shell
pytest
```

