import os
import time
import requests
import json
import tempfile
from io import BytesIO
from dotenv import load_dotenv
from supabase import create_client, Client
import google.generativeai as genai
from elevenlabs.client import ElevenLabs

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Configure APIs
genai.configure(api_key=GEMINI_API_KEY)
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Configure Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

def diagnose_database_connection():
    try:
        print("=== SUPABASE CONNECTION DIAGNOSTIC ===")
        
        # 1. Check basic connection by fetching from system tables
        print("\n1. Checking if we can access the database at all...")
        try:
            # This is a very basic check to see if we can execute any query
            response = supabase.table("refund_requests").select("count", count="exact").execute()
            print(f"✓ Basic connection successful, count query returned: {response.count}")
        except Exception as e:
            print(f"✗ Basic connection failed: {e}")
            return False
        
        # 2. List tables (using PostgreSQL system tables)
        print("\n2. Attempting to list tables using SQL query...")
        try:
            sql_query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            response = supabase.rpc('exec_sql', {'query': sql_query}).execute()
            if hasattr(response, 'data') and response.data:
                print(f"✓ Tables in public schema: {[table['table_name'] for table in response.data]}")
                
                # Check if our target table exists
                table_names = [table['table_name'] for table in response.data]
                if 'refund_requests' in table_names:
                    print("✓ 'refund_requests' table found!")
                else:
                    print(f"✗ 'refund_requests' table NOT found. Available tables: {table_names}")
            else:
                print("✗ No tables found or cannot list tables")
        except Exception as e:
            print(f"✗ Cannot list tables: {e}")
            # Continue even if this fails
        
        # 3. Try direct query with different case variations
        print("\n3. Trying direct queries with different case variations:")
        table_variations = ["refund_requests", "Refund_Requests", "REFUND_REQUESTS", "refund_request"]
        
        for table_name in table_variations:
            try:
                print(f"   Trying: {table_name}")
                response = supabase.table(table_name).select("*").execute()
                print(f"   ✓ Query returned {len(response.data)} rows")
                if len(response.data) > 0:
                    # Found data! Show first row structure (keys only)
                    print(f"   ✓ Found data! First row keys: {list(response.data[0].keys())}")
                    return True  # Success!
            except Exception as e:
                print(f"   ✗ Failed: {e}")
        
        print("\n=== DIAGNOSTIC COMPLETE ===")
        return False  # If we get here, we couldn't find any data
    
    except Exception as e:
        print(f"Diagnostic failed with general error: {e}")
        return False
       
