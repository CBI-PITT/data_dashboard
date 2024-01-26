import React, { useState } from "react";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import TextField from "@mui/material/TextField";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import Button from "@mui/material/Button";
import Chip from "@mui/material/Chip";
import N_number from "./N_number";
import Grid from "@mui/material/Grid";
const SortCheckbox = ({
  displayData,
  setDisplayData,
  originalArray,
  field,
  agg,
  N,
  sortCondition,
  setSortCondition,
  topN,
  setTopN,
  meta,
  groupBy,
  aggregation,
  acronym_volumn,
}) => {
  // const meta_config = {
  //   atlas_structure_acronym: meta.atlas_structure_acronym_column_name,
  //   aggregation_condition: meta.aggregation_condition,
  // };

  // let density_sort_array = [];
  // if (displayData) {
  //   density_sort_array = JSON.parse(JSON.stringify(displayData));
  //   density_sort_array.forEach((element) => {
  //     let acronym =
  //       groupBy.length === 1
  //         ? element["key"].toString()
  //         : element["key"][groupBy.indexOf(meta.atlas_structure_acronym)];
  //     element[meta_config.aggregation_condition + "_" + field].value =
  //       element[meta_config.aggregation_condition + "_" + field].value /
  //       acronym_volumn[acronym];
  //   });
  // }

  const handleSort3 = () => {
    // Shallow copy for originalArray
    if (sortCondition) {
      // if (sortCondition !== "density") {
      let sort_key = sortCondition + "_" + field;
      // Sort the displayData based on the field
      // JSON.parse(JSON.stringify(displayData))
      if (topN) {
        let sortedArray = [...originalArray]
          .sort((a, b) => b[sort_key].value - a[sort_key].value)
          .slice(0, topN);
        setDisplayData(sortedArray);
      } else {
        let sortedArray = [...originalArray].sort(
          (a, b) => b[sort_key].value - a[sort_key].value
        );
        setDisplayData(sortedArray);
      }
    }
    //   else {
    //     let sort_key = meta_config.aggregation_condition + "_" + field;
    //     if (topN) {
    //       let sortedArray = density_sort_array
    //         .sort((a, b) => b.sort_key.value - a.sort_key.value)
    //         .slice(0, topN);
    //       console.log("sorted", sortedArray);
    //       setDisplayData(sortedArray);
    //     } else {
    //       console.log(sort_key);
    //       let sortedArray = density_sort_array.sort(
    //         (a, b) => b[sort_key].value - a[sort_key].value
    //       );
    //       console.log("sorted", sortedArray);
    //       setDisplayData(sortedArray);
    //     }
    //   }
    // }
    else {
      // Use the original displayData
      if (topN) {
        let topN_array = [...originalArray].slice(0, topN);
        setDisplayData(topN_array);
      } else {
        setDisplayData(originalArray);
      }
    }

    // console.log(originalArray);
  };

  if (displayData) {
    let aggregation_density_checked = [...agg];
    const firstObjectHasDensityAttribute = Object.keys(displayData[0]).some(
      (key) => key.startsWith("density")
    );
    if (firstObjectHasDensityAttribute) {
      aggregation_density_checked.push("density");
      // aggregation_density_checked.push('density')
    }
    return (
      <Grid container spacing={2}>
        {/* <FormControlLabel
          control={
            <Checkbox
              checked={isCheckedSort}
              onChange={handleSort}
              color="primary"
              disabled={disableSort}
            />
          }
          label={`Sort by`}
          style={{ float: "left" }}
        />
        <FormControlLabel
          control={
            <Checkbox
              checked={isCheckedTopN}
              onChange={handleTopN}
              color="primary"
              disabled={disableTopN}
            />
          }
          label={`Top 20`}
          style={{ float: "left" }}
        /> */}
        <Grid item>
          <FormControl sx={{ m: 1, minWidth: 120 }}>
            <InputLabel id="sortConditionx-label">Sort by</InputLabel>
            <Select
              labelId="sortConditionx-label"
              id="sortConditionx"
              value={sortCondition}
              label="sortCondition *"
              name="sortCondition"
              onChange={(event) => {
                setSortCondition(event.target.value);
              }}
              // autoWidth
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              {aggregation_density_checked.map((item) => (
                <MenuItem value={item} key={item}>
                  {item}
                </MenuItem>
              ))}
              {/* {groupBy.includes(meta_config.atlas_structure_acronym) &&
                field === meta_config.atlas_structure_acronym &&
                aggregation.includes(meta_config.aggregation_condition) && (
                  <MenuItem value="density">density</MenuItem>
                )} */}
            </Select>
          </FormControl>
        </Grid>
        <Grid item>
          <FormControl sx={{ m: 1, minWidth: 50 }}>
            <TextField
              type="number"
              variant="standard"
              id="topN"
              value={topN}
              onChange={(e) => {
                setTopN(e.target.value);
              }}
              label="TopN"
            />
          </FormControl>
        </Grid>
        <Grid item>
          <FormControl sx={{ m: 2, minWidth: 50 }}>
            <Button variant="contained" onClick={handleSort3}>
              Apply
            </Button>
          </FormControl>
        </Grid>
        <Grid item sx={{ marginLeft: "auto" }}>
          <FormControl sx={{ m: 3, minWidth: 50 }}>
            <N_number N={N} />
          </FormControl>
        </Grid>
      </Grid>
    );
  }
};

export default SortCheckbox;
