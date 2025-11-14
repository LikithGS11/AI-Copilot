import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client only if API key is available
groq_key = os.getenv("GROQ_API_KEY")
if not groq_key or groq_key.strip() == "":
    client = None
else:
    client = Groq(api_key=groq_key)

# Allow model selection via environment variable
# Default to llama-3.1-8b-instant (safe, stable, working model on Groq)
GROQ_MODEL = os.getenv("GROQ_MODEL")
DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"
MODEL_NAME = GROQ_MODEL if GROQ_MODEL else DEFAULT_GROQ_MODEL


def _format_api_error(exc: Exception) -> str:
    """Return a user-friendly Groq API error message with remediation steps."""
    msg = str(exc)
    guidance = (
        f"[GROQ ERROR: {msg}]\n"
        "Remediation:\n"
        "- Ensure `GROQ_API_KEY` is valid and has permission for the model.\n"
        "- To use a different model, set `GROQ_MODEL` environment variable.\n"
        "- Current model: llama-3.1-8b-instant\n"
        "- See: https://console.groq.com/docs/models\n"
    )
    return guidance

def _groq_api_call_with_retry(messages, max_tokens, max_retries=3):
    """Make a Groq API call with retry logic for transient failures."""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.3,
                max_tokens=max_tokens
            )
            return response
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                time.sleep(wait_time)
                continue
            else:
                raise e

def load_json(file_path):
    """Load data from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(file_path, data):
    """Save data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def save_version(section_id, content, versions_dir):
    """Save a version of the edited content with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"section_{section_id}_{timestamp}.json"
    filepath = os.path.join(versions_dir, filename)
    data = {
        "section_id": section_id,
        "timestamp": timestamp,
        "content": content
    }
    save_json(filepath, data)

def regenerate_content(original_text):
    if client is None:
        return "GROQ_API_KEY is missing or invalid."

    prompt = f"""
Rewrite the following educational content to improve clarity, readability,
and flow. Keep the meaning the same. Make it more structured and teacher-friendly.

Content:
{original_text}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        result = response.choices[0].message.content.strip()
        if not result:
            return "Groq returned an empty response. Check your API key or model."
        return result
    except json.JSONDecodeError:
        return "Groq returned invalid JSON. Check your API key or model."
    except Exception as e:
        return _format_api_error(e)

def summarize_changes(version_a, version_b):
    if client is None:
        return "GROQ_API_KEY is missing or invalid."

    prompt = f"""
Summarize the semantic differences between Version A (Original) and
Version B (Edited). Highlight improvements, clarity changes, added ideas,
or removed details.

Version A:
{version_a}

Version B:
{version_b}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )
        result = response.choices[0].message.content.strip()
        if not result:
            return "Groq returned an empty response. Check your API key or model."
        return result
    except json.JSONDecodeError:
        return "Groq returned invalid JSON. Check your API key or model."
    except Exception as e:
        return _format_api_error(e)

def generate_module(curriculum_text, pedagogy_text, user_prompt):
    if client is None:
        return None, "GROQ_API_KEY is missing or invalid."

    prompt = f"""
Based on the following curriculum and pedagogy guidelines, generate a structured JSON for a module.

Curriculum:
{curriculum_text if curriculum_text else "Not provided"}

Pedagogy:
{pedagogy_text if pedagogy_text else "Not provided"}

User Request: {user_prompt}

Generate a JSON with exactly this structure:
{{
  "module_title": "string",
  "sections": [
    {{
      "id": "sec1",
      "title": "string",
      "content": "string",
      "type": "learning_objective|lesson|assessment",
      "bloom_level": "Remember|Understand|Apply|Analyze|Evaluate|Create"
    }}
  ]
}}

Output ONLY the JSON, nothing else. No markdown, no code blocks, just pure JSON.
"""

    try:
        response = _groq_api_call_with_retry(
            [{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        
        # Check if response has choices
        if not response.choices or len(response.choices) == 0:
            return None, "Groq returned no choices. API may be rate limited or down."
        
        json_str = response.choices[0].message.content.strip()
        
        # Check if response is empty
        if not json_str:
            return None, "Groq returned an empty response. API may be overloaded or key invalid."
        
        # Try to extract JSON if it's wrapped in markdown
        if json_str.startswith("```"):
            json_str = json_str.split("```")[1]
            if json_str.startswith("json"):
                json_str = json_str[4:]
            json_str = json_str.strip()
        
        # Validate and parse JSON
        data = json.loads(json_str)
        
        # Validate structure
        if "module_title" not in data or "sections" not in data:
            return None, "Invalid JSON structure: missing 'module_title' or 'sections'"
        
        if not isinstance(data["sections"], list) or len(data["sections"]) == 0:
            return None, "Invalid JSON structure: 'sections' must be a non-empty list"
        
        return data, None
        
    except json.JSONDecodeError as e:
        return None, f"Failed to parse Groq response as JSON: {str(e)}. Response may be truncated or malformed."
    except Exception as e:
        return None, _format_api_error(e)
