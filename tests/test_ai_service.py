import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.modules.setdefault("openai", MagicMock())

from services.ai_service import AIServiceError, _recent_messages, generate_reply


class AIServiceTests(unittest.TestCase):
    def test_recent_messages_keeps_the_latest_twenty(self):
        messages = [{"role": "user", "content": str(index)} for index in range(25)]

        result = _recent_messages(messages)

        self.assertEqual(len(result), 20)
        self.assertEqual(result[0]["content"], "5")

    def test_missing_api_key_has_clear_error(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(AIServiceError, "Missing OPENAI_API_KEY"):
                generate_reply([])


if __name__ == "__main__":
    unittest.main()
