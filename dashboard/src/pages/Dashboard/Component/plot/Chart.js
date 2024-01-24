import StackBarChart from "./Charts/StackBar";
import GroupBarChart from "./Charts/GroupBar";
import LineChart from "./Charts/Line";
import AreaChart from "./Charts/Area";
import React from "react";
import PieChart from "./Charts/Pie";
import CloudChart from "./Charts/Cloud";
import CirclePackingChart from "./Charts/CirclePacking";
import FacetChart from "./Charts/Facet";
import CoverImg from "../asset/CoverImg.png";
import BoxChart from "./Charts/Box";

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
  // }

  // Only available when field type is not keyword
  // data_Box = [
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

  if (displayData === undefined) {
    // return <p>Loading....</p>
    return (
      <div className="cover">
        <img src={CoverImg} className="coverImg" alt="coverImg"></img>
        <h3 id="coverText">Statistics and Visulization</h3>
      </div>
    );
  }
  if (field_status === "keyword" && plotChoice === "box") {
    setPlotChoice("stack_bar");
    return;
  }
  if (groupBy.length !==2 && plotChoice === "group_bar") {
    setPlotChoice("stack_bar");
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
  if (
    groupBy.includes(meta_config.atlas_structure_acronym) &&
    field === meta_config.atlas_structure_acronym &&
    aggregation.includes(meta_config.aggregation_condition)
  ) {
    displayData.forEach((element) => {
      aggregation.forEach((agg) => {
        let block = {};
        let X_axis =
          groupBy.length === 1
            ? element["key"].toString()
            : element["key_as_string"];
        block["X_axis"] = X_axis;
        block["type"] = agg + "_" + field;
        block["value"] = element[agg + "_" + field]["value"];
        data_BLA.push(block);

        if (agg === meta_config.aggregation_condition) {
          let block_density = {};
          let acronym =
            groupBy.length === 1
              ? element["key"].toString()
              : element["key"][
                  groupBy.indexOf(meta_config.atlas_structure_acronym)
                ];
          block_density["X_axis"] = X_axis;
          block_density["type"] = "density" + "_" + field;
          block_density["value"] =
            element[agg + "_" + field]["value"] / acronym_volume[acronym];
          data_acronym_density_BLA.push(block_density);
        }
      });
    });
  } else {
    displayData.forEach((element) => {
      aggregation.forEach((agg) => {
        let block = {};
        let X_axis =
          groupBy.length === 1
            ? element["key"].toString()
            : element["key_as_string"];
        block["X_axis"] = X_axis;
        block["type"] = agg + "_" + field;
        block["value"] = element[agg + "_" + field]["value"];
        data_BLA.push(block);
      });
    });
  }
  // console.log(data_acronym_density_BLA)
  // console.log("format for BLA plots", data_BLA);
  if (plotChoice === "stack_bar") {
    return (
      <StackBarChart
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggregation}
        field={field}
        meta={meta_config}
        N={N}
      />
    );
  } else if(plotChoice === "group_bar") {
    return (
      <GroupBarChart
      displayData={displayData}
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggregation}
        field={field}
        meta={meta_config}
        N={N}
      />
    );
  } 
  else if (plotChoice === "pie") {
    return (
      <PieChart
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggregation}
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
        aggregation={aggregation}
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
        aggregation={aggregation}
        field={field}
        meta={meta_config}
        N={N}
      />
    );
  } else if (plotChoice === "area") {
    return (
      <AreaChart
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggregation}
        field={field}
        meta={meta_config}
        N={N}
      />
    );
  } else if (plotChoice === "box") {
    return (
      <BoxChart
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggregation}
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
        aggregation={aggregation}
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
        data_BLA={data_BLA}
        data_acronym_density_BLA={data_acronym_density_BLA}
        groupBy={groupBy}
        aggregation={aggregation}
        field={field}
        meta={meta_config}
        displayData={displayData}
        plotChoice={plotChoice}
        N={N}
      />
    );
  }
}

export default Chart;
