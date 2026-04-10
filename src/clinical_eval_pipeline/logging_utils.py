from __future__ import annotations

import sys
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Generator


class _TeeStream:
    def __init__(self, stream_a, stream_b) -> None:
        self.stream_a = stream_a
        self.stream_b = stream_b
        self._at_line_start = True

    @staticmethod
    def _ts_prefix() -> str:
        return f"[{datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}] "

    def write(self, data) -> int:
        if isinstance(data, bytes):
            text = data.decode("utf-8", errors="replace")
        else:
            text = str(data)

        chunks = text.splitlines(keepends=True)
        if not chunks:
            return 0

        rendered: list[str] = []
        for chunk in chunks:
            if self._at_line_start and chunk != "":
                rendered.append(self._ts_prefix())
            rendered.append(chunk)
            self._at_line_start = chunk.endswith("\n")

        out = "".join(rendered)
        self.stream_a.write(out)
        self.stream_b.write(out)
        return len(text)

    def flush(self) -> None:
        self.stream_a.flush()
        self.stream_b.flush()


@contextmanager
def tee_terminal_to_log(output_dir: str | Path, log_subdir: str, command_line: str) -> Generator[Path, None, None]:
    out_dir = Path(output_dir)
    logs_dir = out_dir / log_subdir
    logs_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    log_path = logs_dir / f"pipeline_{ts}.log"

    original_stdout = sys.stdout
    original_stderr = sys.stderr
    with log_path.open("w", encoding="utf-8") as log_file:
        sys.stdout = _TeeStream(original_stdout, log_file)
        sys.stderr = _TeeStream(original_stderr, log_file)
        print(f"[pipeline] log_file={log_path}", flush=True)
        print(f"[pipeline] command={command_line}", flush=True)
        print(f"[pipeline] started_utc={datetime.now(UTC).isoformat()}", flush=True)
        try:
            yield log_path
        finally:
            print(f"[pipeline] finished_utc={datetime.now(UTC).isoformat()}", flush=True)
            sys.stdout.flush()
            sys.stderr.flush()
            sys.stdout = original_stdout
            sys.stderr = original_stderr
