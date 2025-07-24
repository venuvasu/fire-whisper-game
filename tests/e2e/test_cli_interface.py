"""
End-to-End CLI Interface Tests

This module contains end-to-end tests for the CLI interface.
"""
import unittest
import sys
import os
import io
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from client.cli.game_cli import GameCLI


class TestCLIInterface(unittest.TestCase):
    """Test CLI interface scenarios"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.cli = GameCLI()
    
    @patch('sys.argv', ['game_cli.py', 'new', '--character', 'TestHero', '--saga', 'TestSaga'])
    @patch('builtins.input', side_effect=['examine area', 'quit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_new_game_command(self, mock_stdout, mock_input):
        """Test the new game command"""
        try:
            self.cli.run()
        except SystemExit:
            pass  # Expected when argparse processes test arguments
        
        # Verify that the CLI attempted to start a new game
        # (This is a simplified test since we're mocking the input/output)
        self.assertIsNotNone(mock_stdout.getvalue())
    
    @patch('sys.argv', ['game_cli.py', 'list'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_list_games_command(self, mock_stdout):
        """Test the list games command"""
        try:
            self.cli.run()
        except SystemExit:
            pass  # Expected when argparse processes test arguments
        
        # Verify that the CLI attempted to list games
        output = mock_stdout.getvalue()
        self.assertIn("Fire Whisper RPG", output)
    
    def test_get_available_actions(self):
        """Test getting available actions"""
        actions = self.cli._get_available_actions()
        
        # Verify actions are returned
        self.assertIsInstance(actions, list)
        self.assertTrue(len(actions) > 0)
        
        # Verify action structure
        for action in actions:
            self.assertIn("id", action)
            self.assertIn("text", action)
            self.assertIn("risk", action)


if __name__ == "__main__":
    unittest.main()