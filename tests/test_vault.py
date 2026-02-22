# Mock is used as the test runs fast with the mocker.
# Better to do this than test the DB as we are testing the connection to the SQL.
import pytest
from unittest.mock import MagicMock
from counter.views import get_value_matches

def test_get_value_matches_logic(mocker):
    """Create a fake database connection and cursor."""

    #Create the mocks.
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # We make execute() return the cursor.
    # we make the fetchall() return our data.
    mock_conn.execute.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(
        'python', 'Greek', 'Greece', 39.0, 22.0, 'Named after a serpent.'
    )]
    # Handle the 'with' statement.
    mock_conn.__enter__.return_value = mock_conn

    # Use mocker.patch - to swap the real Duckdb connect with our fake one.
    mocker.patch('counter.views.duckdb.connect', return_value=mock_conn)

    # Run the function with a test word.
    result = get_value_matches(['python'])

    # Assertions: Check if the function turned the raw tuple into a dictionary.
    assert len(result) == 1
    assert result[0]['word'] == 'python'
    assert result[0]['country'] == 'Greece'
    assert result[0]['lat'] == 39.0
    assert result[0]['fact'] == 'Named after a serpent.'

    # Verify that the actual DB was called with the right SQL.
    mock_conn.execute.assert_called_once()

