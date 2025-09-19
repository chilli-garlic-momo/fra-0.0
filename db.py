from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY length: {len(SUPABASE_KEY) if SUPABASE_KEY else 'None'}")


# Optional safety check
if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase URL or KEY not set in environment variables!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_record(entities, ocr_text, pdf_path):
    data = {
        "claimant_name": entities.get('CLAIMANT_NAME', [None])[0],
        "village": entities.get('VILLAGE', [None])[0],
        "date_claimed": entities.get('DATE', [None])[0],
        "ocr_text": ocr_text,
        "proofant_pdf_path": pdf_path,
    }
    response = supabase.table("fra_records").insert(data).execute()

    # Since response object has no status/status_code or error attributes,
    # we print the response data to check for error info
    print("Supabase response data:", response.data)

    # Optional: You can try to check if response.data contains an error message
    if isinstance(response.data, dict) and "message" in response.data:
        print("Failed to insert:", response.data["message"])
    else:
        print("Record inserted successfully")
