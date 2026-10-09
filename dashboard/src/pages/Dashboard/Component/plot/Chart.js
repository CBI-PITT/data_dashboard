import StackBarChart from "./Charts/StackBar";
import GroupBarChart from "./Charts/GroupBar";
import LineChart from "./Charts/Line";
import AreaChart from "./Charts/Area";
import React, { useState } from "react";
import Alert from "@mui/material/Alert";
import PieChart from "./Charts/Pie";
import CloudChart from "./Charts/Cloud";
import CirclePackingChart from "./Charts/CirclePacking";
import FacetChart from "./Charts/Facet";
import CoverImg from "../asset/cyan_brain_icon.png";
import { accentAlertSx } from "../../../../config/theme";
import BoxChart from "./Charts/Box";
import StackedBar from "./Charts/StackBar_Pl";
import GroupBar from "./Charts/GroupBar_Pl";
import Line from "./Charts/Line_Pl";
import Area from "./Charts/Area.Pl";
function Chart({
  displayData,
  field,
  groupBy,
  aggregation,
  plotChoice,
  setPlotChoice,
  field_status,
  acronym_volume,
  meta,
  n_value,
  aggList,
  errorBarChecked,
  dimension,
  setDimension,
  groupByKeys,
  setGroupByKeys,
  formFrame,
}) {
  // Request condition = { "field": "atlas_structure_acronym", "filter": { "categorical": { "atlas_structure_acronym": [], "file_path": [], "route": [], "time_point": [], "transformed_coord_units": [], "treatment": [], "uuid_brain": [], "uuid_cell": [], "voxel_spacing": [], "voxel_spacing_units": [] }, "continuous": { "Unnamed: 0": [0, 32153394], "atlas_structure_number": [0, 614454277], "metadata": [18, 39], "n_channels": [1, 2], "x_downsampled": [0, 887], "x_transformed": [0, 13925], "x_transformed_px": [0, 557], "y_downsampled": [0, 276], "y_transformed": [0, 8000], "y_transformed_px": [0, 320], "z_downsampled": [4, 1210], "z_transformed": [0, 16850], "z_transformed_px": [0, 674] } }, "group_by": ["time_point", "route", "treatment"], "aggregate": ["value_count", "cardinality"] }

  // displayData(server data) = [{
  //   cardinality_atlas_structure_acronym: { value: 61 },
  //   doc_count: 65787,
  //   key: ['24.0', 'subcutaneous', 'veev'],
  //   key_as_string: "24.0|subcutaneous|veev",
  //   value_count_atlas_structure_acronym: { value: 65787 }
  // },
  // {
  //   cardinality_atlas_structure_acronym: { value: 242 },
  //   doc_count: 4072799,
  //   key: ['48.0', 'aerosol', 'veev'],
  //   key_as_string: "48.0|aerosol|veev",
  //   value_count_atlas_structure_acronym: { value: 4072799 }
  // }]

  // BLA for Bar Line Area
  // data_BLA = [{
  //   X_axis: "24.0|subcutaneous|veev",
  //   type: "value_count_atlas_structure_acronym",
  //   value: 65787
  // }, {
  //   X_axis: "48.0|aerosol|veev",
  //   type: "cardinality_atlas_structure_acronym",
  //   value: 242
  // }]

  // Loop the aggregation, and plot each agg.
  // data_PC = [{
  //   type: "24.0|subcutaneous|veev",
  //   value: 65787
  // }, {
  //   type: "48.0|aerosol|veev",
  //   value: 242
  // }]

  // Loop the aggregation, and plot each agg. Add children dict.
  // data_Circle = {
  //   // name : 'root' (no need)
  //   children: [{
  //     type: "24.0|subcutaneous|veev",
  //     value: 65787
  //   }, {
  //     type: "48.0|aerosol|veev",
  //     value: 242
  //   }]
  // }65,536[
  //   {
  //     max: 995,
  //     median: 505.0222408432804,
  //     min: 407,
  //     q1: 477,
  //     q3: 566.3017480577137,
  //     x: "24.0|veev|subcutaneous"
  //   },
  //   {}
  // ]

  // load situation
  // BLA pre-load
  // PC, Circle, Box on-load
  // console.log(aggList);

  if (displayData === undefined) {
    // return <p>Loading....</p>
    return (
      <div className="cover">
        <img src={CoverImg} className="coverImg" alt="Brain illustration"></img>
        <h3 id="coverText">Statistics and Visualization</h3>
        {formFrame === undefined ? (
          <Alert
            severity="info"
            variant="filled"
            sx={{
              ...accentAlertSx,
              marginTop: "16px",
              maxWidth: 480,
              boxShadow: "var(--peace-shadow-lg)",
            }}
          >
            Select a dataset from the panel on the left to get started
          </Alert>
        ) : null}
      </div>
    );
  }
  if (field_status === "keyword" && plotChoice === "box") {
    setPlotChoice("stack_bar_pl");
    return;
  }
  if (groupBy.length !== 2 && plotChoice === "group_bar") {
    setPlotChoice("stack_bar_pl");
    return;
  }
  // console.log(displayData)
  // console.log(meta.atlas_structure_acronym_column_name)
  // console.log(meta)
  const meta_config = {
    atlas_structure_acronym: meta.atlas_structure_acronym_column_name,
    aggregation_condition: meta.aggregation_condition,
  };

  let N = n_value;

  // calculation for BLA or density_BLA based on condition
  let data_BLA = [];
  let data_acronym_density_BLA = [];

  // data source for stack_bar line and area
  let data_bla_pl = [];
  for (const agg of aggList) {
    data_bla_pl.push({
      x: [],
      y: [],

      error_y: {
        type: "data",
        array: [],
        visible: errorBarChecked,
      },
      customdata: [],
      hovertemplate: "%{x}<br>%{y}<br>%{customdata}",
      name: agg + "_" + field,
      type: "",
    });
  }
  // console.log(data_bla_pl);
  displayData.forEach((element) => {
    aggList.forEach((agg) => {
      let x_array = [];
      groupBy.forEach((gb) => {
        x_array.push(element["key"][gb]);
      });

      data_bla_pl[aggList.indexOf(agg)].x.push(x_array.join("|"));
      data_bla_pl[aggList.indexOf(agg)].y.push(
        element[agg + "_" + field]["value"]
      );
      if (element.hasOwnProperty("N")) {
        data_bla_pl[aggList.indexOf(agg)].customdata.push(
          `N = ${element["N"]["value"]}`
        );
      }
      if (element[agg + "_" + field].hasOwnProperty("std")) {
        data_bla_pl[aggList.indexOf(agg)].error_y.array.push(
          element[agg + "_" + field]["std"]
        );
      }
    });
  });
  data_bla_pl.forEach((element) => {
    if (element["customdata"].length === 0) {
      delete element["customdata"];
      element["hovertemplate"] = "%{x}<br>%{y}";
    }
  });
  // console.log("data_pl", data_bla_pl);

  // data source for group_bar
  let data_traces_group = [];
  aggList.forEach((agg) => {
    const groups = displayData.map((item) => ({
      [groupBy[0]]: item.key[groupBy[0]],
      [groupBy[1]]: item.key[groupBy[1]],
      value: item[agg + "_" + field]["value"],
      N: item["N"] ? item["N"]["value"] : null, // Include the N value
    }));

    // Grouping data by groupBy[0] and groupBy[1]
    const groupedData = groups.reduce((acc, curr) => {
      const key = curr[groupBy[0]] + "-" + curr[groupBy[1]];
      acc[key] = acc[key] || [];
      acc[key].push(curr);
      return acc;
    }, {});

    // Extracting unique values for groupBy[0] and groupBy[1]
    const [groupBy0Values, groupBy1Values] = [
      [...new Set(groups.map((item) => item[groupBy[0]]))],
      [...new Set(groups.map((item) => item[groupBy[1]]))],
    ];

    // Creating traces for each group
    const traces = groupBy1Values.map((groupBy1Value) => ({
      x: groupBy0Values, // Swapping groupBy0Values and groupBy1Values
      y: groupBy0Values.map((groupBy0Value) => {
        const data = groupedData[`${groupBy0Value}-${groupBy1Value}`];
        if (data) {
          return data.reduce((acc, curr) => acc + curr.value, 0);
        } else {
          return 0;
        }
      }),
      type: "bar",
      name: groupBy1Value, // Swapping name and x
      hovertemplate: "<b>%{y}</b><br>N: %{customdata}<extra></extra>", // Define hovertemplate
      customdata: groupBy0Values.map((groupBy0Value) => {
        const data = groupedData[`${groupBy0Value}-${groupBy1Value}`];
        if (data) {
          return data[0].N; // Assuming N is same for all entries in the group
        } else {
          return null;
        }
      }),
    }));

    data_traces_group.push(traces);
  });
  let arr = [];
  let haspmaps_array = [];
  for (let i = 0; i < groupBy.length; i++) {
    haspmaps_array[i] = {};
  }
  displayData.forEach((element) => {});

  // let data_traces_group = [];
  // aggList.forEach((agg) => {
  //     const groups = displayData.map((item) => ({
  //         [groupBy[0]]: item.key[groupBy[0]],
  //         [groupBy[1]]: item.key[groupBy[1]],
  //         value: item[agg + "_" + field]["value"],
  //         N: item["N"] ? item["N"]["value"] : null, // Include N value if it exists
  //     }));

  //     // Grouping data by groupBy[0] and groupBy[1]
  //     const groupedData = groups.reduce((acc, curr) => {
  //         const key = curr[groupBy[0]] + "-" + curr[groupBy[1]];
  //         acc[key] = acc[key] || [];
  //         acc[key].push(curr.value);
  //         return acc;
  //     }, {});

  //     // Extracting unique values for groupBy[0] and groupBy[1]
  //     const [groupBy0Values, groupBy1Values] = [
  //         [...new Set(groups.map((item) => item[groupBy[0]]))],
  //         [...new Set(groups.map((item) => item[groupBy[1]]))],
  //     ];

  //     // Creating traces for each group
  //     const traces = groupBy1Values.map((groupBy1Value) => ({
  //         x: groupBy0Values, // Swapping groupBy0Values and groupBy1Values
  //         y: groupBy0Values.map((groupBy0Value) =>
  //             groupedData[`${groupBy0Value}-${groupBy1Value}`]
  //                 ? groupedData[`${groupBy0Value}-${groupBy1Value}`].reduce((a, b) => a + b, 0)
  //                 : 0
  //         ),
  //         type: "bar",
  //         name: groupBy1Value, // Swapping name and x
  //         hovertemplate: `<b>%{x}</b><br>Value: %{y}<extra>N: %{customdata}</extra>`,
  //         customdata: groupBy0Values.map((groupBy0Value) =>
  //             groupedData[`${groupBy0Value}-${groupBy1Value}`]
  //                 ? groupedData[`${groupBy0Value}-${groupBy1Value}`].map((group) => group.N).join("<br>")
  //                 : ""
  //         ),
  //     }));

  //     data_traces_group.push(traces);
  // });

  // console.log(data_traces_group)

  if (plotChoice === "stack_bar") {
    return (
      <StackBarChart
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggList}
        field={field}
        meta={meta_config}
        N={N}
      />
    );
  } else if (plotChoice == "stack_bar_pl") {
    return <StackedBar data={data_bla_pl} type={"bar"} />;
  } else if (plotChoice == "group_bar_pl") {
    return <GroupBar data={data_traces_group} agg={aggList} field={field} />;
  } else if (plotChoice === "group_bar") {
    return (
      <GroupBarChart
        displayData={displayData}
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggList}
        field={field}
        meta={meta_config}
        N={N}
        acronym_volumn={acronym_volume}
      />
    );
  } else if (plotChoice === "pie") {
    return (
      <PieChart
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggList}
        field={field}
        meta={meta_config}
        displayData={displayData}
        N={N}
        acronym_volumn={acronym_volume}
      />
    );
  } else if (plotChoice === "cloud") {
    return (
      <CloudChart
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggList}
        field={field}
        meta={meta_config}
        displayData={displayData}
        N={N}
        acronym_volumn={acronym_volume}
      />
    );
  } else if (plotChoice === "line") {
    return (
      <LineChart
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggList}
        field={field}
        meta={meta_config}
        N={N}
      />
    );
  } else if (plotChoice === "line_pl") {
    return <Line data={data_bla_pl} type={"markers"} />;
  } else if (plotChoice === "area") {
    return (
      <AreaChart
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggList}
        field={field}
        meta={meta_config}
        N={N}
      />
    );
  } else if (plotChoice === "area_pl") {
    return <Area data={data_bla_pl} type={"scatter"} fill={"tozeroy"} />;
  } else if (plotChoice === "box") {
    return (
      <BoxChart
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggList}
        field={field}
        meta={meta_config}
        displayData={displayData}
        N={N}
      />
    );
  } else if (plotChoice === "circle packing") {
    return (
      <CirclePackingChart
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggList}
        field={field}
        meta={meta_config}
        displayData={displayData}
        N={N}
        acronym_volumn={acronym_volume}
      />
    );
  } else if (plotChoice === "facet") {
    return (
      <FacetChart
        aggregation={aggList}
        field={field}
        displayData={displayData}
        dimension={dimension}
        groupByKeys={groupByKeys}
      />
    );
  }
}

export default Chart;
