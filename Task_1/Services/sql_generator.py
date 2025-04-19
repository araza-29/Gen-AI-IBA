import google.generativeai as genai
from Utils.prompt_helper import format_prompt

genai.configure(api_key="AIzaSyCxXgWTduZ9FNw0hef7qIDlrG8I_5QDlPg")

model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

def generate_sql(nl_query):
    prompt = format_prompt(nl_query)
    print(prompt)

    response = model.generate_content(prompt)
    print(response)
    sql = response.text.strip()

    # Remove Markdown code block formatting
    sql = sql.replace("```sql", "").replace("```", "").strip()

    if not sql.lower().startswith(("select", "insert", "update", "delete")):
        raise ValueError("The model did not return a valid SQL statement.")
    
    return sql


