from datetime import datetime
from pathlib import Path
import sys
import types

sys.path.append(str(Path(__file__).resolve().parent.parent))

requests_module = types.ModuleType("requests")
requests_module.Session = lambda *args, **kwargs: None

adapters_module = types.ModuleType("requests.adapters")

class HTTPAdapter:  # minimal stub for subclassing
    pass

adapters_module.HTTPAdapter = HTTPAdapter

sys.modules["requests"] = requests_module
sys.modules["requests.adapters"] = adapters_module

import v75


def test_list_v75_dates_only_saturdays(monkeypatch, capsys):
    class FixedDatetime(datetime):
        @classmethod
        def now(cls):
            return cls(2024, 1, 1)

    monkeypatch.setattr(v75, "datetime", FixedDatetime)

    v75.list_v75_dates_for_year()
    output_lines = capsys.readouterr().out.splitlines()

    date_lines = [line[2:] for line in output_lines if line.startswith("- ")]
    for date_str in date_lines:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        assert dt.weekday() == 5
