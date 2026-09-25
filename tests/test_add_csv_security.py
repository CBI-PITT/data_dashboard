"""Security tests for the add-to-dashboard endpoint: login enforcement, CSV
validation, and browsable-root containment."""

import os

import pytest

from data_dashboard.utils import (
    browsable_roots,
    csv_within_allowed_roots,
    sanitize_dataset_name,
)


@pytest.fixture()
def allowed_root(tmp_path, monkeypatch):
    root = tmp_path / "roots"
    root.mkdir()
    monkeypatch.setattr(
        "data_dashboard.utils.browsable_roots", lambda settings: [str(root)])
    return root


def test_inside_root_allowed(allowed_root):
    csv_file = allowed_root / "cells.csv"
    csv_file.write_text("a,b\n1,2\n")
    assert csv_within_allowed_roots(None, str(csv_file)) is True


def test_outside_root_rejected(tmp_path, allowed_root):
    outside = tmp_path / "outside.csv"
    outside.write_text("a,b\n1,2\n")
    assert csv_within_allowed_roots(None, str(outside)) is False


def test_subdirectory_of_root_allowed(allowed_root):
    sub = allowed_root / "sub"
    sub.mkdir()
    csv_file = sub / "cells.csv"
    csv_file.write_text("a,b\n1,2\n")
    assert csv_within_allowed_roots(None, str(csv_file)) is True


def test_dotdot_segments_rejected(tmp_path, allowed_root):
    sneaky = str(allowed_root / "sub" / ".." / "cells.csv")
    assert csv_within_allowed_roots(None, sneaky) is False


def test_symlink_escape_rejected(tmp_path, allowed_root):
    outside = tmp_path / "secret.csv"
    outside.write_text("a,b\n1,2\n")
    link = allowed_root / "link.csv"
    os.symlink(str(outside), str(link))
    assert csv_within_allowed_roots(None, str(link)) is False


def test_non_csv_rejected(allowed_root):
    not_csv = allowed_root / "image.ims"
    not_csv.write_text("x")
    assert csv_within_allowed_roots(None, str(not_csv)) is False


def test_missing_file_rejected(allowed_root):
    assert csv_within_allowed_roots(None, str(allowed_root / "nope.csv")) is False


def test_empty_and_invalid_paths_rejected():
    assert csv_within_allowed_roots(None, None) is False
    assert csv_within_allowed_roots(None, "") is False
    assert csv_within_allowed_roots(None, 123) is False


def test_browsable_roots_prefers_file_browser_settings(monkeypatch, settings):
    """The browser's configured browsable roots are the single source of
    truth (the button lives in its file modal)."""
    import configparser
    import flask_file_browser.routes as browser_routes
    browser_settings = configparser.ConfigParser(allow_no_value=True)
    browser_settings.add_section("dir_auth")
    browser_settings.set("dir_auth", "cbi", "/h20/CBI")
    browser_settings.add_section("dir_anon")
    browser_settings.set("dir_anon", "world", "/h20/Public/world")
    monkeypatch.setattr(browser_routes, "settings", browser_settings)
    roots = browsable_roots(settings)
    assert os.path.realpath("/h20/CBI") in roots
    assert os.path.realpath("/h20/Public/world") in roots


def test_browsable_roots_fallback_to_allowed_csv_dirs(monkeypatch, settings):
    """When flask_file_browser is not importable, the optional
    [allowed_csv_dirs] section is used instead."""
    import builtins
    real_import = builtins.__import__

    def broken_import(name, *args, **kwargs):
        if name.startswith("flask_file_browser"):
            raise ImportError("stubbed out")
        return real_import(name, *args, **kwargs)

    if not settings.has_section("allowed_csv_dirs"):
        settings.add_section("allowed_csv_dirs")
    settings.set("allowed_csv_dirs", "projects", "/h20/CBI/Iana/projects")
    monkeypatch.setattr(builtins, "__import__", broken_import)
    roots = browsable_roots(settings)
    assert os.path.realpath("/h20/CBI/Iana/projects") in roots


def test_sanitize_dataset_name_blocks_path_traversal():
    assert sanitize_dataset_name("../../etc/passwd") == "passwd"
    assert sanitize_dataset_name("../cells.csv") == "cells"
    with pytest.raises(ValueError):
        sanitize_dataset_name("///")
    with pytest.raises(ValueError):
        sanitize_dataset_name("..csv")
