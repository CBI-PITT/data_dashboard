import configparser
import os
import re


def get_config(file='settings.ini', allow_no_value=True):
    """Load an INI file relative to the data_dashboard package directory,
    never the current working directory (mirrors flask_file_browser.utils)."""
    pkg_folder = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(pkg_folder, file)
    config = configparser.ConfigParser(allow_no_value=allow_no_value)
    config.read(file)
    return config


def sanitize_dataset_name(name):
    """Derive a safe dataset name from a file name: no path parts, no
    extension, only [A-Za-z0-9._-]. Raises ValueError for empty results."""
    name = os.path.basename(str(name or '').strip())
    if name.lower().endswith('.csv'):
        name = name[:-4]
    name = re.sub(r'[^A-Za-z0-9._-]+', '_', name).strip('._-')
    if not name:
        raise ValueError('Could not derive a valid dataset name from the CSV file name')
    return name


def browsable_roots(settings):
    """Directories the add-to-dashboard endpoint accepts CSVs from.

    The file browser's configured browsable roots ([dir_auth]/[dir_anon] in
    its settings.ini) are the single source of truth, because the button that
    triggers ingestion lives in that browser's file modal. When the browser
    package is not importable, the optional [allowed_csv_dirs] section in the
    dashboard settings.ini is used instead.
    """
    roots = []
    try:
        from flask_file_browser.routes import settings as browser_settings
        for section in ('dir_auth', 'dir_anon'):
            if browser_settings.has_section(section):
                for value in browser_settings[section].values():
                    if value:
                        roots.append(value)
    except Exception:
        pass
    if not roots and settings.has_section('allowed_csv_dirs'):
        for value in settings['allowed_csv_dirs'].values():
            if value:
                roots.append(value)
    return [os.path.realpath(os.path.expanduser(str(root))) for root in roots if root]


def csv_within_allowed_roots(settings, path):
    """True when path is an existing .csv file inside one of the browsable
    roots. Realpath-based containment: symlink escapes are caught because the
    resolved location must still be under a root, and explicit '..' segments
    are rejected before resolution."""
    if not path or not isinstance(path, str):
        return False
    if '\x00' in path or '\n' in path or '\r' in path:
        return False
    if '..' in path.replace('\\', '/').split('/'):
        return False
    real = os.path.realpath(path)
    if os.path.splitext(real)[1].lower() != '.csv':
        return False
    if not os.path.isfile(real):
        return False
    for root in browsable_roots(settings):
        if real == root or real.startswith(root.rstrip(os.sep) + os.sep):
            return True
    return False
