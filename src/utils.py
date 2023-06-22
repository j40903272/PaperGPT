import json
import requests
import tiktoken
import logging


def json_validator(
    text: str,
    openai_key: str,
    retry: int = 3,
    model: str = "text-davinci-003"
):
    
    encoder = tiktoken.encoding_for_model(model)
    
    for _ in range(retry):
        try:
            return json.loads(text)
        except Exception:
            
            try:
                prompt = f"Modify the following into a valid json format:\n{text}"
                prompt_token_length = len(encoder.encode(prompt))

                data = {
                    "model": model,
                    "prompt": prompt,
                    "max_tokens": 4097 - prompt_token_length - 64
                }
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {openai_key}"
                }
                for _ in range(retry):
                    response = requests.post(
                        'https://api.openai.com/v1/completions',
                        json=data,
                        headers=headers,
                        timeout=300
                    )
                    if response.status_code != 200:
                        logging.warning(f'fetch openai chat retry: {response.text}')
                        continue
                    text = response.json()['choices'][0]['text']
                    break
            except Exception:
                return response.json()['error']
            
    return text


def fetch_chat(
    prompt: str,
    openai_key: str,
    retry: int = 3,
    model: str = "gpt-3.5-turbo-16k"
):
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_key}"
    }
    for _ in range(retry):
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            json=data,
            headers=headers,
            timeout=300
        )
        if response.status_code != 200:
            logging.warning(f'fetch openai chat retry: {response.text}')
            continue
        result = response.json()['choices'][0]['message']['content']
        return result
    
    return response.json()["error"]
