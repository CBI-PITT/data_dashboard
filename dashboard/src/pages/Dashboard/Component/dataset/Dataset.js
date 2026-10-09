import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import Chip from "@mui/material/Chip";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import {
  Paper,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Checkbox,
  ListItemText,
} from "@mui/material";
import IconButton from "@mui/material/IconButton";
import RefreshIcon from "@mui/icons-material/Refresh";
import EditIcon from "@mui/icons-material/Edit";
import CallMergeIcon from "@mui/icons-material/CallMerge";
import DeleteIcon from "@mui/icons-material/Delete";
import React, { useCallback, useEffect, useState } from "react";
import axios from "axios";
import HOST from "../../../../config/path";

const url_index = "/api/indices";
const url_index_choosen = "/api/index_choosen/";
const url_index_choosen_meta = "/api/index_choosen/meta/";
const url_rename = "/api/datasets/";
const url_merge = "/api/merge";

// "treatment=ctrl, time=24" -> {"treatment": "ctrl", "time": "24"}
export function parseFieldsText(text) {
  const fields = {};
  String(text || "")
    .split(",")
    .forEach((pair) => {
      const [key, ...rest] = pair.split("=");
      const value = rest.join("=").trim();
      if (key && key.trim() && value) {
        fields[key.trim()] = value;
      }
    });
  return fields;
}

