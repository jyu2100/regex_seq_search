from collections import defaultdict
from django.conf import settings
from stegano import lsb
import re

# CHUNK_SIZE = 1 * 1024      # 1KB chunks (For testing)
CHUNK_SIZE = 1024 * 1024   # 1MB chunks
OVERLAP_SIZE = 256         # overlap to avoid missing regex matches, need to handle duplicates
    
def run_search(pattern_str, uid):
    found_sequence_dict = defaultdict(list)

    file_name = f"sequence.fasta_{uid}.xml"
    file_path = f"{settings.BASE_DIR}/data/{file_name}"

    # Compiles the regular expression pattern as it will be used multilpe times, 
    # also assumes the pattern and searched data are all in uppercase.
    # pattern = re.compile(pattern_str, re.IGNORECASE)
    pattern = re.compile(pattern_str)
    
    with open(file_path, "r") as f:
        matches = list(stream_matches(f, pattern))
        for sequence, location in matches:
            found_sequence_dict[sequence].append(location)

    return found_sequence_dict

def stream_matches(file_obj, pattern):
    """
    Generator that streams regex matches from <TSeq_sequence> element.
    """
    inside_tseq_sequence = False
    buffer = ""
    offset = 0

    opening_tag = "<TSeq_sequence>"
    closing_tag = "</TSeq_sequence>"
    tag_overlay_size = len(opening_tag)

    while True:
        file_chunk = file_obj.read(CHUNK_SIZE)
        if not file_chunk:
            break

        buffer += file_chunk

        if not inside_tseq_sequence:
            # Look for opening tag
            start_idx = buffer.find(opening_tag)
            if start_idx == -1:
                # keep the last tag_overlay_size part in case tag is split across chunks
                buffer = buffer[-tag_overlay_size:]
                continue

            buffer = buffer[start_idx + len(opening_tag):]
            inside_tseq_sequence = True

        if inside_tseq_sequence:
            # Look for closing tag
            end_idx = buffer.find(closing_tag)
            if end_idx == -1:
                while len(buffer) > CHUNK_SIZE:
                    chunk = buffer[:CHUNK_SIZE]
                    yield from find_matches(chunk, pattern, offset)
                    offset += CHUNK_SIZE - OVERLAP_SIZE
                    buffer = buffer[CHUNK_SIZE - OVERLAP_SIZE:]

                continue
            else:
                # Found closing tag
                chunk = buffer[:end_idx]
                yield from find_matches(chunk, pattern, offset)
                return

def find_matches(chunk, pattern, offset):
    """
    Apply regex to a text buffer and yield all matches.
    """
    
    for match in pattern.finditer(chunk):
        matched_str = match.group()
        span = match.span()
        location = (span[0] + offset, span[1] + offset - 1)

        # Matches end inside the overlay area are duplicates, ignores them except for the first chunk
        # Matches end after the overlay area are new ones
        if offset == 0 or location[1] >= offset + OVERLAP_SIZE:
            yield (matched_str, location)

def embed_value(input_image, output_image, value):
    """
    Embed a string value into an image.
    """
    secret_image = lsb.hide(input_image, value)
    secret_image.save(output_image)

def extract_value(image):
    """
    Extract a string value embedded in an image.
    """
    revealed_str = lsb.reveal(image)

    if not revealed_str:
        return None

    return revealed_str
