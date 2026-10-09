import React, { useCallback, useEffect, useRef, useState } from "react";
import axios from "axios";
import {
  Alert,
  Box,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tooltip,
  Typography,
} from "@mui/material";
import HOST from "../../../../config/path";

const PAGE_SIZE = 200;
const SCROLL_THRESHOLD = 300;
const FETCH_DEBOUNCE_MS = 500;

function TypeBadge({ kind, type }) {
  if (kind === "categorical") {
    return (
      <Tooltip title={"Categorical" + (type ? " (" + type + ")" : "")} arrow>
        <span className="typeBadge typeBadgeCategorical">abc</span>
      </Tooltip>
    );
  }
  if (kind === "date") {
    return (
      <Tooltip title={"Date (" + type + ")"} arrow>
        <span className="typeBadge typeBadgeDate">date</span>
      </Tooltip>
    );
  }
  return (
    <Tooltip title={"Numeric" + (type ? " (" + type + ")" : "")} arrow>
      <span className="typeBadge typeBadgeNumeric">123</span>
    </Tooltip>
  );
}

function DataTable({ identifier, filters }) {
  const [columns, setColumns] = useState([]);
  const [rows, setRows] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState("");

  // Scroll/append bookkeeping lives in a ref so the scroll handler and the
  // in-flight fetches always see the current values (no stale closures).
  const stateRef = useRef({ offset: 0, total: 0, busy: false, hasMore: false });

  const fetchPage = useCallback(
    async (offset, append) => {
      if (!identifier) return;
      stateRef.current.busy = true;
      if (append) {
        setLoadingMore(true);
      } else {
        setLoading(true);
      }
      try {
        const body = { offset: offset, limit: PAGE_SIZE };
        if (filters) {
          body.filter = filters;
        }
        const response = await axios.post(
          HOST + "/api/datasets/" + encodeURIComponent(identifier) + "/rows",
          body,
          { headers: { "Content-Type": "application/json" } }
        );
        const data = response.data || {};
        const pageRows = data.rows || [];
        setColumns(data.columns || []);
        setTotal(data.total || 0);
        setRows((prev) => (append ? prev.concat(pageRows) : pageRows));
        stateRef.current.offset = offset + pageRows.length;
        stateRef.current.total = data.total || 0;
        stateRef.current.hasMore = stateRef.current.offset < (data.total || 0);
        setError("");
      } catch (err) {
        const message =
          err.response && err.response.data && err.response.data.error
            ? err.response.data.error
            : err.message;
        if (!append) {
          setColumns([]);
          setRows([]);
          setTotal(0);
          stateRef.current = { offset: 0, total: 0, busy: false, hasMore: false };
        }
        setError(message);
      } finally {
        stateRef.current.busy = false;
        if (append) {
          setLoadingMore(false);
        } else {
          setLoading(false);
        }
      }
    },
    [identifier, filters]
  );

  // New dataset or changed filters: reset and (debounced — the continuous
  // sliders fire onChange continuously while dragging) load the first page.
  const filtersJson = JSON.stringify(filters || null);
  useEffect(() => {
    if (!identifier) {
      return undefined;
    }
    setColumns([]);
    setRows([]);
    setTotal(0);
    setError("");
    stateRef.current = { offset: 0, total: 0, busy: false, hasMore: false };
    const timer = setTimeout(() => {
      fetchPage(0, false);
    }, FETCH_DEBOUNCE_MS);
    return () => clearTimeout(timer);
  }, [identifier, filtersJson]);

  const handleScroll = (event) => {
    const container = event.currentTarget;
    if (
      !stateRef.current.hasMore ||
      stateRef.current.busy ||
      !identifier
    ) {
      return;
    }
    if (
      container.scrollTop + container.clientHeight >=
      container.scrollHeight - SCROLL_THRESHOLD
    ) {
      fetchPage(stateRef.current.offset, true);
    }
  };

  if (!identifier) {
    return null;
  }

  return (
    <Box className="dataTable">
      <Box className="dataTableHeader">
        <Typography variant="h6" className="dataTableTitle">
          Data
        </Typography>
        <Typography variant="body2" className="dataTableCount">
          {loading
            ? "Loading rows..."
            : rows.length === 0
            ? ""
            : "Loaded " + rows.length + " of " + total + " rows"}
          {loadingMore ? (
            <CircularProgress size={14} sx={{ ml: 1 }} color="inherit" />
          ) : null}
        </Typography>
      </Box>
      {error ? (
        <Alert severity="error" className="dataTableError">
          Could not load rows: {error}
        </Alert>
      ) : null}
      <TableContainer
        className="dataTableContainer"
        onScroll={handleScroll}
        sx={{
          maxHeight: "62vh",
          border: "1px solid var(--peace-border)",
          borderRadius: "8px",
        }}
      >
        <Table size="small" stickyHeader className="dataTableTable">
          <TableHead>
            <TableRow>
              <TableCell className="dataTableRowNumber" />
              {columns.map((col) => (
                <TableCell key={col.name} className="dataTableHeaderCell">
                  <span className="dataTableHeaderName">{col.name}</span>
                  <TypeBadge kind={col.kind} type={col.type} />
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row, rowIndex) => (
              <TableRow
                key={rowIndex}
                className={rowIndex % 2 === 1 ? "dataTableRowOdd" : ""}
              >
                <TableCell className="dataTableRowNumber">
                  {rowIndex + 1}
                </TableCell>
                {row.map((value, colIndex) => (
                  <TableCell
                    key={colIndex}
                    className="dataTableCell"
                    title={value === null || value === undefined ? "" : String(value)}
                  >
                    {value === null || value === undefined ? "" : String(value)}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      {loading ? (
        <Box className="dataTableLoading">
          <CircularProgress size={22} />
        </Box>
      ) : null}
      {!loading && !error && rows.length === 0 ? (
        <Typography className="dataTableEmpty">
          This dataset has no rows
        </Typography>
      ) : null}
    </Box>
  );
}

export default DataTable;