class AudioProcessingAgent:
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        self.skipped_count = 0
        
        # Check if API keys are available
        if not ELEVENLABS_API_KEY:
            print("\n⚠️ WARNING: ELEVENLABS_API_KEY not found in environment variables!")
            print("Speech-to-text transcription will fail without a valid API key.")
            print("Please add your ElevenLabs API key to your .env file:")
            print("ELEVENLABS_API_KEY=your_api_key_here\n")
        else:
            print("ElevenLabs API key found. Ready for transcription.")
            
        if not GEMINI_API_KEY:
            print("\n⚠️ WARNING: GEMINI_API_KEY not found in environment variables!")
            print("Text summarization will fail without a valid API key.")
            print("Please add your Gemini API key to your .env file:")
            print("GEMINI_API_KEY=your_api_key_here\n")
        else:
            print("Gemini API key found. Ready for summarization.")
            
            # List available Gemini models
            try:
                print("\nChecking available Gemini models...")
                available_models = genai.list_models()
                self.gemini_models = [model.name for model in available_models if "gemini" in model.name.lower()]
                print(f"Available Gemini models: {self.gemini_models}")
                
                if not self.gemini_models:
                    print("⚠️ No Gemini models found. Summarization may fail.")
                    self.gemini_models = ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"]
            except Exception as e:
                print(f"Error listing Gemini models: {e}")
                # Default models to try if listing fails
                self.gemini_models = ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"]

    def download_audio(self, audio_url):
        try:
            print(f"Downloading audio from {audio_url}...")
            response = requests.get(audio_url)
            response.raise_for_status()
            
            # Return audio data as BytesIO object
            audio_data = BytesIO(response.content)
            print(f"Audio downloaded successfully ({len(response.content)} bytes)")
            return audio_data
        except Exception as e:
            print(f"Error downloading audio: {e}")
            raise

    def transcribe_audio(self, audio_data):
        try:
            print("Transcribing audio with ElevenLabs Speech-to-Text...")
            
            # First try with auto-detection (omitting language_code parameter)
            try:
                print("Attempting transcription with automatic language detection...")
                transcription = elevenlabs_client.speech_to_text.convert(
                    file=audio_data,
                    model_id="scribe_v1",      # Using the Scribe model
                    tag_audio_events=True,     # Tag events like laughter, applause, etc.
                    diarize=True               # Enable speaker diarization
                    # Note: language_code parameter is omitted for auto-detection
                )
                print("Auto-detection transcription successful")
            except Exception as auto_detect_error:
                print(f"Auto-detection failed: {auto_detect_error}")
                print("Trying with explicit language codes...")
                
                # If auto-detection fails, try with explicit language codes
                # First try with Urdu
                try:
                    print("Attempting transcription with Urdu language code...")
                    # Reset the BytesIO position to the beginning
                    audio_data.seek(0)
                    transcription = elevenlabs_client.speech_to_text.convert(
                        file=audio_data,
                        model_id="scribe_v1",
                        tag_audio_events=True,
                        language_code="urd",   # Urdu language code
                        diarize=True
                    )
                    print("Urdu transcription successful")
                except Exception as urdu_error:
                    print(f"Urdu transcription failed: {urdu_error}")
                    
                    # If Urdu fails, try with Hindi (which might work better for some mixed content)
                    try:
                        print("Attempting transcription with Hindi language code...")
                        # Reset the BytesIO position to the beginning
                        audio_data.seek(0)
                        transcription = elevenlabs_client.speech_to_text.convert(
                            file=audio_data,
                            model_id="scribe_v1",
                            tag_audio_events=True,
                            language_code="hin",   # Hindi language code
                            diarize=True
                        )
                        print("Hindi transcription successful")
                    except Exception as hindi_error:
                        print(f"Hindi transcription failed: {hindi_error}")
                        
                        # If Hindi fails, try with English
                        print("Attempting transcription with English language code...")
                        # Reset the BytesIO position to the beginning
                        audio_data.seek(0)
                        transcription = elevenlabs_client.speech_to_text.convert(
                            file=audio_data,
                            model_id="scribe_v1",
                            tag_audio_events=True,
                            language_code="eng",   # English language code
                            diarize=True
                        )
                        print("English transcription successful")
            
            # Extract the text from the transcription
            if hasattr(transcription, 'text'):
                text = transcription.text
            elif isinstance(transcription, dict) and 'text' in transcription:
                text = transcription['text']
            else:
                text = str(transcription)
            
            print(f"Transcription complete: {text[:100]}..." if len(text) > 100 else text)
            
            # If we have detailed transcription with speakers, format it nicely
            if hasattr(transcription, 'segments') and transcription.segments:
                formatted_text = ""
                for segment in transcription.segments:
                    speaker = f"Speaker {segment.speaker}" if hasattr(segment, 'speaker') and segment.speaker else "Unknown"
                    segment_text = segment.text if hasattr(segment, 'text') else ""
                    formatted_text += f"{speaker}: {segment_text}\n"
                
                print("Formatted transcription with speakers:")
                print(formatted_text[:200] + "..." if len(formatted_text) > 200 else formatted_text)
                return formatted_text
            
            return text
        except Exception as e:
            print(f"Error transcribing with ElevenLabs: {e}")
            
            # Provide troubleshooting information
            
            # Return error message as transcription
            return f"Transcription failed: {str(e)}"

    def summarize_text(self, text):
        try:
            # Configure the generation model
            generation_config = {
                "temperature": 0.2,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 150,
            }
            
            # Try each model in sequence until one works
            last_error = None
            for model_name in self.gemini_models:
                try:
                    print(f"Attempting summarization with model: {model_name}")
                    
                    # Create a Gemini model instance
                    model = genai.GenerativeModel(
                        model_name=model_name,
                        generation_config=generation_config
                    )
                    
                    # Generate the summary
                    prompt = f"""Please summarize this refund request description concisely. 
                    It contains mixed English and Urdu text: {text}"""
                    response = model.generate_content(prompt)
                    
                    summary = response.text.strip()
                    print(f"Summary generated with {model_name}: {summary[:100]}..." if len(summary) > 100 else summary)
                    return summary
                except Exception as e:
                    print(f"Error with model {model_name}: {e}")
                    last_error = e
                    continue
            
            # If we get here, all models failed
            print(f"All Gemini models failed: {last_error}")
            
            # Fallback to a simple summary method
            return self.simple_summarize(text)
        except Exception as e:
            print(f"Error generating summary with Gemini: {e}")
            # Fallback to a simple summary method if Gemini fails
            return self.simple_summarize(text)
    
    def simple_summarize(self, text):
        print("Using simple fallback summarization")
        # Take the first 150 characters as a simple summary
        simple_summary = text[:150] + "..." if len(text) > 150 else text
        
        # If the text is very long, also include a portion from the middle
        if len(text) > 500:
            middle_start = len(text) // 2 - 75
            middle_end = len(text) // 2 + 75
            middle_portion = text[middle_start:middle_end]
            simple_summary += f"\n\nMiddle portion: {middle_portion}..."
        
        return simple_summary

    def update_refund_request(self, request_id, summary):
        try:
            print(f"Updating database for request {request_id}...")
            result = supabase.table("refund_requests").update(
                {"audio_summary": summary}
            ).eq("id", request_id).execute()
            print("Database updated successfully")
            return result
        except Exception as e:
            print(f"Error updating database: {e}")
            raise

    def check_already_processed(self, request_id):
        try:
            response = supabase.table("refund_requests")\
                .select("audio_summary")\
                .eq("id", request_id)\
                .execute()
            
            if response.data and len(response.data) > 0:
                summary = response.data[0].get('audio_summary')
                if summary and not summary.startswith("Error processing audio:"):
                    return True  # Already has a valid summary
            
            return False  # Needs processing
        except Exception as e:
            print(f"Error checking if request {request_id} was processed: {e}")
            return False  # Assume it needs processing if we can't check

    def process_audio_requests(self, start_id=None, process_all=False):
        try:
            # Get all refund requests with audio URLs, ordered by ID
            print("Fetching refund requests with audio URLs...")
            query = supabase.table("refund_requests")\
                .select("id, audio_url")\
                .not_.is_("audio_url", "null")\
                .order("id")  # Order by ID to ensure we process in sequence
            
            # If start_id is provided, only process from that ID onwards
            if start_id is not None:
                query = query.gte("id", start_id)
                
            response = query.execute()
            
            refund_requests = response.data
            print(f"Found {len(refund_requests)} refund requests with audio URLs")
            
            # Print the range of IDs we're processing
            if refund_requests:
                min_id = min(request['id'] for request in refund_requests)
                max_id = max(request['id'] for request in refund_requests)
                print(f"Processing requests with IDs from {min_id} to {max_id}")
            
            for request in refund_requests:
                request_id = request['id']
                audio_url = request['audio_url']
                
                try:
                    print(f"\nProcessing refund request {request_id}")
                    
                    # Check if this request has already been processed
                    if not process_all and self.check_already_processed(request_id):
                        print(f"Request {request_id} already has a summary. Skipping.")
                        self.skipped_count += 1
                        continue
                    
                    print(f"Audio URL: {audio_url}")
                    
                    # Download audio
                    audio_data = self.download_audio(audio_url)
                    
                    # Transcribe audio
                    transcription = self.transcribe_audio(audio_data)
                    
                    # Generate summary
                    summary = self.summarize_text(transcription)
                    
                    # Update database
                    self.update_refund_request(request_id, summary)
                    
                    self.processed_count += 1
                    
                except Exception as e:
                    print(f"Error processing request {request_id}: {e}")
                    # Try to update the database with an error message
                    error_summary = f"Error processing audio: {str(e)[:100]}"
                    try:
                        self.update_refund_request(request_id, error_summary)
                    except:
                        pass
                    self.error_count += 1
                    continue
            
            print(f"\nProcessing complete. Processed: {self.processed_count}, Errors: {self.error_count}, Skipped: {self.skipped_count}")
            return {
                "processed": self.processed_count,
                "errors": self.error_count,
                "skipped": self.skipped_count
            }
                
        except Exception as e:
            print(f"Error fetching refund requests: {e}")
            raise

    def process_single_audio(self, audio_url, request_id=None):
        """Process a single audio URL for testing purposes"""
        try:
            print(f"Processing single audio URL: {audio_url}")
            
            # Download audio
            audio_data = self.download_audio(audio_url)
            
            # Transcribe audio
            transcription = self.transcribe_audio(audio_data)
            
            # Generate summary
            summary = self.summarize_text(transcription)
            
            print("\n=== RESULTS ===")
            print(f"Transcription: {transcription}")
            print(f"Summary: {summary}")
            
            # Update database if request_id is provided
            if request_id:
                self.update_refund_request(request_id, summary)
                print(f"Updated database for request {request_id}")
            
            return {
                "transcription": transcription,
                "summary": summary
            }
        except Exception as e:
            print(f"Error processing audio: {e}")
            raise

