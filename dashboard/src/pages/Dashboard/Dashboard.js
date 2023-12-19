import "./Dashboard.css";
import React, { useState } from "react";
import Chart from "./Component/plot/Chart";
import PlotChoice from "./Component/plotChoices/PlotChoices";
import Dataset from "./Component/dataset/Dataset";
import Form from "./Component/form/Form";
import { Paper } from "@mui/material";
import Footer from "./Component/layout/footer";
import Header from "./Component/layout/header";
function Dashboard() {
  const [type_fields_dict, setType_field_dict] = useState({});

  const [displayData, setDisplayData] = useState();

  const [plotChoice, setPlotChoice] = useState("bar");

  const [formFrame, setFormFrame] = useState();

  const [acronym_volume, setAcronym_volume] = useState({});

  const [n_value, setN_value] = useState("calculating...");
  
  const [meta, setMeta] = useState({});

  const [formDataCurrent, setFormDataCurrent] = useState({
    filter_list: [],
    field: "",
    filter: { categorical: {}, continuous: {} },
    group_by: [],
    aggregate: [],
  });

  return (
    <div className="App">
      <Header />
      <div className="main_sec">
        <div className="user_selection">
          <Dataset
            setFormFrame={setFormFrame}
            setDisplayData={setDisplayData}
            setAcronym_volume={setAcronym_volume}
            setMeta={setMeta}
          />
          <Form
            setDisplayData={setDisplayData}
            setFormDataCurrent={setFormDataCurrent}
            type_fields_dict={type_fields_dict}
            setType_field_dict={setType_field_dict}
            formFrame={formFrame}
            meta={meta}
            setN_value={setN_value}
          />
        </div>

        <Paper
          className="display_container"
          elevation={10}
          style={{ backgroundColor: "rgb(246, 241, 228)" }}
        >
          <Paper className="chart" elevation={5} variant="elevation">
            <Chart
              displayData={displayData}
              field={formDataCurrent.field}
              groupBy={formDataCurrent.group_by}
              aggregation={formDataCurrent.aggregate}
              plotChoice={plotChoice}
              setPlotChoice={setPlotChoice}
              field_status={type_fields_dict[formDataCurrent.field]}
              acronym_volume={acronym_volume}
              formDataCurrent={formDataCurrent}
              formFrame={formFrame}
              meta={meta}
              n_value={n_value}
            />
          </Paper>
        </Paper>
        <Paper
          className="drawing_selection_container"
          elevation={10}
          style={{ backgroundColor: "rgb(189, 227, 209)" }}
        >
          <PlotChoice
            setPlotChoice={setPlotChoice}
            field_status={type_fields_dict[formDataCurrent.field]}
          />
        </Paper>
      </div>
      <Footer />
    </div>
  );
}

export default Dashboard;
