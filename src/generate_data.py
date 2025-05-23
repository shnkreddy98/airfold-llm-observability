from datetime import datetime
import random
import uuid
import time
from typing import List, Dict, Any

WORDS_FILE = "./data/words.txt"

# OpenAI models list
OPENAI_MODELS = ["gpt-4.1-2025-04-14", "gpt-4.1-mini-2025-04-14", "gpt-4.1-nano-2025-04-14",
                 "gpt-4.5-preview-2025-02-27", "gpt-4o-2024-11-20", "gpt-4o-2024-08-06", 
                 "gpt-4o-2024-05-13", "gpt-4o-realtime-preview-2024-12-17", "gpt-4o-mini-2024-07-18",
                 "gpt-4o-mini-realtime-preview-2024-12-17", "o1-2024-12-17", "o1-preview-2024-09-12",
                 "o4-mini-2025-04-16", "o3-mini-2025-01-31", "o1-mini-2024-09-12",
                 "codex-mini-latest", "gpt-4o-mini-search-preview", "gpt-4o-search-preview-2025-03-11"]

# Status options
STATUS_OPTIONS = ["completed", "incomplete", "failed"]

# Truncation options  
TRUNCATION_OPTIONS = ["disabled", "auto", "always"]

# Tool choice options
TOOL_CHOICE_OPTIONS = ["auto", "required", "none"]

# User agents for request headers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "OpenAI/Python/1.3.8",
    "OpenAI/Node.js/4.20.1",
    "axios/1.6.0",
    "python-requests/2.31.0",
    "Postman/10.19.0",
    "curl/8.4.0"
]

# Load words for content generation
try:
    with open(WORDS_FILE, "r") as f:
        WORDS = [word.strip() for word in f if word.strip().isalpha()]
except FileNotFoundError:
    # Fallback words if file doesn't exist
    WORDS = ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'lazy', 'dog', 'hello', 'world', 
             'artificial', 'intelligence', 'machine', 'learning', 'data', 'science', 'technology',
             'innovation', 'future', 'digital', 'algorithm', 'neural', 'network', 'deep', 'learning',
             'peaceful', 'grove', 'beneath', 'silver', 'moon', 'unicorn', 'magical', 'realm',
             'stardust', 'shimmer', 'wonder', 'dream', 'sparkle', 'wish', 'pathway', 'hidden']

def generate_realistic_ip():
    """Generate realistic IP addresses"""
    # Common cloud provider IP ranges
    cloud_ranges = [
        (3, 5),      # Amazon AWS partial
        (13, 107),   # Amazon AWS partial
        (52, 54),    # Amazon AWS partial
        (104, 155),  # Google Cloud partial
        (34, 35),    # Google Cloud partial
        (40, 52),    # Microsoft Azure partial
        (137, 138),  # Microsoft Azure partial
    ]
    
    if random.random() < 0.3:  # 30% chance of cloud IP
        first, second = random.choice(cloud_ranges)
        return f"{first}.{second}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    else:  # Regular IP
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_realistic_tokens(model_name: str):
    """Generate realistic token counts based on model type"""
    # Determine model category and adjust tokens accordingly
    if 'o1' in model_name.lower():
        # O1 models typically use more reasoning tokens
        input_tokens = random.randint(20, 200)
        output_tokens = random.randint(50, 300)
        reasoning_tokens = random.randint(100, 1000)
    elif 'gpt-4' in model_name.lower():
        # GPT-4 variants
        input_tokens = random.randint(30, 500)
        output_tokens = random.randint(50, 800)
        reasoning_tokens = 0
    elif 'gpt-3.5' in model_name.lower():
        # GPT-3.5 variants
        input_tokens = random.randint(20, 300)
        output_tokens = random.randint(30, 500)
        reasoning_tokens = 0
    else:
        # Default for other models
        input_tokens = random.randint(10, 200)
        output_tokens = random.randint(20, 400)
        reasoning_tokens = 0
    
    # Sometimes have cached tokens
    cached_tokens = random.randint(0, input_tokens // 3) if random.random() < 0.2 else 0
    
    return {
        "input_tokens": input_tokens,
        "input_tokens_details": {
            "cached_tokens": cached_tokens
        },
        "output_tokens": output_tokens,
        "output_tokens_details": {
            "reasoning_tokens": reasoning_tokens
        },
        "total_tokens": input_tokens + output_tokens + reasoning_tokens
    }

def generate_text_content(min_words: int = 10, max_words: int = 100):
    """Generate realistic text content"""
    word_count = random.randint(min_words, max_words)
    words = random.choices(WORDS, k=word_count)
    
    # Create sentences
    sentences = []
    current_sentence = []
    
    for i, word in enumerate(words):
        current_sentence.append(word)
        
        # End sentence randomly or at end
        if (random.random() < 0.15 and len(current_sentence) > 5) or i == len(words) - 1:
            sentence = " ".join(current_sentence)
            sentence = sentence.capitalize() + random.choice(['.', '!', '?'])
            sentences.append(sentence)
            current_sentence = []
    
    return " ".join(sentences)

def generate_tools():
    """Generate function tools (sometimes empty)"""
    if random.random() < 0.3:  # 30% chance of having tools
        return [{
            "type": "function",
            "function": {
                "name": random.choice(["get_weather", "search_web", "calculate", "send_email"]),
                "description": f"A function that {generate_text_content(3, 8)}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input": {"type": "string", "description": "Input parameter"}
                    },
                    "required": ["input"]
                }
            }
        }]
    return []