# Example usage
if __name__ == "__main__":
    print("Starting audio processing agent with ElevenLabs Speech-to-Text...")
    
    # Initialize the agent
    agent = AudioProcessingAgent()
    username = input("Enter the username of the user you want refund summary of:")
    # Check if we're in test mode (single audio URL)
    test_audio_url = os.getenv("TEST_AUDIO_URL")
    test_request_id = os.getenv("TEST_REQUEST_ID")
    
    # Check if we should start from a specific ID
    start_id = os.getenv("START_ID")
    if start_id:
        try:
            start_id = int(start_id)
            print(f"Starting processing from ID: {start_id}")
        except ValueError:
            print(f"Invalid START_ID: {start_id}. Must be an integer.")
            start_id = None
    
    # Check if we should process all records, including those already processed
    process_all = os.getenv("PROCESS_ALL", "false").lower() in ("true", "1", "yes")
    if process_all:
        print("Will process ALL records, including those already processed")
    
    if test_audio_url:
        print(f"Test mode: Processing single audio URL: {test_audio_url}")
        if test_request_id:
            try:
                test_request_id = int(test_request_id)
                print(f"Will update database for request ID: {test_request_id}")
            except ValueError:
                print(f"Invalid TEST_REQUEST_ID: {test_request_id}. Must be an integer.")
                test_request_id = None
        
        result = agent.process_single_audio(test_audio_url, test_request_id)
    else:
        # Check database connection and process all requests
        if diagnose_database_connection():
            # Run the agent
            result = agent.process_audio_requests(start_id=start_id, process_all=process_all)
            print(f"Final result: {result}")
        else:
            print("Database connection failed!")