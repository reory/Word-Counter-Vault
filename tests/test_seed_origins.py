from unittest.mock import MagicMock, mock_open, patch

from counter.services.seed_origins import seed_vault


@patch("counter.services.seed_origins.os.path.exists")
def test_seed_vault_missing_json_file(mock_exists, capsys):
    """Verify seeding exits gracefully when the JSON file is missing."""

    mock_exists.return_value = False

    seed_vault()

    captured = capsys.readouterr()

    assert "Could not find" in captured.out


@patch("counter.services.seed_origins.duckdb.connect")
@patch("counter.services.seed_origins.json.load")
@patch("builtins.open", new_callable=mock_open)
@patch("counter.services.seed_origins.os.path.exists")
def test_seed_vault_success(
    mock_exists,
    mock_file,
    mock_json_load,
    mock_connect,
    capsys,
):
    """Verify data is loaded and inserted into DuckDB."""

    mock_exists.return_value = True

    mock_json_load.return_value = {
        "hubs": [
            {
                "origin": "Latin",
                "country": "Italy",
                "lat": 41.9,
                "lng": 12.5,
                "fact": "Historical language",
                "words": ["Python", "Code"],
            }
        ]
    }

    mock_connection = MagicMock()

    count_result = MagicMock()
    count_result.fetchone.return_value = [2]

    mock_connection.execute.return_value = count_result
    mock_connect.return_value = mock_connection

    seed_vault()

    mock_connect.assert_called_once()

    mock_connection.executemany.assert_called_once()

    inserted_rows = mock_connection.executemany.call_args[0][1]

    assert (
        "python",
        "Latin",
        "Italy",
        41.9,
        12.5,
        "Historical language",
    ) in inserted_rows

    assert (
        "code",
        "Latin",
        "Italy",
        41.9,
        12.5,
        "Historical language",
    ) in inserted_rows

    mock_connection.close.assert_called_once()

    captured = capsys.readouterr()
    assert "Database now contains 2 words" in captured.out