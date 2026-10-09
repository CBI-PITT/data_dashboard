"""Static contracts for the dashboard's "Add dataset" file-browser picker.

React sources are not executed in this suite; these tests pin the source
contracts that keep the Add-dataset dialog wired to the flask_file_browser
embed (same route the PEACE form picker uses, ?picker=0 hides the dead-end
Select File/Folder buttons) and the dataset-list refresh on close.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REACT_SRC = REPO_ROOT / "dashboard" / "src"
PATH_JS = REACT_SRC / "config" / "path.js"
DATASET_JS = REACT_SRC / "pages" / "Dashboard" / "Component" / "dataset" / "Dataset.js"


def read(path):
    return Path(path).read_text()


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
