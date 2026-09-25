import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import Chip from "@mui/material/Chip";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import { Paper, Tooltip } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import RefreshIcon from "@mui/icons-material/Refresh";
import React, { useCallback, useEffect, useState } from "react";
import axios from "axios";
import Dividers from "./Divider";
import HOST from "../../../../config/path";

const url_index = "/api/indices";
const url_index_choosen = "/api/index_choosen/";
const url_index_choosen_status = "/api/index_choosen/current_status/";
const url_index_choosen_meta = "/api/index_choosen/meta/";
function Dataset({ setFormFrame, setDisplayData, setAcronym_volume, setMeta }) {
  const [dataset, setDataset] = useState([]);

  const [indexStatus, setIndexStatus] = useState({
    health: "NaN",
    status: "NaN",
    storageSize: "NaN",
    docCount: "NaN",
  });

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

  return (
    <Paper elevation={10} className="dataset">
      <br></br>
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
              axios
                .get(HOST + url_index_choosen + index)
                .then((response) => {
                  console.log("Index selected or changed successfully");
                  setFormFrame(response.data);
                });
              setIndexStatus({
                health: "Retrieving",
                status: "Retrieving",
                storageSize: "Retrieving",
                docCount: "Retrieving",
              });
              axios
                .get(HOST + url_index_choosen_status + index)
                .then((response) => {
                  console.log("Index status retreive successfully");

                  setIndexStatus({
                    health: response.data["health"],
                    status: response.data["status"],
                    storageSize: response.data["storage_size"],
                    docCount: response.data["docs_count"],
                  });
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
      </div>

      <Dividers index_status={indexStatus}></Dividers>
    </Paper>
  );
}

export default Dataset;
