import "./Dashboard.css";
import React, { useState } from "react";
import Chart from "./Component/plot/Chart";
import PlotChoice from "./Component/plotChoices/PlotChoices";
import Dataset from "./Component/dataset/Dataset";
import Form from "./Component/form/Form";
import { Paper, Grid } from "@mui/material";
import Header from "./Component/layout/header";
import MetricsTool from "./Component/plot/Control/MetricsTool";
import N_number from "./Component/plot/Control/N_number";
function Dashboard() {
  const [type_fields_dict, setType_field_dict] = useState({});

  const [displayData, setDisplayData] = useState();
  const [aggList, setAggList] = useState([]);
  const [plotChoice, setPlotChoice] = useState("stack_bar_pl");

  const [formFrame, setFormFrame] = useState();

  const [acronym_volume, setAcronym_volume] = useState({});

  const [n_value, setN_value] = useState("calculating...");

  const [meta, setMeta] = useState({});

  const [originalArray, setOriginalArray] = useState();

  const [sortCondition, setSortCondition] = useState("");
  const [topN, setTopN] = useState("");
  const [dimension,setDimension] = useState('')
  const [groupByKeys,setGroupByKeys] = useState([])
  const [aggregation_density_checked, set_aggregation_density_checked] =
    useState([]);
  const [errorBarChecked, setErrorBarChecked] = useState(true);
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
      <Grid
        container
        spacing={3}
        columns={20}
        sx={{ padding: "16px" }}
      >
        <Grid item xs={20} sm={20} md={3} lg={3} xl={4}>
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
            setOriginalArray={setOriginalArray}
            setSortCondition={setSortCondition}
            setTopN={setTopN}
            setAggList={setAggList}
            setDimension={setDimension}
            setGroupByKeys={setGroupByKeys}
          />
        </Grid>
        <Grid item xs={20} sm={20} md={16} lg={15.5} xl={15}>
          <Paper
            className="chart"
            elevation={0}
            sx={{
              borderRadius: "12px",
              border: "1px solid var(--peace-border)",
              boxShadow: "var(--peace-shadow-lg)",
              backgroundColor: "var(--peace-surface)",
            }}
          >
            <MetricsTool
              originalArray={originalArray}
              plotChoice = {plotChoice}
              setDisplayData={setDisplayData}
              field={formDataCurrent.field}
              agg={formDataCurrent.aggregate}
              N={n_value}
              sortCondition={sortCondition}
              setSortCondition={setSortCondition}
              topN={topN}
              setTopN={setTopN}
              meta={meta}
              groupBy={formDataCurrent.group_by}
              aggregation={formDataCurrent.aggregate}
              acronym_volumn={acronym_volume}
              errorBarChecked={errorBarChecked}
              setErrorBarChecked={setErrorBarChecked}
              dimension={dimension}
              setDimension={setDimension}
              setGroupByKeys={setGroupByKeys}
              aggList={aggList}
              displayData={displayData}
            />

            <Chart
              displayData={displayData}
              field={formDataCurrent.field}
              groupBy={formDataCurrent.group_by}
              aggregation={formDataCurrent.aggregate}
              plotChoice={plotChoice}
              setPlotChoice={setPlotChoice}
              field_status={type_fields_dict[formDataCurrent.field]}
              acronym_volume={acronym_volume}
              meta={meta}
              n_value={n_value}
              aggList={aggList}
              errorBarChecked={errorBarChecked}
              dimension={dimension}
              setDimension={setDimension}
              groupByKeys={groupByKeys}
              setGroupByKeys={setGroupByKeys}
              formFrame={formFrame}
            />
          </Paper>
        </Grid>
        <Grid item xs={20} sm={20} md={1} lg={1.5} xl={1}>
          <Paper
            elevation={0}
            sx={{
              padding: "8px",
              borderRadius: "12px",
              border: "1px solid var(--peace-border)",
              boxShadow: "var(--peace-shadow)",
              backgroundColor: "var(--peace-surface)",
            }}
          >
            <PlotChoice
              setPlotChoice={setPlotChoice}
              plotChoice={plotChoice}
              field_status={type_fields_dict[formDataCurrent.field]}
              groupBy={formDataCurrent.group_by}
            />
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}

export default Dashboard;