def generate_output_message():
    """Generate output message array"""
    return [{
        "type": "message",
        "id": f"msg_{uuid.uuid4().hex}",
        "status": random.choice(STATUS_OPTIONS),
        "role": "assistant",
        "content": [{
            "type": "output_text",
            "text": generate_text_content(20, 150),
            "annotations": []
        }]
    }]

def generate_reasoning():
    """Generate reasoning object"""
    return {
        "effort": random.choice([None, "low", "medium", "high"]) if random.random() < 0.3 else None,
        "summary": generate_text_content(5, 20) if random.random() < 0.1 else None
    }

def generate_text_format():
    """Generate text format object"""
    return {
        "format": {
            "type": "text"
        }
    }

def generate_request_messages():
    """Generate request messages array"""
    # Generate 1-5 messages in conversation
    message_count = random.randint(1, 5)
    messages = []
    
    # Start with user message
    roles = ['user', 'assistant']
    current_role = 0
    
    for i in range(message_count):
        role = roles[current_role]
        content = generate_text_content(5, 50) if role == 'user' else generate_text_content(10, 100)
        
        messages.append({
            "role": role,
            "content": content
        })
        
        # Alternate roles (but end with user message)
        if i < message_count - 1:
            current_role = 1 - current_role
        else:
            # Always end with user message for the request
            if role != 'user':
                messages.append({
                    "role": "user", 
                    "content": generate_text_content(5, 30)
                })
    
    return messages

def generate_request_data(timestamp: int):
    """Generate request data including headers and message"""
    return {
        "timestamp": timestamp - random.randint(1, 10),  # Request came slightly before response
        "ip": generate_realistic_ip(),
        "user_agent": random.choice(USER_AGENTS),
        "headers": {
            "Content-Type": "application/json",
            "Authorization": f"Bearer sk-{uuid.uuid4().hex}",
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json",
            "Connection": "keep-alive",
            "Content-Length": str(random.randint(200, 2000)),
            "Host": "api.openai.com",
            "X-Request-ID": f"req_{uuid.uuid4().hex[:16]}",
        },
        "messages": generate_request_messages()
    }

