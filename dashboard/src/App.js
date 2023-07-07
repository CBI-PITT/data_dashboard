import './App.css';
import React, { useEffect, useState } from 'react';

import Plot from './plot/Plot';
import PlotChoice from './plotChoices/PlotChoices';

import Form from './filters/Form';










function App() {
    const urlPrefix = "http://127.0.0.1:5000"
    const url_field = "/api/field"
    const url_filter = "/api/filters2"
    const url_groupBy = "/api/group-by"
    const url_aggregation = "/api/get-aggregate2"
    const url_query = "/api/query2"

    //Initialize columns section
    // const [Field_axis_list, setField_axis_list] = useState()
    // // const [Y_axis_list, setY_axis_list] = useState()

    // //Initialize type dict for recording all types of fileds
    const [type_fields_dict, setType_field_dict] = useState({})
    // // var type_fields_dict = {}
    // //Initialize filter section
    // const [key_Category, setkey_Category] = useState([])
    // const [value_Category, setvalue_Category] = useState([])
    // const [key_Continuous, setkey_Continuous] = useState([])
    // const [value_Continuous, setvalue_Continuous] = useState([])
    // const [tableData, setTableData] = useState()
    const [displayData, setDisplayData] = useState()

    // //Initialize GroupBy section
    // const [GroupBy_list, setGroupBy_List] = useState()

    // //Initialize Agrregation section
    // const [Aggregation_list, setAggregation_list] = useState()

    // //Initialize plot button
    const [plotChoice, setPlotChoice] = useState("bar")

    //initialize Form Data

    const [formDataCurrent, setFormDataCurrent] = useState({
        field: '',
        // y: '',
        filter: { "categorical": {}, "continuous": {} },
        group_by: [],
        aggregate: []
    })

    // const [formDataUpdated, setFormDataUpdated] = useState({
    //     field: '',
    //     filter: { "categorical": {}, "continuous": {} },
    //     group_by: [],
    //     aggregate: []
    // })



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


    //     // console.log("X_axis_list" + X_axis_list)
    //     // console.log("Y_axis_list" + Y_axis_list)
    //     // console.log("key_Category" + key_Category)
    //     // console.log("key_Continuous" + key_Continuous)
    //     // console.log("GroupBy_list: " + GroupBy_list)
    //     // console.log("Agrregation_list" + Agrregation_list)


    //     // const mockData = {
    //     //     "X_axis_list": ["cellId"],
    //     //     "Y_axis_list": ["Time_Point"],
    //     //     "categorical": { "Treatment": ["eeev", "veev", "weev"], "Time_point": [24, 48, 72, 96], "Route": ['subcutaneous'] },
    //     //     "continuous": { "Age": { "min": 0.5, "max": 5 }, "Metadata": { "min": 1, "max": 29 } },
    //     //     "GroupBy_list": ["Treatment"],
    //     //     "Aggregation_list": ["value"]
    //     // }
    //     // var agent_cate_key = []
    //     // var agent_cate_value = []
    //     // var agent_conti_key = []
    //     // var agent_conti_value = []
    //     // for (var key in mockData.categorical) {
    //     //     agent_cate_key.push(key)
    //     //     agent_cate_value.push(mockData.categorical[key])
    //     // }

    //     // for (var key in mockData.continuous) {
    //     //     agent_conti_key.push(key)
    //     //     agent_conti_value.push(mockData.continuous[key])
    //     // }
    //     // Columns (X_axis_list, Y_axis_list) setting
    //     // setX_axis_list(mockData.X_axis_list)
    //     // setY_axis_list(mockData.Y_axis_list)
    //     // console.log("X_axis_list is :" + X_axis_list)

    //     // Filter setting
    //     // setkey_Category(agent_cate_key)
    //     // setvalue_Category(agent_cate_value)
    //     // setkey_Continuous(agent_conti_key)
    //     // setvalue_Continuous(agent_conti_value)
    //     // console.log(agent_cate_key)

    //     //GroupBy list setting
    //     // setGroupBY_List(mockData.GroupBy_list)

    //     // //Aggregation list setting
    //     // setAgrregation_list(mockData.Aggregation_list)
    //     // const fetchTableData = async () => {
    //     //     const response = await fetch('/api/query');
    //     //     const data = await response.json();
    //     //     setTableData(data);
    //     // };

    //     // fetchTableData();
    // }, [])





    return (
        <div className="App">
            <header className="App-header">
                <h1>Klimstra</h1>
            </header>
            <div className='main_sec'>
                <div className='user_selection_container'>


                    <Form setDisplayData={setDisplayData} setFormDataCurrent={setFormDataCurrent} type_fields_dict={type_fields_dict} setType_field_dict={setType_field_dict} />

                </div>

                <div className='display_container'>

                    <div className='chart'>
                        
                        <Plot displayData={displayData} field={formDataCurrent.field} groupBy={formDataCurrent.group_by} aggregation={formDataCurrent.aggregate} plotChoice={plotChoice} />
                    </div>
                </div>
                
                <div className='drawing_selection_container'>
                    <PlotChoice setPlotChoice={setPlotChoice} field_status={type_fields_dict[formDataCurrent.field]} />
                </div>
            </div>


        </div>
    );
}

export default App;


