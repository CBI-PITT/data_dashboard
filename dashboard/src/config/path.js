// Same origin: the dashboard blueprint is served by the PEACE Flask app at
// /dashboard. HOST carries the blueprint prefix so composed API paths resolve
// to /dashboard/api/... (a bare '' made them root-relative and 404).
const HOST = '/dashboard'

// Chrome-less file browser embed (same route the PEACE form picker uses),
// served by the flask_file_browser blueprint at the same origin. 
// hides the Select File/Folder buttons, which only work for the form picker.
const BROWSER_EMBED_URL = '/browser/dir_embed/?picker=0'

export { BROWSER_EMBED_URL }
export default HOST
