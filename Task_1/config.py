from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# SUPABASE_URL = "https://ewqqiiowvwdzsnemaixq.supabase.co"
# SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV3cXFpaW93dndkenNuZW1haXhxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUwNjMwNzMsImV4cCI6MjA2MDYzOTA3M30.c3GD_Zsh-RrMpnmc-rQo1t4fXEhnQotfjFQpMfhVZ90"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
