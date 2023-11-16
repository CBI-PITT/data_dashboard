import "./App.css";
import React, { useState } from "react";

import Chart from "./plot/Chart";
import PlotChoice from "./plotChoices/PlotChoices";
import Dataset from "./dataset/Dataset";
import Form from "./form/Form";
import { Paper } from "@mui/material";

function App() {
  // Initialize type dict for recording all types of fileds
  const [type_fields_dict, setType_field_dict] = useState({});

  // //Initialize filter section
  // const [key_Category, setkey_Category] = useState([])
  // const [value_Category, setvalue_Category] = useState([])
  // const [key_Continuous, setkey_Continuous] = useState([])
  // const [value_Continuous, setvalue_Continuous] = useState([])
  // const [tableData, setTableData] = useState()

  // Initialize displayData, used for receive query response
  const [displayData, setDisplayData] = useState();

  // //Initialize plot button
  const [plotChoice, setPlotChoice] = useState("bar");

  // Initialize formFrame
  const [formFrame, setFormFrame] = useState();
  // Initialize acronym_volume
  const [acronym_volume, setAcronym_volume] = useState({});
  const [meta, setMeta] = useState({})
  //initialize Form_Data_current used for rendering plot
  const [formDataCurrent, setFormDataCurrent] = useState({
    filter_list: [],
    field: "",
    filter: { categorical: {}, continuous: {} },
    group_by: [],
    aggregate: [],
  });

  // const handleSubmit = (event) => {
  //     event.preventDefault();
  //     // Boxplot testing (no choice in aggregation)
  //     let formData_boxplot_add = {
  //         "field": formDataUpdated.field,
  //         "filter": formDataUpdated.filter,
  //         "group_by": formDataUpdated.group_by,
  //         "aggregate": []
  //     }
  //     formDataUpdated["aggregate"].forEach(element => {
  //         formData_boxplot_add["aggregate"].push(element)
  //     });
  //     // console.log(type_fields_dict)
  //     // console.log(formData_boxplot_add['field'])
  //     // console.log(typeof(type_fields_dict[formData_boxplot_add['field']]))
  //     if (type_fields_dict[formData_boxplot_add['field']] !== 'keyword') {
  //         formData_boxplot_add["aggregate"].push("boxplot")
  //     }
  //     var formData_send = JSON.stringify(formData_boxplot_add)

  //     // var formData_send = JSON.stringify(formData)
  //     console.log(formDataUpdated)
  //     console.log(formData_send)
  //     // console.log("formdata_send", typeof (formData_send))

  //     fetch(urlPrefix + url_query, {
  //         headers: { 'Content-Type': 'application/json' },
  //         method: 'POST',
  //         body: formData_send
  //     }).then(
  //         res => res.json()
  //     ).then(
  //         data => {
  //             console.log(typeof (data), data)
  //             // setTableData(data)
  //             // console.log("setTableData", tableData)
  //             setDisplayData(data)
  //             setFormDataCurrent(formDataUpdated)
  //             // console.log("setDisplayData", displayData)
  //         }
  //     )

  // };

  // useEffect(() => {
  //     // Request for field list
  //     axios.get(urlPrefix + url_field).then((response) => {
  //         setType_field_dict(response.data)

  //         let field_list_return = Object.keys(response.data)
  //         // console.log(type_fields_dict)

  //         setField_axis_list(field_list_return)
  //         // setY_axis_list(xyAxis_list_return)
  //         // console.log(X_axis_list)
  //     })

  //     // Request for filter(key,value)
  //     axios.get(urlPrefix + url_filter).then((response) => {

  //         // console.log("filter return", response.data)

  //         // let filter_return = JSON.parse(response.data.replace(/\bNaN\b/g, "null"));
  //         let filter_return = response.data;

  //         // console.log(filter_return)
  //         let agent_cate_key = []
  //         let agent_cate_value = []
  //         let agent_conti_key = []
  //         let agent_conti_value = []

  //         for (let key in filter_return.categorical) {

  //             agent_cate_key.push(key)
  //             agent_cate_value.push(filter_return.categorical[key])
  //         }

  //         for (let key in filter_return.continuous) {
  //             agent_conti_key.push(key)
  //             agent_conti_value.push(filter_return.continuous[key])
  //         }

  //         // Filter setting
  //         setkey_Category(agent_cate_key)
  //         setvalue_Category(agent_cate_value)
  //         setkey_Continuous(agent_conti_key)
  //         setvalue_Continuous(agent_conti_value)
  //     });

  //     // Request for groupBy list
  //     axios.get(urlPrefix + url_groupBy).then((response) => {
  //         // console.log("groupBy return", typeof (response.data))
  //         let groupBy_list_return = response.data
  //         setGroupBy_List(groupBy_list_return)
  //         //  console.log(GroupBy_list)
  //     })

  //     // Request for aggregation list
  //     axios.get(urlPrefix + url_aggregation).then((response) => {
  //         // console.log(response.data.data)
  //         let aggregation_list_return = response.data.data
  //         setAggregation_list(aggregation_list_return)
  //         //  console.log(Agrregation_list)
  //     })

    //  console.log(acronym_volume)
    // console.log(meta)
  return (
    <div className="App">
      <header className="App-header">
        <h1>Dashboard</h1>
      </header>
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
          />
          {/* <div>{test()}</div> */}
          {/* <Form setDisplayData={setDisplayData} setFormDataCurrent={setFormDataCurrent} type_fields_dict={type_fields_dict} setType_field_dict={setType_field_dict} /> */}
        </div>

        {/* <Paper className='display_container'>
                    <Paper className='chart' elevation={10}>
                        <Chart displayData={displayData} field={formDataCurrent.field} groupBy={formDataCurrent.group_by} aggregation={formDataCurrent.aggregate} plotChoice={plotChoice} setPlotChoice={setPlotChoice} field_status={type_fields_dict[formDataCurrent.field]} />
                    </Paper>
                </Paper> */}
        {/* <Paper className='display_container' elevation={10} style={{ backgroundColor: 'rgb(211, 211, 202)' }}>
                    <Paper className = 'chart'  elevation={15}>
                        <Chart  displayData={displayData} field={formDataCurrent.field} groupBy={formDataCurrent.group_by} aggregation={formDataCurrent.aggregate} plotChoice={plotChoice} setPlotChoice={setPlotChoice} field_status={type_fields_dict[formDataCurrent.field]} />
                    </Paper>
                </Paper> */}

        <Paper
          className="display_container"
          elevation={10}
          style={{ backgroundColor: "rgb(246, 241, 228)" }}
        >
          {/* <ResponsiveContainer><Paper className='chart' elevation={5} variant='elevation' >
                        <Chart displayData={displayData} field={formDataCurrent.field} groupBy={formDataCurrent.group_by} aggregation={formDataCurrent.aggregate} plotChoice={plotChoice} setPlotChoice={setPlotChoice} field_status={type_fields_dict[formDataCurrent.field]} />
                    </Paper></ResponsiveContainer> */}
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
      <footer className="App-footer">
        <h4>
          Any using problems and suggestions, please contact
          collin9527@gmail.com
        </h4>
      </footer>
    </div>
  );
}

export default App;
