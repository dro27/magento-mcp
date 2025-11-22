import os
import sys
import json
import re
import requests

USE_OLLAMA = True

MCP_SERVER_URL = os.getenv(
    "MCP_SERVER_URL", "http://host.docker.internal:52765/query")
OLLAMA_URL = os.getenv(
    "OLLAMA_URL", "http://host.docker.internal:11434/api/generate")


def clean_sql(raw_sql: str) -> str:
    """Remove markdown artifacts, explanations, and ensure plain SQL."""
    # Remove code fences and markdown formatting
    sql = re.sub(r"```(\w+)?", "", raw_sql)
    sql = sql.replace("```", "")
    # Remove text before SELECT and after semicolon (optional)
    match = re.search(r"(SELECT[\s\S]+?;)", sql, re.IGNORECASE)
    if match:
        sql = match.group(1)
    return sql.strip()


def generate_sql_with_ollama(prompt: str) -> str:
    payload = {
        "model": "llama3",
        "prompt": f"Generate a safe MySQL query for: {prompt}. Only output SQL, no explanation, no markdown formatting."
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        sql = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                sql += data.get("response", "")
        return clean_sql(sql)
    except Exception as e:
        return f"ERROR: Ollama SQL generation failed: {e}"


def query_mcp_server(sql: str):
    try:
        response = requests.post(MCP_SERVER_URL, json={"sql": sql}, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"MCP query failed: {e}"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing query text"}))
        sys.exit(1)

    user_prompt = sys.argv[1]

    # Generate SQL
    sql = generate_sql_with_ollama(user_prompt) if USE_OLLAMA else user_prompt

    # Send SQL to MCP server
    result = query_mcp_server(sql)

    # Output to Magento (or CLI)
    print(json.dumps({
        "sql": sql,
        "result": result
    }))
