import os
import sys
import types

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

requests_stub = types.ModuleType("requests")
adapters_stub = types.ModuleType("requests.adapters")

class HTTPAdapter:  # minimal stub for import
    pass


class Session:  # minimal stub for import
    def mount(self, *args, **kwargs):
        pass


requests_stub.Session = Session
adapters_stub.HTTPAdapter = HTTPAdapter
requests_stub.adapters = adapters_stub
sys.modules["requests"] = requests_stub
sys.modules["requests.adapters"] = adapters_stub

from v75 import display_races_and_horses


def test_display_races_and_horses_includes_trainer(capsys):
    races = [
        {
            "scheduledStartTime": "2023-01-01T12:00:00",
            "id": "race1",
            "number": 1,
            "name": "Test Race",
            "starts": [
                {
                    "number": 1,
                    "horse": {
                        "name": "Speedster",
                        "id": 1,
                        "pedigree": {"father": {"nationality": "US"}},
                    },
                    "driver": {"firstName": "John", "lastName": "Doe"},
                    "trainer": {"firstName": "Jane", "lastName": "Smith"},
                }
            ],
        }
    ]

    display_races_and_horses(races)
    captured = capsys.readouterr()
    assert "Trainer: Jane Smith" in captured.out
