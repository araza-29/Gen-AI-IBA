def format_prompt(nl_query):
    schema = """
    Table: employees(id, created_at, name, age, salary)
    Table: refund_requests(id, created_at, name, amount, image_url, audio_url, audio_summary)
    """
    return f"""
You are a helpful AI assistant that only responds with valid SQL queries.

Given the following database schema:
{schema}

Your task is to convert the following natural language question into a syntactically correct PostgreSQL SQL query.

Respond with **only the SQL query**, and nothing else. Do not include explanations or comments.

Natural Language Question:
"{nl_query}"
"""
