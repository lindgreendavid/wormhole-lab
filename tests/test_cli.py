import json
import subprocess
import sys

from wormhole_lab.cli import main


def test_cli_prints_valid_json(capsys, monkeypatch):
    monkeypatch.setattr(
        sys, "argv", ["wormhole-lab", "--r0", "2.0", "--n", "1.0", "--redshift", "inverse"]
    )
    main()
    payload = json.loads(capsys.readouterr().out)
    assert payload["r0"] == 2.0
    assert payload["n"] == 1.0
    assert payload["redshift"] == "inverse"


def test_cli_subprocess_smoke_test():
    result = subprocess.run(
        [sys.executable, "-m", "wormhole_lab.cli", "--r0", "2.0", "--n", "1.0"],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert payload["r0"] == 2.0
    assert payload["n"] == 1.0
