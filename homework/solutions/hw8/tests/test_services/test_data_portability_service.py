import pytest
from unittest.mock import MagicMock, patch
from solution.services.data_portability_service import DataPortabilityService
from solution.models.account import Account
from solution.models.categories import Category
from solution.models.transaction import Transaction
from solution.models.transfer import Transfer

EXPORT_ZIP_FILE_NAME = "data.zip"

def test_export_success():
    mock_account = MagicMock()
    mock_category = MagicMock()
    mock_transaction = MagicMock()
    mock_transfer = MagicMock()

    service = DataPortabilityService(
        mock_account,
        mock_category,
        mock_transaction,
        mock_transfer,
    )

    with patch("os.path.exists", return_value=True):
        with patch("zipfile.ZipFile.write") as mock_write:
            result = service.export()

            assert result == EXPORT_ZIP_FILE_NAME
            assert mock_write.call_count == 4


def test_export_missing_file():
    mock_account_repo = MagicMock()
    mock_category_repo = MagicMock()
    mock_transaction_repo = MagicMock()
    mock_transfer_repo = MagicMock()

    service = DataPortabilityService(
        mock_account_repo,
        mock_category_repo,
        mock_transaction_repo,
        mock_transfer_repo,
    )

    with patch("os.path.exists", return_value=False):
        with pytest.raises(ValueError, match="Missing file"):
            service.export()
            
def test_import_zip_not_exists():

    mock_account = MagicMock()
    mock_category = MagicMock()
    mock_transaction = MagicMock()
    mock_transfer = MagicMock()

    service = DataPortabilityService(
        mock_account,
        mock_category,
        mock_transaction,
        mock_transfer,
    )

    with patch("os.path.exists", return_value=False):
        with pytest.raises(ValueError, match="Zip file does not exist"):
            service.import_from_zip("fake.zip")
            
def test_validate_import_files_missing_file():

    service = DataPortabilityService(
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )

    with patch("os.path.exists", return_value=False):
        with pytest.raises(ValueError, match="Missing required file"):
            service.validate_import_files("test_path")