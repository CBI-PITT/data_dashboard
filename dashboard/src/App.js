import './App.css';
import React, { useEffect, useState } from 'react';
import axios from "axios";

import Get_field from './filters/Get_field';
// import Get_Y_axis from './filters/Get_Y_axis';
import GetCate from './filters/Get_categorical';
import GetConti from './filters/Get_continuous';
import Get_GroupBy from './filters/Get_groupBy';
import Get_Aggregation from './filters/Get_aggregation';
import Plot from './plot/Plot';
import PlotChoice from './plotChoices/PlotChoices';
import Button from '@mui/material/Button';
// import ButtonGroup from '@mui/material/ButtonGroup';
// import Box from '@mui/material/Box';
// import barImg from './asset/bar.png'
// import boxImg from './asset/box.png'
// import dotImg from './asset/dot.png'
// import pieImg from './asset/pie.png'
// import lineImg from './asset/line.png'
// import areaImg from './asset/area.png'


// function get_X_axis(list) {
//     console.log(list)
//     if (list !== undefined) {
//         return (
//             // <div>
//             //     {
//             //         list.map((item) => (
//             //             <span>
//             //                 {item} /
//             //             </span>
//             //         ))
//             //     }
//             // </div>
//             <label for="x_axis"> X axis:
//                 <select id='x_axis' name="x">
//                     {
//                         list.map((item) => (
//                             <option value={item}>{item}</option>
//                         ))
//                     }
//                 </select>
//             </label>
//         )
//     }
// }

// function get_Y_axis(list) {
//     console.log(list)
//     if (list !== undefined) {
//         return (
//             // <div>
//             //     {
//             //         list.map((item) => (
//             //             <span>
//             //                 {item} /
//             //             </span>
//             //         ))
//             //     }
//             // </div>
//             <label for="y_axis"> Y axis:
//                 <select id='y_axis' name="y">
//                     {
//                         list.map((item) => (
//                             <option value={item}>{item}</option>
//                         ))
//                     }
//                 </select>
//             </label>
//         )
//     }
// }

// function getCate(key, value) {
//     // const key = ["Treatment", "Time_Point"]
//     // const value = [["eeve", "weev", "vvev"], [24, 48, 72, 96]]
//     if (key !== undefined && value !== undefined) {

//         return (
//             // <div>
//             //     {
//             //         key.map((k, ind) => (
//             //             <div>
//             //                 <h2>{k}</h2>
//             //                 {value[ind].map((v) => (
//             //                     <label>
//             //                         <input type="checkbox" />
//             //                         {v}
//             //                     </label>
//             //                 ))}
//             //             </div>
//             //         ))
//             //     }
//             // </div>


//             // current like{"treatment" : ["weev","veev"]}
//             // should be packed to "filter": {
//             //     "categorical": {"<column_name>": [<value1>, <value2>], "<column_name>": [<value1>, <value2>]},
//             //     "continuous": {"<column_name>": [<min>, <max>], "<column_name>": [<min>, <max>]}
//             // }
//             <div>
//                 {
//                     key.map((k, ind) => (
//                         <div>
//                             <h2>{k}</h2>
//                             <label for={k}>
//                                 {console.log(k)}
//                                 <select id={k} name={k} size={3} multiple>
//                                     {value[ind].map((v) => (
//                                         <option value={v}>
//                                             {v}
//                                         </option>
//                                     ))}
//                                 </select>
//                             </label>
//                         </div>
//                     ))
//                 }
//             </div>
//         )
//     }
// }

// function getConti(key, value) {
//     // const key = ["Treatment", "Time_Point"]
//     // const value = [["eeve", "weev", "vvev"], [24, 48, 72, 96]]
//     if (key !== undefined && value !== undefined) {
//         return (
//             // <div>
//             //     {
//             //         key.map((k, ind) => (
//             //             <div>
//             //                 <h2>{k}</h2>
//             //                 {/* {value[ind].map((v) => (
//             //                     <label>
//             //                         <input type="checkbox" />
//             //                         {v}
//             //                     </label>
//             //                 ))} */}
//             //                 <span>Min: {value[ind].min}</span>
//             //                 <span>Max: {value[ind].max}</span>
//             //             </div>
//             //         ))
//             //     }
//             // </div>
//             <div>
//                 <center>

