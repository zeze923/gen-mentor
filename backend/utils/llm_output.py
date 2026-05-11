import re
import json
from typing import Dict, Any


def convert_json_output(output: str) -> Dict[str, Any]:
    """
    Convert raw JSON output from the LLM into structured format.
    Uses robust multi-strategy extraction to handle long content with special characters.
    """
    output = output.strip()

    # Remove markdown code block markers
    if output.startswith("```json"):
        output = output[7:].strip()
    if output.endswith("```"):
        output = output[:-3].strip()
    if output.endswith("```json"):
        output = output[:-7].strip()

    # Remove illegal control characters (preserve \n, \r, \t)
    output = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', output)

    # Strategy 1: Direct parse
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        pass

    # Strategy 2: Brace-tracking extraction
    # Find the outermost JSON object by tracking brace depth
    brace_count = 0
    json_start = -1
    for i, ch in enumerate(output):
        if ch == '{':
            if brace_count == 0:
                json_start = i
            brace_count += 1
        elif ch == '}':
            brace_count -= 1
            if brace_count == 0 and json_start >= 0:
                candidate = output[json_start:i + 1]
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError:
                    continue

    raise json.JSONDecodeError("No valid JSON found in response", output, 0)

def get_text_from_response(response):
    """Extract text from the response object."""
    if 'messages' in response:
        return response['messages'][-1].content
    if 'message' in response['choices'][0]:
        return response['choices'][0]['message']['content']
    return response['choices'][0]['text']

def extract_think_and_result(info):
    "Extract think and result content from the response info."""
    think_match = re.search(r"<think>(.*?)</think>", info, re.DOTALL)
    think_content = think_match.group(1).strip() if think_match else ''
    result_content = re.sub(r"<think>.*?</think>", "", info, flags=re.DOTALL).strip()
    return think_content, result_content


def preprocess_response(response, only_text=True, exclude_think=False, json_output=False):
    if only_text or exclude_think or json_output:
        response = get_text_from_response(response)
    if exclude_think:
        think_content, result_content = extract_think_and_result(response)
        response = result_content
    if json_output:
        try:
            response = convert_json_output(response)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON output: {e}")
            print(f"Raw response content: {response[:500]}...")  # 打印前 500 个字符
            response = {"error": "Invalid JSON output", "raw_content": response}
            raise e
    return response