function Dataset({ setFormFrame, setDisplayData, setAcronym_volume, setMeta, setSelectedDataset }) {
  const [dataset, setDataset] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState("");

  const [renameOpen, setRenameOpen] = useState(false);
  const [renameValue, setRenameValue] = useState("");

  const [deleteOpen, setDeleteOpen] = useState(false);

  const [mergeOpen, setMergeOpen] = useState(false);
  const [mergeSelections, setMergeSelections] = useState([]);
  const [mergeFieldsText, setMergeFieldsText] = useState({});
  const [mergeName, setMergeName] = useState("");

  const fetchIndices = useCallback(() => {
    axios.get(HOST + url_index).then((response) => {
      setDataset(response.data);
    });
  }, []);

  useEffect(() => {
    fetchIndices();
    // Re-fetch when the tab becomes visible again so datasets added from the
    // File Browser tab (Add to dashboard) appear without a manual reload.
    const onVisibilityChange = () => {
      if (document.visibilityState === "visible") {
        fetchIndices();
      }
    };
    document.addEventListener("visibilitychange", onVisibilityChange);
    return () =>
      document.removeEventListener("visibilitychange", onVisibilityChange);
  }, [fetchIndices]);

  const submitRename = () => {
    axios
      .post(
        HOST + url_rename + encodeURIComponent(selectedIndex) + "/rename",
        { new_name: renameValue },
        { headers: { "Content-Type": "application/json" } }
      )
      .then((response) => {
        const renamed = response.data.dataset;
        if (selectedIndex === sessionStorage.getItem("INDEX")) {
          sessionStorage.setItem("INDEX", renamed);
        }
        setRenameOpen(false);
        fetchIndices();
      })
      .catch((error) => {
        console.error("Rename failed:", error);
        window.alert(
          "Rename failed: " +
            (error.response && error.response.data && error.response.data.error
              ? error.response.data.error
              : error.message)
        );
      });
  };

  const submitDelete = () => {
    axios
      .post(
        HOST + url_rename + encodeURIComponent(selectedIndex) + "/delete",
        {},
        { headers: { "Content-Type": "application/json" } }
      )
      .then(() => {
        if (selectedIndex === sessionStorage.getItem("INDEX")) {
          sessionStorage.removeItem("INDEX");
          setSelectedIndex("");
          if (setSelectedDataset) setSelectedDataset("");
        }
        setDeleteOpen(false);
        fetchIndices();
      })
      .catch((error) => {
        console.error("Delete failed:", error);
        window.alert(
          "Delete failed: " +
            (error.response && error.response.data && error.response.data.error
              ? error.response.data.error
              : error.message)
        );
      });
  };

  const submitMerge = () => {
    const fields = {};
    mergeSelections.forEach((identifier) => {
      fields[identifier] = parseFieldsText(mergeFieldsText[identifier]);
    });
    axios
      .post(
        HOST + url_merge,
        { datasets: mergeSelections, name: mergeName, fields: fields },
        { headers: { "Content-Type": "application/json" } }
      )
      .then(() => {
        setMergeOpen(false);
        setMergeSelections([]);
        setMergeFieldsText({});
        setMergeName("");
        fetchIndices();
      })
      .catch((error) => {
        console.error("Merge failed:", error);
        window.alert(
          "Merge failed: " +
            (error.response && error.response.data && error.response.data.error
              ? error.response.data.error
              : error.message)
        );
      });
  };

  return (
    <Paper
      elevation={0}
      className="dataset"
      sx={{
        padding: "10px",
        borderRadius: "12px",
        border: "1px solid var(--peace-border)",
        boxShadow: "var(--peace-shadow)",
      }}
    >
      <div style={{ display: "flex", alignItems: "flex-end" }}>
        <FormControl required sx={{ m: 1, minWidth: 120 }}>
          <InputLabel id="dataset-required-label">Index</InputLabel>
          <Select
            labelId="dataset-required-label"
            id="dataset-required"
            // value=''
            defaultValue={""}
            label="dataset *"
            name="dataset"
            onChange={(event) => {
              setFormFrame("dataset retrieving");
              setDisplayData();
              let index = event.target.value;
              sessionStorage.setItem('INDEX', index);
              if (setSelectedDataset) setSelectedDataset(index);
              setSelectedIndex(index);
              axios
                .get(HOST + url_index_choosen + index)
                .then((response) => {
                  console.log("Index selected or changed successfully");
                  setFormFrame(response.data);
                });
              axios
                .get(HOST + url_index_choosen_meta + index)
                .then((response) => {
                  console.log("Index meta retreive successfully");
                  console.log(response.data)
                  sessionStorage.setItem('serialized_parameters',JSON.stringify(response.data))
                  setMeta(response.data["meta"]);
                  setAcronym_volume(response.data["acronym_volumn"]);
                });
            }}
            renderValue={(selected) => <Chip label={selected} />}
          >
            {dataset.map((item) => (
              <MenuItem value={item} key={item}>
                {item}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Tooltip title="Refresh dataset list">
          <IconButton
            onClick={fetchIndices}
            size="small"
            sx={{ mb: 1.5 }}
            aria-label="Refresh dataset list"
          >
            <RefreshIcon />
          </IconButton>
        </Tooltip>
        <Tooltip title="Rename selected dataset">
          <span>
            <IconButton
              onClick={() => {
                setRenameValue(selectedIndex.split("/").pop());
                setRenameOpen(true);
              }}
              size="small"
              sx={{ mb: 1.5 }}
              disabled={!selectedIndex}
              aria-label="Rename selected dataset"
            >
              <EditIcon />
            </IconButton>
          </span>
        </Tooltip>
        <Tooltip title="Merge datasets into one comparable dataset">
          <IconButton
            onClick={() => setMergeOpen(true)}
            size="small"
            sx={{ mb: 1.5 }}
            disabled={dataset.length < 2}
            aria-label="Merge datasets"
          >
            <CallMergeIcon />
          </IconButton>
        </Tooltip>
        <Tooltip title="Delete selected dataset (dashboard only, original CSV is kept)">
          <span>
            <IconButton
              onClick={() => setDeleteOpen(true)}
              size="small"
              sx={{ mb: 1.5 }}
              disabled={!selectedIndex}
              aria-label="Delete selected dataset"
            >
              <DeleteIcon />
            </IconButton>
          </span>
        </Tooltip>
      </div>

      <Dialog open={renameOpen} onClose={() => setRenameOpen(false)}>
        <DialogTitle>Rename dataset</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="New dataset name"
            fullWidth
            value={renameValue}
            onChange={(event) => setRenameValue(event.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRenameOpen(false)}>Cancel</Button>
          <Button
            onClick={submitRename}
            disabled={!renameValue.trim()}
            variant="contained"
          >
            Rename
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={deleteOpen} onClose={() => setDeleteOpen(false)}>
        <DialogTitle>Delete dataset</DialogTitle>
        <DialogContent>
          Delete <strong>{selectedIndex.split("/").pop()}</strong> from the
          dashboard? This only removes the dataset from the dashboard — the
          original CSV file is not affected. This cannot be undone.
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteOpen(false)}>Cancel</Button>
          <Button onClick={submitDelete} variant="contained" color="error">
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={mergeOpen} onClose={() => setMergeOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Merge datasets</DialogTitle>
        <DialogContent>
          <FormControl fullWidth sx={{ mt: 1 }}>
            <InputLabel id="merge-datasets-label">Datasets to merge</InputLabel>
            <Select
              labelId="merge-datasets-label"
              multiple
              value={mergeSelections}
              onChange={(event) => setMergeSelections(event.target.value)}
              renderValue={(selected) => selected.join(", ")}
            >
              {dataset.map((item) => (
                <MenuItem value={item} key={item}>
                  <Checkbox checked={mergeSelections.indexOf(item) > -1} />
                  <ListItemText primary={item} />
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          {mergeSelections.map((identifier) => (
            <TextField
              key={identifier}
              margin="dense"
              fullWidth
              size="small"
              label={"Fields for " + identifier + " (key=value, ...)"}
              placeholder="treatment=ctrl, time=24"
              value={mergeFieldsText[identifier] || ""}
              onChange={(event) =>
                setMergeFieldsText({
                  ...mergeFieldsText,
                  [identifier]: event.target.value,
                })
              }
            />
          ))}
          <TextField
            margin="dense"
            fullWidth
            label="Merged dataset name"
            value={mergeName}
            onChange={(event) => setMergeName(event.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setMergeOpen(false)}>Cancel</Button>
          <Button
            onClick={submitMerge}
            disabled={mergeSelections.length < 2 || !mergeName.trim()}
            variant="contained"
          >
            Merge
          </Button>
        </DialogActions>
      </Dialog>
    </Paper>
  );
}

export default Dataset;
