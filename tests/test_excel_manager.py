"""Tests for Excel project codes management."""

from pathlib import Path

import pytest
from openpyxl import Workbook

from corp_opportunity_manager.excel_manager import (
    find_row_by_client,
    list_projects,
    update_folder_link,
)


@pytest.fixture
def sample_excel(tmp_path: Path) -> Path:
    """Create a sample project_codes.xlsx."""
    wb = Workbook()
    ws = wb.active
    ws.append(["Project Name", "Client", "Product", "Stage", "Folder Link"])
    ws.append(["Lenzing IBP", "Lenzing", "Planning", "discovery", ""])
    ws.append(["Honda WMS", "Honda", "WMS", "rfp", ""])
    ws.append(["BMW TMS", "BMW", "TMS", "proposal", "C:\\projects\\BMW_TMS"])

    path = tmp_path / "project_codes.xlsx"
    wb.save(path)
    wb.close()
    return path


def test_find_row_by_client(sample_excel: Path):
    row = find_row_by_client(sample_excel, "Lenzing")
    assert row is not None
    assert row.client == "Lenzing"
    assert row.product == "Planning"
    assert row.row_number == 2


def test_find_row_by_client_case_insensitive(sample_excel: Path):
    row = find_row_by_client(sample_excel, "honda")
    assert row is not None
    assert row.client == "Honda"


def test_find_row_by_client_not_found(sample_excel: Path):
    row = find_row_by_client(sample_excel, "Nonexistent")
    assert row is None


def test_find_row_missing_file(tmp_path: Path):
    row = find_row_by_client(tmp_path / "nope.xlsx", "Test")
    assert row is None


def test_update_folder_link(sample_excel: Path):
    success = update_folder_link(sample_excel, 2, "C:\\projects\\Lenzing_Planning")
    assert success

    row = find_row_by_client(sample_excel, "Lenzing")
    assert row is not None
    assert row.folder_link == "C:\\projects\\Lenzing_Planning"


def test_list_projects(sample_excel: Path):
    rows = list_projects(sample_excel)
    assert len(rows) == 3
    clients = {r.client for r in rows}
    assert clients == {"Lenzing", "Honda", "BMW"}


def test_list_projects_missing_file(tmp_path: Path):
    rows = list_projects(tmp_path / "nope.xlsx")
    assert rows == []
