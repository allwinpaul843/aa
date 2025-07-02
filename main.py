import streamlit as st
from core.pipeline import process_spellcorrect_user_query, process_suggestion_user_query
from core.drive_utils import authenticate_drive, download_file_from_drive, upload_file_to_drive
import json
import os

st.title("Query Correction and Enrichment Tool")

user_query = st.text_area("Enter your search query:")

# Google Drive file IDs for your cache files
REMOTE_CACHE_FILE_ID = '18chHJFUjHivG-_lG8f8Ambifx5fJsQIE'
SEMANTIC_PROMPT_CACHE_FILE_ID = '1CE8PjeFxzYU9_TmgLGSOAWRr3DbqMT9R'  # <-- Replace with your actual file ID
REMOTE_CACHE_PATH = 'remote_generation_cache.sqlite'
SEMANTIC_PROMPT_CACHE_PATH = 'semantic_prompt_cache.sqlite'
SERVICE_ACCOUNT_JSON = 'service_account.json'

# Handle Streamlit Cloud secrets (if present)
if 'GOOGLE_SERVICE_ACCOUNT_JSON' in st.secrets:
    with open(SERVICE_ACCOUNT_JSON, 'w') as f:
        json.dump(st.secrets['GOOGLE_SERVICE_ACCOUNT_JSON'], f)

drive = authenticate_drive(SERVICE_ACCOUNT_JSON)

# Download cache files at startup
try:
    download_file_from_drive(drive, REMOTE_CACHE_FILE_ID, REMOTE_CACHE_PATH)
except Exception as e:
    st.warning(f'Could not download remote_generation_cache: {e}')
try:
    download_file_from_drive(drive, SEMANTIC_PROMPT_CACHE_FILE_ID, SEMANTIC_PROMPT_CACHE_PATH)
except Exception as e:
    st.warning(f'Could not download semantic_prompt_cache: {e}')

if st.button("Correct & Suggest"):
    if user_query.strip():
        typo_found, corrected_text, relevant_df, _string_columns = process_spellcorrect_user_query(user_query.strip())
        if not typo_found:
            st.info("No typos found in the query.")
            suggestions = process_suggestion_user_query(user_query.strip(), relevant_df, _string_columns)
            st.write("Top Suggestions:")
            st.write(suggestions)
        else:
            st.success(f"Corrected Query: {corrected_text}")
            suggestions = process_suggestion_user_query(corrected_text, relevant_df, _string_columns)
            st.write("Top Suggestions:")
            st.write(suggestions)
        # Upload cache files after processing
        try:
            upload_file_to_drive(drive, REMOTE_CACHE_FILE_ID, REMOTE_CACHE_PATH)
        except Exception as e:
            st.warning(f'Could not upload remote_generation_cache: {e}')
        try:
            upload_file_to_drive(drive, SEMANTIC_PROMPT_CACHE_FILE_ID, SEMANTIC_PROMPT_CACHE_PATH)
        except Exception as e:
            st.warning(f'Could not upload semantic_prompt_cache: {e}')
    else:
        st.warning("Please enter a query.")