import './App.css';
import React, { useEffect, useState } from 'react';
import axios from "axios";

import get_X_axis from './dataRetreive/get_X_axis';
import get_Y_axis from './dataRetreive/get_Y_axis';
import getCate from './dataRetreive/get_categorical';
import getConti from './dataRetreive/get_continuous';
import get_GroupBy from './dataRetreive/get_groupBy';
import get_Aggregation from './dataRetreive/get_aggregation';
import bar from './asset/bar.png'


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
    const url_xyAxis = "/api/get-xy"
    const url_filter = "/api/filters"
    const url_groupBy = "/api/get-group-by"
    const url_aggregation = "/api/get-aggregate"
    const url_query = "/api/query"

    //Initialize columns section
    const [X_axis_list, setX_axis_list] = useState()
    const [Y_axis_list, setY_axis_list] = useState()

    //Initialize filter section
    const [key_Category, setkey_Category] = useState()
    const [value_Category, setvalue_Category] = useState()
    const [key_Continuous, setkey_Continuous] = useState()
    const [value_Continuous, setvalue_Continuous] = useState()
    const [tableData, setTableData] = useState([])

    //Initialize GroupBy section
    const [GroupBy_list, setGroupBy_List] = useState()

    //Initialize Agrregation section
    const [Aggregation_list, setAggregation_list] = useState()

    //initialize Form Data
    // const [formData, setFormData] = useState({
    //     x: '',
    //     y: '',
    //     filter: { "categorical": {}, "continuous": {} },
    //     group_by: [],
    //     aggregate: ''
    // });
    const formData = {
        x: '',
        y: '',
        filter: { "categorical": {}, "continuous": {} },
        group_by: [],
        aggregate: ''
    }
    const handleSubmit = (event) => {
        event.preventDefault();
        let breakFlag = false;
        formData.x = event.target.x.value;
        formData.y = event.target.y.value;
        if(formData.x === formData.y)
        {
            alert("X axis shoud not be same as y axis")
            return
        }
        console.log(formData)
        // Categorical form data setting
        const map_categorical = new Map()
        key_Category.forEach(element => {
            if(breakFlag)
            {
                return 
            }
            console.log("event.target.element", document.getElementById(element))
            let all_choice_keyInCategorical = document.getElementById(element)
            let select_keyInCategorical = [];
            for (let i = 0; i < all_choice_keyInCategorical.length; i++) {
                // console.log(all_choice_keyInCategorical.options[1])
                if (all_choice_keyInCategorical.options[i].selected) {
                    select_keyInCategorical.push(all_choice_keyInCategorical[i].value)
                }
                map_categorical.set(element, select_keyInCategorical)
            }
            if(select_keyInCategorical.length === 0)
            {
                alert("Please fill the required section!")
                breakFlag = true;
                return
            }
            
            formData.filter.categorical = map_categorical

        }
        
        );

        if(breakFlag)
        {
            return
        }
        

        // Continuous form data setting
        const map_continuous = new Map()
        key_Continuous.forEach(element => {

            console.log("event.target.element", document.getElementById(element))
            let selectValue_keyInContinuous = document.getElementById(element)
            map_continuous.set(element, selectValue_keyInContinuous.value)
            

        });
        formData.filter.continuous = map_continuous
        
        // var select = document.getElementById("groupBy");
        let all_choice_groupBy = document.getElementById("groupBy")
        let select_groupBy = [];
        for (let i = 0; i < all_choice_groupBy.length; i++) {
            if (all_choice_groupBy.options[i].selected) {
                select_groupBy.push(all_choice_groupBy[i].value);
            }
        }
        if (select_groupBy.length === 0)
        {
            alert("Please fill the required section!")
            return 
        }
        // console.log("groupBy:",select_groupBy)

        formData.group_by = select_groupBy;
        formData.aggregate = event.target.aggregate.value
        
        
        // console.log("formData type", typeof (formData));
        // // console.log(formData.x);
        // // console.log(formData.y);
        // // console.log(formData.filter)
        // // console.log(formData.group_by);
        // // console.log(formData.aggregate);
    

        console.log(formData)
        console.log("formdata",typeof(formData))
        fetch("/api/query",{
            method:'POST',
            body:formData
            
        }).then(
            res => res.json()
        ).then(
            data => {
                setTableData(data)
                console.log(data)
            }
        )
    };

    useEffect(() => {
        // fetch("/api/query").then(
        //     res => res.json()
        // ).then(
        //     data => {
        //         setTableData(data)
        //         console.log(data)
        //     }
        // )

        // Request for xy axis list
        axios.get(urlPrefix + url_xyAxis).then((response) => {
            let xyAxis_list_return = response.data.data
            // console.log(xyAxis_list_return)
            setX_axis_list(xyAxis_list_return)
            setY_axis_list(xyAxis_list_return)
            // console.log(X_axis_list)
        })
        

        // Request for filter(key,value)
        axios.get(urlPrefix + url_filter).then((response) => {

            console.log("filter return", typeof (response.data))

            let filter_return = JSON.parse(response.data.replace(/\bNaN\b/g, "null"));
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
            console.log("groupBy return", typeof (response.data.data))
            let groupBy_list_return = response.data.data
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
                            {get_X_axis(X_axis_list)}
                            <br></br>
                            {get_Y_axis(Y_axis_list)}
                            <br></br>
                        </div>
                        <div className='filter'>
                            <div className='continuous'>
                                {getConti(key_Continuous, value_Continuous)}
                            </div>
                            <div className='categorical'>
                                {getCate(key_Category, value_Category)}
                            </div>
                            <br></br>
                        </div>
                        <div className='groupBy'>
                            {get_GroupBy(GroupBy_list)}
                            <br></br>
                        </div>
                        <div className='aggregation'>
                            <br></br>
                            {get_Aggregation(Aggregation_list)}
                            <br></br>
                        </div>
                        <br></br>
                        <div>
                            {/* <button>submit</button> */}
                            <input type="submit" value="Submit" />
                            <input type="reset" value="Reset" />
                        </div>
                        <br></br>
                    </form>
                </div>
                <div className='display_container'>
                    <div>
                        {(typeof tableData === "undefined") ? (
                            <p>Loading...</p>
                        ) : (
                            <p>{tableData}</p>
                            // console.log(tableData)
                        )}
                    </div>
                    
                </div>
                <div className='drawing_selection_container'>
                    
                       
                </div>
            </div>

            <div>
            </div>

        </div>
    );
}

export default App;


