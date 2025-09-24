from collections import defaultdict
from django.conf import settings
# from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import re

# Front-end view
# @login_required
def home(request):
    return render(request, "search/home.html")

# API View
class RegexSearchView(APIView):
    # CHUNK_SIZE = 1 * 1024      # 1KB chunks (For testing)
    CHUNK_SIZE = 1024 * 1024   # 1MB chunks
    OVERLAP_SIZE = 100         # overlap to avoid missing regex matches, need to handle duplicates
    
    def get(self, request):
        pattern_str = request.query_params.get("pattern")
        uid = request.query_params.get("uid")
        found_sequence_dict = defaultdict(list)

        try:
            file_name = f'sequence.fasta_{uid}.xml'
            file_path = f'{settings.BASE_DIR}/data/{file_name}'
            pattern = re.compile(pattern_str)
            
            with open(file_path, "r") as f:
                matches = list(self._stream_matches(f, pattern))
                for sequence, location in matches:
                    found_sequence_dict[sequence].append(location)

            json_str = json.dumps(found_sequence_dict)
            return Response(json_str)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
    def _stream_matches(self, file_obj, pattern):
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
                yield from self._find_matches(buffer, pattern, offset)
                offset += len(buffer)
                break
            elif inside_tseq_sequence:
                buffer += line
                while len(buffer) > self.CHUNK_SIZE:
                    chunk = buffer[:self.CHUNK_SIZE]
                    yield from self._find_matches(chunk, pattern, offset)
                    buffer = buffer[self.CHUNK_SIZE - self.OVERLAP_SIZE:]
                    offset += (len(chunk) - self.OVERLAP_SIZE)

        if buffer:
            yield from self._find_matches(buffer, pattern, offset)

    def _find_matches(self, text, pattern, offset):
        """
        Apply regex to a text buffer and yield all matches.
        """
        
        for match in pattern.finditer(text):
            matched_str = match.group()
            span = match.span()
            location = (span[0] + offset, span[1] + offset - 1)
            yield (matched_str, location)
