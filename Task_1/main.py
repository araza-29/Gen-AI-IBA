from Services.sql_generator import generate_sql
from Services.supabase_client import execute_sql

def agent():
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Exiting the program.")
            break
        try:
            sql_query = generate_sql(user_input)
            print("Generated SQL:", sql_query)
            result = execute_sql(sql_query)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    agent()
