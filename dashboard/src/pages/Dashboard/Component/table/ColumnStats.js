import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Alert,
  Box,
  CircularProgress,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import HOST from "../../../../config/path";

const STATS_URL = "/api/datasets/";

function formatValue(value) {
  if (value === null || value === undefined) {
    return "—";
  }
  if (typeof value === "number" && Number.isFinite(value) && !Number.isInteger(value)) {
    return String(parseFloat(value.toFixed(4)));
  }
  return String(value);
}

function formatFraction(fraction) {
  if (fraction === null || fraction === undefined) {
    return "—";
  }
  return (fraction * 100).toFixed(2) + "%";
}

function ColumnStats({ identifier, columns }) {
  const [selected, setSelected] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // New dataset or a new table load: clear the selection and stats.
  const columnsJson = JSON.stringify(columns || []);
  useEffect(() => {
    setSelected(null);
    setStats(null);
    setError("");
  }, [identifier, columnsJson]);

  const fetchStats = (column) => {
    if (!identifier) {
      return;
    }
    setSelected(column);
    setLoading(true);
    axios
      .post(
        HOST + STATS_URL + encodeURIComponent(identifier) + "/column_stats",
        { column: column },
        { headers: { "Content-Type": "application/json" } }
      )
      .then((response) => {
        setStats(response.data || null);
        setError("");
        setLoading(false);
      })
      .catch((err) => {
        setStats(null);
        setError(
          err.response && err.response.data && err.response.data.error
            ? err.response.data.error
            : err.message
        );
        setLoading(false);
      });
  };

  const handleChipClick = (column) => {
    if (selected === column) {
      // Click again hides the stats.
      setSelected(null);
      setStats(null);
      setError("");
      return;
    }
    fetchStats(column);
  };

  if (!identifier || !columns || columns.length === 0) {
    return null;
  }

  const chipClass = (col) => {
    let cls = "columnChip ";
    if (col.kind === "categorical") {
      cls += "columnChipCategorical";
    } else if (col.kind === "date") {
      cls += "columnChipDate";
    } else {
      cls += "columnChipNumeric";
    }
    if (selected === col.name) {
      cls += " columnChipSelected";
    }
    return cls;
  };

  const renderNumericStats = () => {
    const s = stats.stats || {};
    const rows = [
      ["Minimum", s.min],
      ["Maximum", s.max],
      ["Mean", s.mean],
      ["Median", s.median],
      ["25% quantile", s.q25],
      ["75% quantile", s.q75],
      ["Standard deviation", s.std],
    ];
    return (
      <Box className="columnStatsBody">
        <TableContainer className="columnStatsTableContainer">
          <Table size="small" className="columnStatsTable">
            <TableBody>
              {rows.map(([label, value]) => (
                <TableRow key={label}>
                  <TableCell className="columnStatsLabel">{label}</TableCell>
                  <TableCell className="columnStatsValue">
                    {formatValue(value)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <Typography variant="body2" className="columnStatsMissing">
          n = {s.valid} valid / {s.missing} missing of {s.total} rows
        </Typography>
      </Box>
    );
  };

  const renderCategoricalStats = () => {
    const values = stats.values || [];
    return (
      <Box className="columnStatsBody">
        <TableContainer className="columnStatsTableContainer">
          <Table size="small" className="columnStatsTable">
            <TableHead>
              <TableRow>
                <TableCell className="columnStatsLabel">Value</TableCell>
                <TableCell className="columnStatsLabel">Occurrences</TableCell>
                <TableCell className="columnStatsLabel">Fraction</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {values.map((entry) => (
                <TableRow key={String(entry.value)}>
                  <TableCell
                    className="dataTableCell"
                    title={entry.value === null ? "" : String(entry.value)}
                  >
                    {entry.value === null || entry.value === undefined
                      ? "—"
                      : String(entry.value)}
                  </TableCell>
                  <TableCell className="columnStatsValue">
                    {entry.count}
                  </TableCell>
                  <TableCell className="columnStatsValue">
                    {formatFraction(entry.fraction)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <Typography variant="body2" className="columnStatsMissing">
          {stats.truncated && stats.distinct
            ? "Showing top " + values.length + " of " + stats.distinct + " values — "
            : ""}
          n = {stats.total - stats.missing} non-null / {stats.missing} missing
          of {stats.total} rows
        </Typography>
      </Box>
    );
  };

  return (
    <Box className="columnStats">
      <Typography variant="h6" className="columnStatsTitle">
        Column statistics
      </Typography>
      <Box className="columnChips">
        {columns.map((col) => (
          <button
            type="button"
            key={col.name}
            className={chipClass(col)}
            onClick={() => handleChipClick(col.name)}
          >
            {col.name}
          </button>
        ))}
      </Box>
      {loading ? (
        <Box className="columnStatsLoading">
          <LinearProgress />
        </Box>
      ) : null}
      {error ? (
        <Alert severity="error" className="dataTableError">
          Could not load statistics: {error}
        </Alert>
      ) : null}
      {!loading && !error && stats && stats.kind === "numeric"
        ? renderNumericStats()
        : null}
      {!loading && !error && stats && stats.kind === "categorical"
        ? renderCategoricalStats()
        : null}
      {!loading && !error && stats && stats.kind === "date" ? (
        <Box className="columnStatsBody">
          <TableContainer className="columnStatsTableContainer">
            <Table size="small" className="columnStatsTable">
              <TableBody>
                <TableRow>
                  <TableCell className="columnStatsLabel">Minimum</TableCell>
                  <TableCell className="columnStatsValue">
                    {formatValue(stats.stats.min)}
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="columnStatsLabel">Maximum</TableCell>
                  <TableCell className="columnStatsValue">
                    {formatValue(stats.stats.max)}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
          <Typography variant="body2" className="columnStatsMissing">
            n = {stats.stats.valid} valid / {stats.stats.missing} missing of{" "}
            {stats.stats.total} rows
          </Typography>
        </Box>
      ) : null}
      {!loading && !error && !stats && selected ? (
        <Box className="columnStatsLoading">
          <CircularProgress size={18} />
        </Box>
      ) : null}
    </Box>
  );
}

export default ColumnStats;
