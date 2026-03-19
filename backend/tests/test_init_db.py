from unittest.mock import patch

from init_db import run


def test_run_invokes_database_initialization():
    with patch("init_db.init_database") as init_database:
        run()

    init_database.assert_called_once_with()