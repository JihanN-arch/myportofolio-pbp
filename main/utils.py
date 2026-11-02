import re
from urllib.parse import parse_qs, urlparse

def to_direct_img_url(value):
    """ Ubah link share Google Drive jdi link gambang lgsg, link lain dibiarkan """
    
    if not value:
        return value
    
    parsed = urlparse(value)
    if parsed.netloc not in ("drive.google.com", "docs.google.com"):
        return value
    
    match = re.search(r"/d/([\w-]+)", parsed.path)
    file_id = match.group(1) if match else parse_qs(parsed.query).get("id", [None])[0]
    if not file_id:
        return value
    
    return f"https://lh3.googleusercontent.com/d/{file_id}"    