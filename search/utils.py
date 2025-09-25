from collections import defaultdict
from django.conf import settings
import json
import re

# CHUNK_SIZE = 1 * 1024      # 1KB chunks (For testing)
CHUNK_SIZE = 1024 * 1024   # 1MB chunks
OVERLAP_SIZE = 256         # overlap to avoid missing regex matches, need to handle duplicates
    
def run_search(pattern_str, uid):
    found_sequence_dict = defaultdict(list)

    file_name = f'sequence.fasta_{uid}.xml'
    file_path = f'{settings.BASE_DIR}/data/{file_name}'
    pattern = re.compile(pattern_str)
    
    with open(file_path, "r") as f:
        matches = list(stream_matches(f, pattern))
        for sequence, location in matches:
            found_sequence_dict[sequence].append(location)

    json_str = json.dumps(found_sequence_dict)
    return json_str

def stream_matches(file_obj, pattern):
    """
    Generator that streams regex matches from <TSeq_sequence> element.
    """
    inside_tseq_sequence = False
    buffer = ""
    offset = 0

    for line in file_obj:
        if "<TSeq_sequence>" in line:
            inside_tseq_sequence = True
            buffer += line.split("<TSeq_sequence>", 1)[1]
        elif "</TSeq_sequence>" in line and inside_tseq_sequence:
            buffer += line.split("</TSeq_sequence>", 1)[0]
            yield from find_matches(buffer, pattern, offset)
            offset += len(buffer)
            break
        elif inside_tseq_sequence:
            buffer += line
            while len(buffer) > CHUNK_SIZE:
                chunk = buffer[:CHUNK_SIZE]
                yield from find_matches(chunk, pattern, offset)
                buffer = buffer[CHUNK_SIZE - OVERLAP_SIZE:]
                offset += (len(chunk) - OVERLAP_SIZE)

    if buffer:
        yield from find_matches(buffer, pattern, offset)

def find_matches(text, pattern, offset):
    """
    Apply regex to a text buffer and yield all matches.
    """
    
    for match in pattern.finditer(text):
        matched_str = match.group()
        span = match.span()
        location = (span[0] + offset, span[1] + offset - 1)

        # Matches end inside the overlay area are duplicates, ignores them
        # Matches end after the overlay area are new ones
        if location[1] >= offset + OVERLAP_SIZE:
            yield (matched_str, location)