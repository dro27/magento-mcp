
# How to setup Magento MCP

This MCP is build using
[mysql_mcp_server](https://github.com/designcomputer/mysql_mcp_server?utm_source=chatgpt.com) and Uvicorn.

### Step 1

Clone this repo in your Magento Project

Export the env variable via cmd

via Docker

    export OLLAMA_URL="http://host.docker.internal:11434/api/generate"

    export MCP_SERVER_URL="http://host.docker.internal:52765/query"

or if in localhost

    export OLLAMA_URL="http://localhost:11434/api/generate"

    export MCP_SERVER_URL="http://localhost:52765/query"

### Step 2

Setup Ollama Model


    curl -fsSL https://ollama.com/install.sh | sh

    ollama serve

  

Test ollama

    curl http://127.0.0.1:11434/api/tags

or

    curl http://host.docker.internal:11434/api/tags

  

### Step 3

Setup MCP


Create venv and activate it:

``source venv-mcp/bin/activate``


Install the MySQL MCP and Uvicorn

``pip install --upgrade mysql_mcp_server``

``pip install uvicorn``

Setup up the server for the mysql mcp: mcp_http_wrapper.py

You can put the server in a different directory or WSL. It's up to you.

  
Create .env
```
    MYSQL_HOST=127.0.0.1
    MYSQL_PORT=32779
    MYSQL_USER=db
    MYSQL_PASSWORD=db
    MYSQL_DATABASE=db
    MCP_HOST=0.0.0.0
    MCP_PORT=52765
```
export it and activate the server

``export $(grep -v '^#' .env | xargs)``

``python mcp_http_wrapper.py``

  
### Step 4 (Optional) Test it

Go back to Magento Module and run:

``python app/code/Mcp/ClaudeMcp/mcp_claude_bridge.py "count the total customers from the table customer_entity"``
