from Services.sql_generator import generate_sql
from Services.supabase_client import execute_sql
from tabulate import tabulate

def agent():
    print("Welcome, How may I help you? (type 'exit' to leave)")
    while True:
        
        user_input = input("\nUser: ").strip()
        print('')
        if user_input.lower() == "exit":
            print("Exiting the program.")
            break
        try:
            print("Loading...")
            sql_query = generate_sql(user_input)
            print("\nAgent executing SQL query:", sql_query)
            result = execute_sql(sql_query)
            print("\nResponse:", result)
            print("\nFormatted Response:")
            print(tabulate(result, headers="keys", tablefmt="github"))
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    agent()
