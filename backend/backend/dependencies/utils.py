from base64 import b64encode

def convert_bytes_to_b64_src(blob: bytes, mime_type: str) -> str:
    return f"data:{mime_type};base64,{b64encode(blob).decode('utf-8')}"
