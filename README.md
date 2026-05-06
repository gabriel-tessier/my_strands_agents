Hello world and tests using strands agent python sdk.

> agent.py

hello world copy paste from the strands agent Quick start
https://github.com/strands-agents/sdk-python

> code_review_agent.py

Vide coding to test a local AI‑powered code review agent using:

    Strands Agents SDK
    Ollama
    Parallel file review
    Repository walking tool
    Ignore file support (.reviewignore)

🚀 Installation
1. Install Python dependencies

```shell
pip install strands-agents strands-agents-tools
```

2. Install and run Ollama

```shell
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

3. Pull the DeepSeek model

```shell
ollama pull deepseek-coder-v2:latest
```

📁 Project Structure

my_agent/
│
├── code_review_agent.py
├── parallel_review.py
├── tools/
│   └── repo_walker.py
├── django_code_review.prompt
└── .reviewignore   (optional)

📝 Ignore File (.reviewignore)

Create a .reviewignore file in your repo to exclude files or directories:


Glob patterns are supported.
🧠 Running the Agent
▶ Review a single file

```shell
python code_review_agent.py path/to/file.py
```

▶ Review an entire repository

```shell
python code_review_agent.py /path/to/repo
```

▶ Review a cloned GitHub repo

```shell
git clone https://github.com/your/repo.git
python code_review_agent.py repo/
```

▶ Use a custom prompt file

```shell
python code_review_agent.py repo/ --prompt django_code_review.prompt
```

⚡ Parallel Review

Enable parallel processing for large repositories, not tested:

```shell
python code_review_agent.py repo/ --parallel
```

Specify number of workers, not tested:

```shell
python code_review_agent.py repo/ --parallel --workers 8
```

🧩 Repo Walking Tool

The agent automatically:

    walks the directory

    loads ignore patterns from .reviewignore

    filters Python files

    sends them to the model for review

No extra configuration needed.

🧪 Add Extra Context (Optional)

You can pass additional context to help the model understand the module:
bash

python code_review_agent.py repo/ --context "This is the billing service."

