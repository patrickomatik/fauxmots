import email
import base64
import quopri
import chardet
from email.header import decode_header

def decode_value(value):
    """Decode email header values."""
    if value is None:
        return ""
        
    decoded_parts = []
    for part, encoding in decode_header(value):
        if isinstance(part, bytes):
            if encoding:
                try:
                    decoded_parts.append(part.decode(encoding))
                except:
                    # If specified encoding fails, try to detect it
                    detected = chardet.detect(part)
                    try:
                        decoded_parts.append(part.decode(detected['encoding'] or 'utf-8', errors='replace'))
                    except:
                        decoded_parts.append(part.decode('utf-8', errors='replace'))
            else:
                # No encoding specified, try to detect it
                detected = chardet.detect(part)
                try:
                    decoded_parts.append(part.decode(detected['encoding'] or 'utf-8', errors='replace'))
                except:
                    decoded_parts.append(part.decode('utf-8', errors='replace'))
        else:
            decoded_parts.append(part)
    
    return ''.join(decoded_parts)

def parse_payload(part, attachments=None):
    """Parse message part payload."""
    content_type = part.get_content_type()
    charset = part.get_content_charset() or 'utf-8'
    payload = part.get_payload(decode=True)
    
    if not payload:
        return ''
    
    # Try to decode with the specified charset
    try:
        if isinstance(payload, bytes):
            text = payload.decode(charset, errors='replace')
        else:
            text = payload
    except:
        # If decoding fails, try to detect the encoding
        if isinstance(payload, bytes):
            detected = chardet.detect(payload)
            try:
                text = payload.decode(detected['encoding'] or 'utf-8', errors='replace')
            except:
                text = payload.decode('utf-8', errors='replace')
        else:
            text = payload
    
    # Handle attachment if this is one
    if attachments is not None and part.get_filename():
        filename = decode_value(part.get_filename())
        attachments.append({
            'filename': filename,
            'content_type': content_type,
            'size': len(payload) if payload else 0
        })
        # For attachments, we don't include the content
        return f'[Attachment: {filename}]'
    
    return text

def parse_email_file(filepath):
    """Parse email file and extract content and headers."""
    with open(filepath, 'rb') as f:
        msg = email.message_from_binary_file(f)
    
    # Extract headers
    headers = {}
    for key in msg.keys():
        headers[key] = decode_value(msg[key])
    
    # Extract body parts and attachments
    body_parts = {
        'text/plain': [],
        'text/html': []
    }
    
    attachments = []
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if part.get_filename():
                # This is an attachment
                parse_payload(part, attachments)
            elif content_type == 'text/plain':
                body_parts['text/plain'].append(parse_payload(part))
            elif content_type == 'text/html':
                body_parts['text/html'].append(parse_payload(part))
            elif content_type.startswith('multipart/'):
                # Skip multipart containers
                continue
            else:
                # Unknown content type, treat as attachment
                parse_payload(part, attachments)
    else:
        # Not multipart
        content_type = msg.get_content_type()
        if content_type == 'text/plain':
            body_parts['text/plain'].append(parse_payload(msg))
        elif content_type == 'text/html':
            body_parts['text/html'].append(parse_payload(msg))
        else:
            # Unknown content type, treat as attachment
            parse_payload(msg, attachments)
    
    # Join body parts
    for content_type in body_parts:
        body_parts[content_type] = '\n'.join(body_parts[content_type])
    
    return {
        'headers': headers,
        'body': body_parts,
        'attachments': attachments
    }
