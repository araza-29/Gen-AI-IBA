from config import supabase

def execute_sql(sql):
    try:
        sql = sql.strip().rstrip(';')
        command = sql.split()[0].lower()

        if command == 'select':
            response = supabase.rpc("execute_sql", {"query": sql}).execute()
        elif command in ('insert', 'update', 'delete'):
            response = supabase.rpc("execute_mutation", {"query": sql}).execute()
        else:
            raise ValueError(f"Unsupported SQL command: {command}")

        return response.data
    except Exception as e:
        print("DB Error:", e)
        return None
