import re


class StackTraceExtractor:
    _exception = re.compile(r"^([\w.]+(?:Error|Exception|Fault|Timeout)): (.+)$", re.MULTILINE)

    def extract(self, trace: str | None) -> dict[str, object]:
        if not trace:
            return {"exception": None, "message": None, "frames": []}
        matches = self._exception.findall(trace)
        frames = re.findall(r'File "([^"]+)", line (\d+), in ([^\n]+)', trace)
        return {"exception": matches[-1][0] if matches else "UnhandledException",
                "message": matches[-1][1] if matches else trace.splitlines()[-1],
                "frames": [{"file": path, "line": int(line), "function": func} for path, line, func in frames]}
