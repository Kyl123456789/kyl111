import json
import subprocess
import sys
from pathlib import Path


def test_run_placeholder(tmp_path, monkeypatch):
    """Run the placeholder script and check output format."""
    # Create input file
    input_file = tmp_path / "in.txt"
    input_file.write_text("testing123", encoding="utf-8")

    output_file = tmp_path / "out.jsonl"

    # Run script as subprocess to emulate normal usage
    proc = subprocess.run([sys.executable, str(Path(__file__).parent.parent / "run_so101.py"),
                           "--input", str(input_file),
                           "--output", str(output_file)], capture_output=True, text=True)
    assert proc.returncode == 0
    assert output_file.exists()

    text = output_file.read_text(encoding="utf-8").strip()
    data = json.loads(text)
    assert "output" in data
    # The placeholder reverses the string
    assert data["output"] == "321gnitset"
