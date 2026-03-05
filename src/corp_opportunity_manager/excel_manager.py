"""Read and update project_codes.xlsx — find rows, add folder links."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from openpyxl import load_workbook

logger = logging.getLogger(__name__)


@dataclass
class ProjectRow:
    """A row from the project codes spreadsheet."""

    row_number: int
    project_name: str
    client: str
    product: str
    stage: str
    folder_link: str


def find_row_by_client(excel_path: Path, client: str) -> ProjectRow | None:
    """Find the first row matching the client name (case-insensitive).

    Assumes columns: A=Project Name, B=Client, C=Product, D=Stage, E=Folder Link.
    Skips the header row (row 1).
    """
    if not excel_path.exists():
        logger.warning("Excel file not found: %s", excel_path)
        return None

    wb = load_workbook(excel_path, read_only=True)
    ws = wb.active

    client_lower = client.lower()
    for row in ws.iter_rows(min_row=2, values_only=False):
        # Column B = Client
        cell_value = row[1].value
        if cell_value and str(cell_value).strip().lower() == client_lower:
            return ProjectRow(
                row_number=row[0].row,
                project_name=str(row[0].value or ""),
                client=str(row[1].value or ""),
                product=str(row[2].value or ""),
                stage=str(row[3].value or ""),
                folder_link=str(row[4].value or ""),
            )
    wb.close()
    return None


def update_folder_link(excel_path: Path, row_number: int, folder_path: str) -> bool:
    """Set the folder link (column E) for a given row.

    Returns True if the update succeeded.
    """
    if not excel_path.exists():
        logger.error("Excel file not found: %s", excel_path)
        return False

    wb = load_workbook(excel_path)
    ws = wb.active
    ws.cell(row=row_number, column=5, value=folder_path)
    wb.save(excel_path)
    wb.close()
    logger.info("Updated row %d with folder link: %s", row_number, folder_path)
    return True


def list_projects(excel_path: Path) -> list[ProjectRow]:
    """Read all project rows from the spreadsheet."""
    if not excel_path.exists():
        logger.warning("Excel file not found: %s", excel_path)
        return []

    wb = load_workbook(excel_path, read_only=True)
    ws = wb.active
    rows: list[ProjectRow] = []

    for row in ws.iter_rows(min_row=2, values_only=False):
        if row[0].value is None:
            continue
        rows.append(
            ProjectRow(
                row_number=row[0].row,
                project_name=str(row[0].value or ""),
                client=str(row[1].value or ""),
                product=str(row[2].value or ""),
                stage=str(row[3].value or ""),
                folder_link=str(row[4].value or ""),
            )
        )

    wb.close()
    return rows
