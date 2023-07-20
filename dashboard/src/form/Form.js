import GetAggregation from "./Get_aggregation";
import GetCate from "./Get_categorical";
import GetConti from "./Get_continuous";
import GetField from "./Get_field";
import GetGroupBy from "./Get_groupBy";

import React, { useEffect, useState, useRef } from 'react';
import axios from "axios";
import {Button, Paper} from '@mui/material';
import Backdrop from '@mui/material/Backdrop';
import CircularProgress from '@mui/material/CircularProgress';
import SendIcon from '@mui/icons-material/Send';
import DeleteIcon from '@mui/icons-material/Delete';

function Form({ setDisplayData, setFormDataCurrent, type_fields_dict, setType_field_dict, formFrame, resetSwitch }) {
    // console.log(formFrame)
    const [Field_axis_list, setField_axis_list] = useState()
    // console.log(resetSwitch)


    //Initialize filter section
    const [key_Category, setkey_Category] = useState([])
    const [value_Category, setvalue_Category] = useState([])
    const [key_Continuous, setkey_Continuous] = useState([])
    const [value_Continuous, setvalue_Continuous] = useState([])

    const [open, setOpen] = useState(false);

    //Initialize GroupBy section
    const [GroupBy_list, setGroupBy_List] = useState()

    //Initialize Agrregation section
    const [Aggregation_list, setAggregation_list] = useState()

    //Initialize plot button

    const urlPrefix = "http://127.0.0.1:5000"
    const url_field = "/api/field"
    const url_filter = "/api/filter"
    const url_groupBy = "/api/groupBy"
    const url_aggregation = "/api/aggregation"
    const url_query = "/api/query"
    // Initialize formaDataUpdated for responsing to user selection in form 
    const [formDataUpdated, setFormDataUpdated] = useState({
        field: '',
        filter: { "categorical": {}, "continuous": {} },
        group_by: [],
        aggregate: []
    })


    useEffect(() => {
        if (formFrame === undefined) {
            return;
        } else {
            setType_field_dict(formFrame.field);
            // Other state updates...
            let field_list_return = Object.keys(formFrame.field)
            setField_axis_list(field_list_return)

            let filter_return = formFrame.filter;
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

            let groupBy_list_return = formFrame.group_by
            setGroupBy_List(groupBy_list_return)

            let aggregation_list_return = formFrame.aggregate
            setAggregation_list(aggregation_list_return)
        }
    }, [formFrame]);

    // useEffect(() => {
    //     const restFormDataUpdated = formDataUpdated
    //     restFormDataUpdated.field =''
    //     restFormDataUpdated.filter ={ "categorical": {}, "continuous": {} }
    //     restFormDataUpdated.group_by =[]
    //     restFormDataUpdated.aggregate=[]
    //     setFormDataUpdated(restFormDataUpdated)
    // },[resetSwitch])
    // console.log(formDataUpdated)


    // if(formFrame === undefined)
    // {
    //     return
    // }


    // else {
    //     setType_field_dict(formFrame.field)
    //     let field_list_return = Object.keys(formFrame.field)
    //     setField_axis_list(field_list_return)

    //     let filter_return = formFrame.filter;
    //     // console.log(filter_return)
    //     let agent_cate_key = []
    //     let agent_cate_value = []
    //     let agent_conti_key = []
    //     let agent_conti_value = []
    //     for (let key in filter_return.categorical) {
    //         agent_cate_key.push(key)
    //         agent_cate_value.push(filter_return.categorical[key])
    //     }
    //     for (let key in filter_return.continuous) {
    //         agent_conti_key.push(key)
    //         agent_conti_value.push(filter_return.continuous[key])
    //     }
    //     // Filter setting
    //     setkey_Category(agent_cate_key)
    //     setvalue_Category(agent_cate_value)
    //     setkey_Continuous(agent_conti_key)
    //     setvalue_Continuous(agent_conti_value)

    //     let groupBy_list_return = formFrame.group_by
    //     setGroupBy_List(groupBy_list_return)

    //     let aggregation_list_return = formFrame.aggregate
    //     setAggregation_list(aggregation_list_return)
    // }



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
    // }, [])

    const handleSubmit = (event) => {
        event.preventDefault();
        setOpen(true)
        // Boxplot testing (no choice in aggregation)
        let formData_boxplot_add = {
            "field": formDataUpdated.field,
            "filter": formDataUpdated.filter,
            "group_by": formDataUpdated.group_by,
            "aggregate": []
        }
        formDataUpdated["aggregate"].forEach(element => {
            formData_boxplot_add["aggregate"].push(element)
        });
        // console.log(type_fields_dict)
        // console.log(formData_boxplot_add['field'])
        // console.log(typeof(type_fields_dict[formData_boxplot_add['field']]))
        if (type_fields_dict[formData_boxplot_add['field']] !== 'keyword') {
            formData_boxplot_add["aggregate"].push("boxplot")
        }
        var formData_send = JSON.stringify(formData_boxplot_add)

        // var formData_send = JSON.stringify(formData)
        // console.log(formDataUpdated)
        console.log(formData_send)
        console.log("request send")
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
                // setTableData(data)
                // console.log("setTableData", tableData)
                setDisplayData(data)
                setFormDataCurrent(formDataUpdated)
                setOpen(false)
                console.log("response received")
                // console.log("setDisplayData", displayData)
            }
        )

    };



    return (
        <form className='form_data' onSubmit={handleSubmit}>
            <Backdrop
                sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
                open={open}
            >
                <CircularProgress color='success' />
            </Backdrop>
            {/* <div className="dataset">
                <br></br>
                <Dataset/>
                <br></br>
            </div> */}
            <div className='field'>
                <br></br>
                <GetField list={Field_axis_list} form_Data={formDataUpdated} set_FormData={setFormDataUpdated} />
                <br></br>
            </div>
            <div className='filter'>
                <div className='continuous'>
                    <GetConti key_Continuous={key_Continuous} value_Continuous={value_Continuous} form_Data={formDataUpdated} set_FormData={setFormDataUpdated} />
                </div>
                <div className='categorical'>
                    <GetCate key_category={key_Category} value_category={value_Category} form_Data={formDataUpdated} set_FormData={setFormDataUpdated} />
                </div>
                <br></br>
            </div>
            <div className='groupBy'>
                <br></br>
                <GetGroupBy list={GroupBy_list} form_Data={formDataUpdated} set_FormData={setFormDataUpdated} />
                <br></br>
            </div>
            <div className='aggregation'>
                <br></br>
                <GetAggregation list={Aggregation_list} form_Data={formDataUpdated} set_FormData={setFormDataUpdated} field_status={type_fields_dict[formDataUpdated.field]} />
                <br></br>
            </div>
            <br></br>
            <div>
                <Button type='reset' variant='contained' color='inherit' size='small' id="reset" endIcon={<DeleteIcon />}>Reset</Button>
                <Button type='submit' variant='contained' color='inherit' size='small' id="send" endIcon={<SendIcon />}>Send</Button>
            </div>
            <br></br>
        </form>
    )
}

export default Form;
