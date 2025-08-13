#!/usr/bin/env python
import requests
import json
import sys
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
                       method: str = "GET", 
                       data: Optional[Dict[str, Any]] = None, 
                       chunk_callback: Optional[Callable[[str], None]] = None,
                       timeout: int = 60) -> Iterator[Union[str, Dict[str, Any]]]:
        try:
            request_kwargs = {
                'url': self.webhook_url,
                'headers': self.headers,
                'stream': True,
                'timeout': timeout
            }
            
            with requests.request(method.upper(), **request_kwargs) as response:
                response.raise_for_status()
                
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        parsed_chunk = None
                        try:
                            parsed_chunk = json.loads(chunk)
                        except json.JSONDecodeError:
                            parsed_chunk = chunk
                        
                        # Call the callback if provided
                        if chunk_callback:
                            chunk_callback(parsed_chunk)
                        
                        yield parsed_chunk
                        
        except requests.RequestException as e:
            print(f"Error connecting to webhook: {e}", file=sys.stderr)
            raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Client for n8n webhook chunked responses")
    parser.add_argument("--url", help="n8n webhook URL", required=True)
    parser.add_argument("--method", help="HTTP method (GET, POST, etc.)", default="GET")
    parser.add_argument("--data", help="JSON data to send with the request")
    
    args = parser.parse_args()
    
    client = N8nWebhookClient(args.url)
    
    try:
        data = json.loads(args.data) if args.data else None
        
        print(f"Connecting to {args.url} using {args.method}...")
        
        for chunk in client.stream_response(method=args.method, data=data):
            print(f"Received chunk: {chunk}")
            if type(chunk) == str:
                try:
                    chunk = json.loads(chunk)
                    print(chunk.content)
                except json.JSONDecodeError as e:
                    print(f"Failed to decode JSON: {chunk}. {e}")

            # if isinstance(chunk, dict):
            #     # print(json.dumps(chunk, indent=2))
            #     if hasattr(chunk, 'type') and chunk.type not in ('begin', 'end'):
            #         print(chunk.content)
            # else:
            #     print(chunk)
    except KeyboardInterrupt:
        print("\nClient stopped by user")
    except Exception as e:
        print(f"Error: {e}")