//                     {key.map((k, ind) => (
//                         <div>
//                             <h2>{k}</h2>
//                             {/* {value[ind].map((v) => (
//                                 <label>
//                                     <input type="checkbox" />
//                                     {v}
//                                 </label>
//                             ))} */}
//                             <div>
//                                 {value[ind].min}
//                                 <input className='slider' type="range" id={k} min={value[ind].min} max={value[ind].max} name={k} />
//                                 {value[ind].max}

//                             </div>

//                         </div>
//                     ))}


//                 </center>
//             </div>
//         )
//     }
// }

// function get_GroupBy(list) {
//     console.log(list)
//     if (list !== undefined) {
//         return (
//             // <div>
//             //     {
//             //         list.map((item) => (
//             //             <span>
//             //                 {item} /
//             //             </span>
//             //         ))
//             //     }
//             // </div>
//             <div>
//                 <h2>Group By</h2>
//                 <label for="groupBy">
//                     <select id='groupBy' name="group_by" multiple size={3}>
//                         {
//                             list.map((item) => (
//                                 <option value={item}>{item}</option>
//                             ))
//                         }
//                     </select>
//                 </label>

//             </div>
//         )
//     }
// }

// function get_Aggregation(list) {
//     console.log(list)
//     if (list !== undefined) {
//         return (
//             // <div>
//             //     {
//             //         list.map((item) => (
//             //             <span>
//             //                 {item} /
//             //             </span>
//             //         ))
//             //     }
//             // </div>
//             <label for="aggregation">Aggregation:
//                 <select id='aggregation' name="aggregate" >
//                     {
//                         list.map((item) => (
//                             <option value={item}>{item}</option>
//                         ))
//                     }
//                 </select>
//             </label>
//         )
//     }
// }







