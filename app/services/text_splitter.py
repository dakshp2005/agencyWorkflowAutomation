import re


class RecursiveCharacterTextSplitter:
    """Simple text splitter that mimics langchain's interface without heavy dependencies."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", ". ", " ", ""]

    def split_text(self, text: str) -> list:
        if not text:
            return []
        return self._recursive_split(text, self.separators)

    def _recursive_split(self, text: str, separators: list) -> list:
        if len(text) <= self.chunk_size:
            return [text.strip()] if text.strip() else []

        best_sep = ""
        for sep in separators:
            if sep in text:
                best_sep = sep
                break

        if not best_sep:
            chunks = []
            for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
                chunk = text[i:i + self.chunk_size].strip()
                if chunk:
                    chunks.append(chunk)
            return chunks

        parts = text.split(best_sep)
        chunks = []
        current = ""

        for part in parts:
            test = current + best_sep + part if current else part
            if len(test) <= self.chunk_size:
                current = test
            else:
                if current.strip():
                    chunks.append(current.strip())
                if len(part) > self.chunk_size:
                    sub_chunks = self._recursive_split(part, separators[1:] if len(separators) > 1 else [""])
                    chunks.extend(sub_chunks)
                    current = ""
                else:
                    current = part

        if current.strip():
            chunks.append(current.strip())

        if self.chunk_overlap > 0 and len(chunks) > 1:
            overlapped = [chunks[0]]
            for i in range(1, len(chunks)):
                prev_end = chunks[i - 1][-self.chunk_overlap:]
                overlapped.append(prev_end + chunks[i])
            chunks = overlapped

        return [c for c in chunks if c.strip()]
