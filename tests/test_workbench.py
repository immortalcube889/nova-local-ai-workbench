import json
import tempfile
import unittest
from pathlib import Path

from nova_workbench.storage import MemoryStore
from nova_workbench.tools import plan_file_action


class WorkbenchTests(unittest.TestCase):
    def test_memory_is_persistent_and_searchable(self):
        with tempfile.TemporaryDirectory() as folder:
            store = MemoryStore(Path(folder) / "memory.sqlite3")
            item = store.add("Nova uses an inspectable SQLite memory store.")
            self.assertEqual(item["id"], 1)
            self.assertEqual(store.search("SQLite")[0]["id"], 1)

    def test_file_tool_only_plans_an_action(self):
        result = plan_file_action("write", "~/example.txt")
        self.assertEqual(result["status"], "approval_required")
        self.assertNotIn("executed", result)

    def test_invalid_memory_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                MemoryStore(Path(folder) / "memory.sqlite3").add("")


if __name__ == "__main__":
    unittest.main()
