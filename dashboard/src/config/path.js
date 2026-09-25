// Same origin: the dashboard blueprint is served by the PEACE Flask app at
// /dashboard. HOST carries the blueprint prefix so composed API paths resolve
// to /dashboard/api/... (a bare '' made them root-relative and 404).
const HOST = '/dashboard'

export default HOST
