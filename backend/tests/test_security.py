import unittest
from fastapi import HTTPException
from app.services.security import create_token, verify_token


class SecurityTests(unittest.TestCase):
    def test_signed_token_round_trip(self):
        token = create_token(12, False)
        self.assertEqual(verify_token(token)["sub"], "12")

    def test_tampered_token_is_rejected(self):
        with self.assertRaises(HTTPException):
            verify_token("tampered.token")


if __name__ == "__main__":
    unittest.main()