def generate_openai_response(response_id: str, timestamp: int, previous_response_ids: List[str] = None):
    """Generate a realistic OpenAI API response matching the exact format"""
    
    # Select random model
    model = random.choice(OPENAI_MODELS)
    
    # Determine status first to control other fields
    status = random.choice(STATUS_OPTIONS)
    
    # Control output, error, and incomplete_details based on status
    if status == "completed":
        output = generate_output_message()
        error = {}
        incomplete_details = {}
    elif status == "failed":
        output = []
        error = {
            "type": "api_error",
            "code": random.choice(["rate_limit_exceeded", "insufficient_quota", "model_overloaded", "processing_error"]),
            "message": "An error occurred while processing the request."
        }
        incomplete_details = {}
    else:  # incomplete
        output = generate_output_message()  # Partial output for incomplete
        error = {}
        incomplete_details = {
            "reason": random.choice(["max_tokens", "content_filter", "tool_calls"])
        }
    
    # Control parallel_tool_calls, tools, and tool_choice
    parallel_tool_calls = random.choice([True, False])
    if parallel_tool_calls:
        tools = generate_tools()
        if not tools:  # If no tools generated, create at least one
            tools = [{
                "type": "function",
                "function": {
                    "name": "get_current_time",
                    "description": "Get the current time",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }]
        tool_choice = random.choice(TOOL_CHOICE_OPTIONS)
    else:
        tools = []
        tool_choice = "none"
    
    # Determine if this response has a previous response reference
    previous_response_id = None
    if previous_response_ids and random.random() < 0.1:  # 10% chance of referencing previous
        previous_response_id = random.choice(previous_response_ids)
    
    # Generate user with 60% returning users - simplified approach
    if random.random() < 0.7:  # 70% chance of having a user
        if random.random() < 0.6:  # 60% chance of returning user (simplified)
            user_id = random.randint(1, 20)  # Pick from pool of 20 users
            user = f"user_{str(user_id).zfill(8)}"
        else:  # New user
            user = f"user_{uuid.uuid4().hex[:8]}"
    else:
        user = None
    
    return {
        "id": response_id,
        "object": "response",
        "created_at": timestamp,
        "status": status,  # Status with complete should have output and no error, status with failed or incomplete should have error and no output
        "error": error,
        "incomplete_details": incomplete_details,
        "instructions": None,
        "max_output_tokens": random.randint(100, 4000) if random.random() < 0.3 else None,
        "model": model,
        "output": output,
        "parallel_tool_calls": parallel_tool_calls,  # when true tools and tools_choice should have values otherwise none
        "previous_response_id": previous_response_id,
        "reasoning": generate_reasoning(),
        "store": random.choice([True, False]),
        "temperature": round(random.uniform(0.0, 2.0), 1),
        "text": generate_text_format(),
        "tool_choice": tool_choice,
        "tools": tools,
        "top_p": round(random.uniform(0.1, 1.0), 1),
        "truncation": random.choice(TRUNCATION_OPTIONS),
        "usage": generate_realistic_tokens(model),
        "user": user,  # User should be repeating every once in a while, say 60% returning users
        "metadata": {},  # Always empty dict as per example
        "request": generate_request_data(timestamp)
    }

def generate_batch_responses(count: int, stream: bool = False):
    """Generate a batch of OpenAI responses"""
    
    responses = []
    response_ids = []
    
    for i in range(count):
        now = int(datetime.now().timestamp())

        if stream:
            request_timestamp = now
        else:
            start_ts = int(datetime(2024, 1, 1, 0, 0).timestamp())
            end_ts = now
            request_timestamp = random.randint(start_ts, end_ts)

        # Generate timestamp with some randomness
        timestamp = request_timestamp + int(random.triangular(0, 300, 60))  # within 5 mins
        
        # Generate response ID
        response_id = f"resp_{uuid.uuid4().hex}"
        
        # Generate response
        response = generate_openai_response(response_id, timestamp, response_ids)
        
        responses.append(response)
        response_ids.append(response_id)
    
    # Sort by timestamp
    responses.sort(key=lambda x: x['created_at'])
    
    return responses

def save_responses_to_file(responses: List[Dict], filename: str = "openai_responses.json"):
    """Save generated responses to a JSON file"""
    import json
    with open(filename, 'w') as f:
        json.dump(responses, f, indent=2)
    print(f"Saved {len(responses)} responses to {filename}")

# Example usage
if __name__ == "__main__":
    # Generate 50 responses
    responses = generate_batch_responses(50)
    
    # Save to file
    save_responses_to_file(responses)
    
    # Print sample response
    import json
    print("\nSample Response:")
    print(json.dumps(responses[0], indent=2))