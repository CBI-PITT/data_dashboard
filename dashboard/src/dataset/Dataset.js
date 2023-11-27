import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import Chip from "@mui/material/Chip";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import { Paper } from "@mui/material";
import React, { useEffect, useState } from "react";
import axios from "axios";
import Dividers from "./Divider";
const urlPrefix = "http://127.0.0.1:5000";
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
  useEffect(() => {
    axios.get(urlPrefix + url_index).then((response) => {
      setDataset(response.data);
    });
  }, []);

  return (
    <Paper elevation={10} className="dataset">
      <br></br>
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
            axios
              .get(urlPrefix + url_index_choosen + index)
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
              .get(urlPrefix + url_index_choosen_status + index)
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
              .get(urlPrefix + url_index_choosen_meta + index)
              .then((response) => {
                console.log("Index meta retreive successfully");

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

      <Dividers index_status={indexStatus}></Dividers>
    </Paper>
  );
}

export default Dataset;
