#!/usr/bin/env python
import requests
import json
import sys
import time
from urllib.parse import urlparse
from typing import Optional, Dict, Any, Iterator, Union, Callable


class N8nWebhookClient:
    def __init__(self, webhook_url: str, headers: Optional[Dict[str, str]] = None):
        self.webhook_url = webhook_url
        self.headers = headers or {}

        parsed_url = urlparse(webhook_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError(f"Invalid webhook URL: {webhook_url}")

    def stream_response(self, 
                        user_input: str,
                        method: str = "GET", 
                        timeout: int = 60) -> Iterator[Union[str, Dict[str, Any]]]:
        try:
            request_kwargs = {
                'url': self.webhook_url,
                'headers': self.headers,
                'stream': True,
                'timeout': timeout,
                'params': {'chatInput': user_input}
            }

            with requests.request(method.upper(), **request_kwargs) as response:
                response.raise_for_status()

                for chunk in response.iter_lines(decode_unicode=True, delimiter="\n"):
                    if not chunk:
                        continue
                    
                    try:
                        parsed_chunk = json.loads(chunk)
                        yield parsed_chunk
                        time.sleep(0.05)
                    except json.JSONDecodeError:
                        pass

        except requests.RequestException as e:
            print(f"Error connecting to webhook: {e}")
            raise

    def respond(self, user_input: str) -> None:
        for chunk in self.stream_response(user_input):
            chunk_type = chunk.get("type")

            if chunk_type == "begin":
                sys.stdout.write("\nAI: ")
                sys.stdout.flush()
            elif chunk_type == "item":
                content = chunk.get("content", "")
                sys.stdout.write(content)
                sys.stdout.flush()
            elif chunk_type == "end":
                sys.stdout.write("\n")
                sys.stdout.flush()


if __name__ == "__main__":
    WEBHOOK_URL_DEV = "https://adarmesh20.app.n8n.cloud/webhook-test/9dc4acd6-6523-46dc-a0ef-33b13f3d1d0d"
    WEBHOOK_URL_PROD = "https://adarmesh20.app.n8n.cloud/webhook/9dc4acd6-6523-46dc-a0ef-33b13f3d1d0d"
    WEBHOOK_URL_ROUTER_DEV = "https://adarmesh20.app.n8n.cloud/webhook-test/34ee585f-90e5-4a26-a8bb-98c91179de15"
    WEBHOOK_URL_ROUTER_PROD = "https://adarmesh20.app.n8n.cloud/webhook/34ee585f-90e5-4a26-a8bb-98c91179de15"
    
    client = N8nWebhookClient(WEBHOOK_URL_ROUTER_DEV)

    while True:
        user_input = input("\nYou: ")
        if user_input.strip().lower() == "exit":
            print("Exiting chat.")
            break
        client.respond(user_input)