function App() {
    const urlPrefix = "http://127.0.0.1:5000"
    const url_xyAxis = "/api/field"
    const url_filter = "/api/filters2"
    const url_groupBy = "/api/group-by"
    const url_aggregation = "/api/get-aggregate2"
    const url_query = "/api/query2"

    //Initialize columns section
    const [Field_axis_list, setField_axis_list] = useState()
    // const [Y_axis_list, setY_axis_list] = useState()

    //Initialize type dict for recording all types of fileds
    var type_fields_dict = {}

    //Initialize filter section
    const [key_Category, setkey_Category] = useState([])
    const [value_Category, setvalue_Category] = useState([])
    const [key_Continuous, setkey_Continuous] = useState([])
    const [value_Continuous, setvalue_Continuous] = useState([])
    const [tableData, setTableData] = useState()
    const [displayData, setDisplayData] = useState()

    //Initialize GroupBy section
    const [GroupBy_list, setGroupBy_List] = useState()

    //Initialize Agrregation section
    const [Aggregation_list, setAggregation_list] = useState()

    //Initialize plot button
    const [plotChoice, setPlotChoice] = useState("bar")

    //initialize Form Data

    const [formData, setFormData] = useState({
        field: '',
        // y: '',
        filter: { "categorical": {}, "continuous": {} },
        group_by: [],
        aggregate: []
    })
    // const plotButton = () => {
    //     const buttons = [

    //         <Button key="bar" onClick={() => {setPlotChoice("bar")}} ><img src={barImg} className="plotButton"></img></Button>,
    //         <Button key="box" onClick={() => {setPlotChoice("box")}} ><img src={boxImg} className="plotButton"></img></Button>,
    //         <Button key="dot" onClick={() => {setPlotChoice("scatter")}}><img src={dotImg} className="plotButton"></img></Button>,
    //         <Button key="pie" onClick={() => {setPlotChoice("pie")}} ><img src={pieImg} className="plotButton"></img></Button>,
    //         <Button key="line" onClick={() => {setPlotChoice("line")}}><img src={lineImg} className="plotButton"></img></Button>,
    //         <Button key="area" onClick={() => {setPlotChoice("area")}}><img src={areaImg} className="plotButton"></img></Button>
    //     ];
    //     return (

    //         <Box 
    //             sx={{
    //                 display: 'flex',
    //                 '& > *': {
    //                     m: 1,
    //                 },
    //             }}
    //         >

    //             <ButtonGroup
    //                 orientation="vertical"
    //                 aria-label="vertical contained button group"
    //                 variant= 'text'
    //                 color="inherit"                   
    //             >
    //                 {buttons}
    //             </ButtonGroup>

    //         </Box>

    //     );
    // }


    const handleSubmit = (event) => {
        event.preventDefault();
        
        

        // Boxplot testing (no choice in aggregation)
        let formData_boxplot_add = {
            "field": formData.field,
            "filter": formData.filter,
            "group_by": formData.group_by,
            "aggregate": []
        }
        formData["aggregate"].forEach(element => {
            formData_boxplot_add["aggregate"].push(element)
        });
        formData_boxplot_add["aggregate"].push("boxplot")
        var formData_send = JSON.stringify(formData_boxplot_add)

        // var formData_send = JSON.stringify(formData)
        console.log(formData)
        console.log(formData_send)
        // console.log("formdata_send", typeof (formData_send))

        fetch(urlPrefix + url_query, {
            headers: { 'Content-Type': 'application/json' },
            method: 'POST',
            body: formData_send
        }).then(
            res => res.json()
        ).then(
            data => {
                console.log(typeof (data), data)
                setTableData(data)
                // console.log("setTableData", tableData)
                setDisplayData(data)
                // console.log("setDisplayData", displayData)
            }
        )

    };

    useEffect(() => {
        // Request for field list
        axios.get(urlPrefix + url_xyAxis).then((response) => {
            type_fields_dict = response.data
            let field_list_return = Object.keys(response.data)
            // console.log(type_fields_dict)

            setField_axis_list(field_list_return)
            // setY_axis_list(xyAxis_list_return)
            // console.log(X_axis_list)
        })


        // Request for filter(key,value)
        axios.get(urlPrefix + url_filter).then((response) => {

            // console.log("filter return", response.data)

            // let filter_return = JSON.parse(response.data.replace(/\bNaN\b/g, "null"));
            let filter_return = response.data;

            // console.log(filter_return)
            let agent_cate_key = []
            let agent_cate_value = []
            let agent_conti_key = []
            let agent_conti_value = []

            for (let key in filter_return.categorical) {

                agent_cate_key.push(key)
                agent_cate_value.push(filter_return.categorical[key])
            }

            for (let key in filter_return.continuous) {
                agent_conti_key.push(key)
                agent_conti_value.push(filter_return.continuous[key])
            }

            // Filter setting
            setkey_Category(agent_cate_key)
            setvalue_Category(agent_cate_value)
            setkey_Continuous(agent_conti_key)
            setvalue_Continuous(agent_conti_value)
        });

        // Request for groupBy list
        axios.get(urlPrefix + url_groupBy).then((response) => {
            console.log("groupBy return", typeof (response.data))
            let groupBy_list_return = response.data
            setGroupBy_List(groupBy_list_return)
            //  console.log(GroupBy_list)
        })

        // Request for aggregation list
        axios.get(urlPrefix + url_aggregation).then((response) => {
            // console.log(response.data.data)
            let aggregation_list_return = response.data.data
            setAggregation_list(aggregation_list_return)
            //  console.log(Agrregation_list)
        })


        // console.log("X_axis_list" + X_axis_list)
        // console.log("Y_axis_list" + Y_axis_list)
        // console.log("key_Category" + key_Category)
        // console.log("key_Continuous" + key_Continuous)
        // console.log("GroupBy_list: " + GroupBy_list)
        // console.log("Agrregation_list" + Agrregation_list)


        // const mockData = {
        //     "X_axis_list": ["cellId"],
        //     "Y_axis_list": ["Time_Point"],
        //     "categorical": { "Treatment": ["eeev", "veev", "weev"], "Time_point": [24, 48, 72, 96], "Route": ['subcutaneous'] },
        //     "continuous": { "Age": { "min": 0.5, "max": 5 }, "Metadata": { "min": 1, "max": 29 } },
        //     "GroupBy_list": ["Treatment"],
        //     "Aggregation_list": ["value"]
        // }
        // var agent_cate_key = []
        // var agent_cate_value = []
        // var agent_conti_key = []
        // var agent_conti_value = []
        // for (var key in mockData.categorical) {
        //     agent_cate_key.push(key)
        //     agent_cate_value.push(mockData.categorical[key])
        // }

        // for (var key in mockData.continuous) {
        //     agent_conti_key.push(key)
        //     agent_conti_value.push(mockData.continuous[key])
        // }
        // Columns (X_axis_list, Y_axis_list) setting
        // setX_axis_list(mockData.X_axis_list)
        // setY_axis_list(mockData.Y_axis_list)
        // console.log("X_axis_list is :" + X_axis_list)

        // Filter setting
        // setkey_Category(agent_cate_key)
        // setvalue_Category(agent_cate_value)
        // setkey_Continuous(agent_conti_key)
        // setvalue_Continuous(agent_conti_value)
        // console.log(agent_cate_key)

        //GroupBy list setting
        // setGroupBY_List(mockData.GroupBy_list)

        // //Aggregation list setting
        // setAgrregation_list(mockData.Aggregation_list)
        // const fetchTableData = async () => {
        //     const response = await fetch('/api/query');
        //     const data = await response.json();
        //     setTableData(data);
        // };

        // fetchTableData();
    }, [])





    return (
        <div className="App">
            <header className="App-header">
                <h1>Klimstra</h1>
            </header>
            <div className='main_sec'>
                <div className='user_selection_container'>
                    <form className='form_data' onSubmit={handleSubmit}>
                        <div className='columns'>
                            <br></br>
                            {/* {Get_X_axis(X_axis_list,formData)} */}
                            <Get_field list={Field_axis_list} formData={formData} />
                            {/* <br></br> */}
                            {/* {Get_Y_axis(Y_axis_list,formData)} */}
                            {/* <Get_Y_axis list = {Y_axis_list} formData={formData} /> */}
                            <br></br>
                        </div>
                        <div className='filter'>
                            <div className='continuous'>
                                {/* {getConti(key_Continuous, value_Continuous)} */}
                                <GetConti key_Continuous={key_Continuous} value_Continuous={value_Continuous} formData={formData} />
                            </div>
                            <div className='categorical'>
                                {/* {GetCate(key_Category, value_Category,formData)} */}
                                <GetCate key_category={key_Category} value_category={value_Category} formData={formData} />
                            </div>
                            <br></br>
                        </div>
                        <div className='groupBy'>
                            {/* {Get_GroupBy(GroupBy_list)} */}
                            <br></br>
                            <Get_GroupBy list={GroupBy_list} formData={formData} />
                            <br></br>
                        </div>
                        <div className='aggregation'>
                            <br></br>
                            {/* {Get_Aggregation(Aggregation_list, formData)} */}
                            <Get_Aggregation list={Aggregation_list} formData={formData} />
                            <br></br>
                        </div>
                        <br></br>
                        <div>
                            {/* <button>submit</button> */}
                            {/* <input type="reset" value="Reset" /> */}

                            {/* <input type="submit" value="Submit" /> */}
                            <Button type='reset' variant='outlined' size='small' id="reset">Reset</Button>

                            <Button type='submit' variant='outlined' size='small' id="submit">Submit</Button>
                        </div>
                        <br></br>
                    </form>
                </div>
                <div className='display_container'>
                    {/* <div>
                        {(typeof tableData === "undefined") ? (
                            <p>Data retreiving and Loading...</p>
                        ) : (
                            <p>{tableData}</p>
                            // console.log(tableData)
                        )}
                    </div>
                    <br></br> */}
                    <div className='chart'>
                        {/* {
                            Plot(displayData, formData.x, formData.y,plotChoice)
                        } */}
                        <Plot displayData={displayData} field={formData.field} groupBy={formData.group_by} aggregation={formData.aggregate} plotChoice={plotChoice} />
                    </div>
                </div>
                {/* <div className='drawing_selection_container'>
                    {plotButton()}
                </div> */}
                <div className='drawing_selection_container'>
                    <PlotChoice setPlotChoice={setPlotChoice} />
                </div>
            </div>


        </div>
    );
}

export default App;


