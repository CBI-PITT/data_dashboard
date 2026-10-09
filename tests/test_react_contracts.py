"""Static contracts for the dashboard's spreadsheet data table.

React sources are not executed in this suite; these tests pin the source
contracts of the numiqo-style DataTable: progressive pages (offset/limit
POSTs to the rows endpoint), infinite scroll append, first-page debounce,
categorical/numeric type badges, live filter application (no Send needed),
and the plot placement (table is the central element until Send creates the
plot, then it moves below the plot).
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REACT_SRC = REPO_ROOT / "dashboard" / "src"
DATASET_JS = REACT_SRC / "pages" / "Dashboard" / "Component" / "dataset" / "Dataset.js"
DASHBOARD_JS = REACT_SRC / "pages" / "Dashboard" / "Dashboard.js"
FORM_JS = REACT_SRC / "pages" / "Dashboard" / "Component" / "form" / "Form.js"
DATA_TABLE_JS = (
    REACT_SRC / "pages" / "Dashboard" / "Component" / "table" / "DataTable.js"
)


def read(path):
    return Path(path).read_text()


# -- spreadsheet data table ---------------------------------------------------


def test_data_table_fetches_rows_progressively():
    """DataTable must POST one page at a time to the rows endpoint (offset/
    limit), encode the identifier, and use the config HOST (no hardcoded
    hosts)."""
    content = read(DATA_TABLE_JS)
    assert 'HOST + "/api/datasets/"' in content, "rows URL must compose from HOST"
    assert "encodeURIComponent(identifier)" in content
    assert '"/rows"' in content
    assert 'method' not in content or 'axios.post' in content
    assert "PAGE_SIZE" in content and "limit: PAGE_SIZE" in content
    assert "offset: offset" in content
    assert "/api/datasets/" not in content.replace(
        'HOST + "/api/datasets/"', ""
    ).replace('"', ""), "DataTable must not hardcode the API prefix"


def test_data_table_infinite_scroll_and_debounce():
    """Pages append on scroll (threshold + hasMore guard) and the first page
    is debounced because the continuous sliders fire onChange continuously."""
    content = read(DATA_TABLE_JS)
    assert "onScroll={handleScroll}" in content
    assert "SCROLL_THRESHOLD" in content
    assert "hasMore" in content
    assert "prev.concat(pageRows)" in content, "appended pages must concatenate"
    assert "FETCH_DEBOUNCE_MS" in content
    assert "setTimeout(" in content
    assert "clearTimeout(timer)" in content, "debounce timer must be cleaned up"


def test_data_table_type_badges_and_kind_mapping():
    """Column headers carry a categorical/numeric badge driven by the
    endpoint's kind field."""
    content = read(DATA_TABLE_JS)
    assert 'kind === "categorical"' in content
    assert "typeBadgeCategorical" in content
    assert "typeBadgeNumeric" in content
    assert ">abc</span>" in content, "categorical badge shows abc"
    assert ">123</span>" in content, "numeric badge shows 123"
    assert "Tooltip" in content
    # row-number column + zebra rows (spreadsheet look)
    assert "dataTableRowNumber" in content
    assert "dataTableRowOdd" in content
    assert "{rowIndex + 1}" in content


def test_dashboard_places_table_center_then_below_plot():
    """Dashboard.js must render the DataTable in the central Paper: hidden
    while the dataset form is still retrieving, visible once it arrives, and
    still below the plot after Send (displayData set). The Chart cover only
    shows when no dataset is selected or results exist."""
    content = read(DASHBOARD_JS)
    assert 'import DataTable from "./Component/table/DataTable";' in content
    assert 'const [selectedDataset, setSelectedDataset] = useState("");' in content
    assert "const [activeFilters, setActiveFilters] = useState(undefined);" in content
    assert (
        'formFrame !== undefined && formFrame !== "dataset retrieving" ? (\n'
        "              <DataTable" in content
    ), "table must wait for the fresh formFrame (no stale-filter fetch)"
    assert "identifier={selectedDataset}" in content
    assert "filters={activeFilters}" in content
    assert "formFrame === undefined || displayData !== undefined ? (" in content, (
        "the chart cover must only show with no dataset selected or results"
    )


def test_form_pushes_filters_up_immediately():
    """Form.js must push the current filter selections to the dashboard on
    every change so the table reflects them without Send."""
    content = read(FORM_JS)
    assert "setActiveFilters," in content
    assert "}, [formDataUpdated]);" in content, (
        "filters must be pushed on every formDataUpdated change"
    )
    push_at = content.find("setActiveFilters({")
    assert push_at != -1, "filter push missing"
    assert "categorical" in content[push_at:push_at + 400]
    assert "continuous" in content[push_at:push_at + 400]


def test_dataset_selection_flows_to_dashboard():
    """Dataset.js must lift the selected identifier (and clear it on delete)
    so the table can query the right dataset."""
    content = read(DATASET_JS)
    assert "setSelectedDataset" in content
    select_at = content.find("sessionStorage.setItem('INDEX', index);")
    assert select_at != -1, "index selection missing"
    after = content[select_at:select_at + 300]
    assert "setSelectedDataset(index)" in after, (
        "selection must be lifted on dataset change"
    )
    delete_at = content.find("sessionStorage.removeItem(\"INDEX\");")
    assert delete_at != -1
    after_delete = content[delete_at:delete_at + 300]
    assert 'setSelectedDataset("")' in after_delete, (
        "selection must clear when the selected dataset is deleted"
    )
