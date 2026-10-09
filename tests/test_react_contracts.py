"""Static contracts for the dashboard's spreadsheet data table and the
"Add dataset" file-browser picker.

React sources are not executed in this suite; these tests pin the source
contracts of the numiqo-style DataTable (progressive pages via offset/limit
POSTs to the rows endpoint, infinite scroll append, first-page debounce,
categorical/numeric type badges, live filter application without Send, plot
placement below the table) and the Add-dataset dialog (wired to the
flask_file_browser embed, ?picker=0 hides the dead-end Select buttons,
dataset-list refresh on close).
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REACT_SRC = REPO_ROOT / "dashboard" / "src"
PATH_JS = REACT_SRC / "config" / "path.js"
DATASET_JS = REACT_SRC / "pages" / "Dashboard" / "Component" / "dataset" / "Dataset.js"
DASHBOARD_JS = REACT_SRC / "pages" / "Dashboard" / "Dashboard.js"
FORM_JS = REACT_SRC / "pages" / "Dashboard" / "Component" / "form" / "Form.js"
DATA_TABLE_JS = (
    REACT_SRC / "pages" / "Dashboard" / "Component" / "table" / "DataTable.js"
)
COLUMN_STATS_JS = (
    REACT_SRC / "pages" / "Dashboard" / "Component" / "table" / "ColumnStats.js"
)
GROUP_BY_JS = REACT_SRC / "pages" / "Dashboard" / "Component" / "form" / "Get_groupBy.js"
FIELD_JS = REACT_SRC / "pages" / "Dashboard" / "Component" / "form" / "Get_field.js"


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
    # order: the table renders above the plot (plot appears below the table)
    table_at = content.find("<DataTable\n                identifier=")
    chart_at = content.find("<Chart\n                displayData=")
    assert table_at != -1 and chart_at != -1, "both central children must render"
    assert table_at < chart_at, "the plot must render below the data table"


def test_reset_clears_the_plot():
    """Form.js handleReset must clear displayData so Chart/MetricsTool
    unmount and the data table returns to the top of the central component."""
    content = read(FORM_JS)
    reset_at = content.find("const handleReset = () => {")
    assert reset_at != -1, "handleReset missing"
    body = content[reset_at:reset_at + 900]
    assert "setDisplayData(undefined);" in body, (
        "Reset must clear the plot (displayData)"
    )
    assert 'type="reset"' in content, "the Reset button must be a reset-type submit"


# -- left column card split (Filter Settings / Plot Settings) ------------------


def test_form_splits_into_two_cards():
    """Form.js must render two separate cards: Filter Settings (filters) and
    Plot Settings (group-by/field/aggregation). The form element that owns
    the submit must be the Plot Settings card; the cards must not be
    fixed-height boxes (they grow and the page scrolls)."""
    content = read(FORM_JS)
    assert "<Typography variant=\"h6\">Filter Settings</Typography>" in content
    assert "<Typography variant=\"h6\">Plot Settings</Typography>" in content
    # structure: [Filter title, GetFilterList, filters] then the form element
    # (plot card) opens, then the Plot Settings title, GetGroupBy, Send
    filter_at = content.find("Filter Settings</Typography>")
    assert filter_at != -1
    assert content.find('component="form"', 0, filter_at) == -1, (
        "the Filter Settings card must be a plain Paper"
    )
    form_at = content.find('component="form"')
    assert form_at != -1 and form_at > filter_at, (
        "the form element must live on the Plot Settings card"
    )
    plot_at = content.find("Plot Settings</Typography>")
    assert plot_at > form_at, "the Plot Settings title must be inside the form card"
    assert content.find("<GetFilterList") < form_at, (
        "filters must render in the first card"
    )
    submit_at = content.find('type="submit"', plot_at)
    assert submit_at != -1, "Send must live on the Plot Settings card"
    assert "maxHeight" not in content, (
        "the form cards must grow (no fixed-height boxes; page scrolls)"
    )


def test_groupby_and_field_renamed_x_y():
    """GroupBy is renamed X and Field is renamed Y; the payload keys
    (group_by / field) stay unchanged for the backend contract."""
    group_content = read(GROUP_BY_JS)
    assert ">X</InputLabel>" in group_content
    assert '<OutlinedInput label="X" />' in group_content
    assert "name='group_by'" in group_content, "payload key must stay group_by"
    field_content = read(FIELD_JS)
    assert ">Y</InputLabel>" in field_content
    assert 'label="Y"' in field_content
    assert 'name="field"' in field_content, "payload key must stay field"


# -- column statistics (numiqo-style column picker) ----------------------------


def test_column_stats_chips_colored_by_type_and_toggle():
    """ColumnStats renders all column names as type-colored chips below the
    table; clicking the selected chip again hides the stats."""
    content = read(COLUMN_STATS_JS)
    assert "columnChipCategorical" in content
    assert "columnChipNumeric" in content
    assert "columnChipDate" in content
    assert 'kind === "categorical"' in content
    assert 'kind === "date"' in content
    assert "columnChipSelected" in content, "selected chip must be highlighted"
    assert "handleChipClick" in content
    toggle_at = content.find("if (selected === column) {")
    assert toggle_at != -1, "clicking the selected chip again must hide"
    after = content[toggle_at:toggle_at + 400]
    assert "setSelected(null)" in after and "setStats(null)" in after


def test_column_stats_fetches_per_column():
    """Clicking a chip POSTs to the column_stats endpoint with the column
    name, encoding the identifier and using the config HOST."""
    content = read(COLUMN_STATS_JS)
    assert 'HOST + STATS_URL' in content, "URL must compose from HOST"
    assert 'const STATS_URL = "/api/datasets/";' in content
    assert 'encodeURIComponent(identifier) + "/column_stats"' in content
    assert "{ column: column }" in content
    assert "/api/datasets/" not in content.replace(
        'const STATS_URL = "/api/datasets/";', ""
    ).replace('HOST + STATS_URL', ""), "ColumnStats must not hardcode the prefix"


def test_column_stats_labels():
    """Numeric columns report min/max/mean/median/quantiles/std; categorical
    columns report a Value/Occurrences/Fraction frequency table."""
    content = read(COLUMN_STATS_JS)
    for label in ("Minimum", "Maximum", "Mean", "Median", "25% quantile",
                  "75% quantile", "Standard deviation"):
        assert label in content, f"numeric label missing: {label}"
    assert 'kind === "numeric"' in content
    assert 'kind === "categorical"' in content
    for label in ("Value", "Occurrences", "Fraction"):
        assert label in content, f"categorical label missing: {label}"


def test_data_table_renders_column_stats_below():
    """DataTable imports ColumnStats and renders it after the rows table."""
    content = read(DATA_TABLE_JS)
    assert 'import ColumnStats from "./ColumnStats";' in content
    assert "<ColumnStats identifier={identifier} columns={columns} />" in content
    container_at = content.find('className="dataTableContainer"')
    stats_at = content.find("<ColumnStats")
    assert container_at != -1 and stats_at != -1
    assert container_at < stats_at, "stats must render below the rows table"


def test_central_component_not_height_limited():
    """The central Paper must grow with its content and scroll: .chart carries
    max-height, not a fixed height."""
    content = read(REPO_ROOT / "dashboard" / "src" / "pages" / "Dashboard" / "Dashboard.css")
    chart_at = content.find(".chart {")
    assert chart_at != -1
    block = content[chart_at:chart_at + 300]
    assert "max-height:" in block, ".chart must use max-height"
    assert "height: 80vh" not in block, ".chart must not be a fixed-height box"
    assert "overflow-y: auto" in block, ".chart must scroll"


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


# -- "Add dataset" file-browser picker ----------------------------------------


def test_path_js_exports_browser_embed_url():
    """The embed URL must point at the chrome-less browser embed with the
    picker flag that hides the dead-end Select buttons."""
    content = read(PATH_JS)
    assert "BROWSER_EMBED_URL" in content, "BROWSER_EMBED_URL export missing"
    assert "'/browser/dir_embed/?picker=0'" in content, (
        "embed URL must target /browser/dir_embed/ with ?picker=0"
    )
    assert "export { BROWSER_EMBED_URL }" in content


def test_dataset_js_button_and_dialog_contracts():
    """Dataset.js must render the Add dataset trigger and the full-width
    keepMounted dialog that hosts the browser iframe."""
    content = read(DATASET_JS)
    # the trigger button sits in the dataset-panel header row
    assert 'aria-label="Add dataset from file browser"' in content
    assert '"Add dataset from file browser"' in content  # tooltip
    assert "AddCircleOutlineIcon" in content
    assert "setAddOpen(true)" in content
    # the dialog hosts the iframe, stays mounted to keep the last folder
    for contract in (
        'open={addOpen}',
        'onClose={() => {',
        "maxWidth=\"xl\"",
        "fullWidth",
        "\n        keepMounted\n",  # JSX attribute, not a comment mention
        "<DialogTitle>Add dataset</DialogTitle>",
        'src={addFrameSrc}',
        'title="File browser"',
        "70vh",
    ):
        assert contract in content, f"Dataset.js lost dialog contract: {contract}"


def test_dataset_js_uses_config_url_and_refreshes_on_close():
    """The iframe URL must come from config/path.js (no hardcoded hosts) and
    the dataset list must refresh when the dialog closes (a same-tab modal
    never fires the visibilitychange listener)."""
    content = read(DATASET_JS)
    assert 'import HOST, { BROWSER_EMBED_URL } from "../../../../config/path";' in content
    assert "setAddFrameSrc(BROWSER_EMBED_URL)" in content, (
        "iframe src must be set from the config constant"
    )
    close_at = content.find("onClose={() => {")
    assert close_at != -1, "dialog onClose missing"
    fetch_at = content.find("fetchIndices();", close_at)
    assert fetch_at != -1, "dataset list must refresh when the dialog closes"
    assert "/browser/dir_embed/" not in content, (
        "Dataset.js must not hardcode the embed URL; it comes from config/path.js"
    )
