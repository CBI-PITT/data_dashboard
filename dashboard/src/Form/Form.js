import GetAggregation from "./Get_aggregation";
import GetCate from "./Get_categorical";
import GetConti from "./Get_continuous";
import GetField from "./Get_field";
import GetGroupBy from "./Get_groupBy";
import React, { useEffect, useState } from 'react';
import axios from "axios";
import Button from '@mui/material/Button';
import Backdrop from '@mui/material/Backdrop';
import CircularProgress from '@mui/material/CircularProgress';
import SendIcon from '@mui/icons-material/Send';
import DeleteIcon from '@mui/icons-material/Delete';
function Form({ setDisplayData, setFormDataCurrent, type_fields_dict, setType_field_dict }) {
    const [Field_axis_list, setField_axis_list] = useState()
    // const [Y_axis_list, setY_axis_list] = useState()

    //Initialize type dict for recording all types of fileds
    // const [type_fields_dict,setType_field_dict] = useState({})
    // var type_fields_dict = {}
    //Initialize filter section
    const [key_Category, setkey_Category] = useState([])
    const [value_Category, setvalue_Category] = useState([])
    const [key_Continuous, setkey_Continuous] = useState([])
    const [value_Continuous, setvalue_Continuous] = useState([])



    //Initialize GroupBy section
    const [GroupBy_list, setGroupBy_List] = useState()

    //Initialize Agrregation section
    const [Aggregation_list, setAggregation_list] = useState()

    //Initialize plot button

    const urlPrefix = "http://127.0.0.1:5000"
    const url_field = "/api/field"
    const url_filter = "/api/filters2"
    const url_groupBy = "/api/group-by"
    const url_aggregation = "/api/get-aggregate2"
    const url_query = "/api/query2"

    const [formDataUpdated, setFormDataUpdated] = useState({
        field: '',
        filter: { "categorical": {}, "continuous": {} },
        group_by: [],
        aggregate: []
    })
    const [open, setOpen] = useState(false);


    useEffect(() => {
        // Request for field list
        axios.get(urlPrefix + url_field).then((response) => {
            setType_field_dict(response.data)


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
            // console.log("groupBy return", typeof (response.data))
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



    }, [])
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
            <div className='field'>
                <br></br>
                {/* {Get_X_axis(X_axis_list,formData)} */}
                <GetField list={Field_axis_list} form_Data={formDataUpdated} set_FormData={setFormDataUpdated} />
                {/* <br></br> */}
                {/* {Get_Y_axis(Y_axis_list,formData)} */}
                {/* <Get_Y_axis list = {Y_axis_list} formData={formData} /> */}
                <br></br>
            </div>
            <div className='filter'>
                <div className='continuous'>
                    {/* {getConti(key_Continuous, value_Continuous)} */}
                    <GetConti key_Continuous={key_Continuous} value_Continuous={value_Continuous} form_Data={formDataUpdated} set_FormData={setFormDataUpdated} />
                </div>
                <div className='categorical'>
                    {/* {GetCate(key_Category, value_Category,formData)} */}
                    <GetCate key_category={key_Category} value_category={value_Category} form_Data={formDataUpdated} set_FormData={setFormDataUpdated} />
                </div>
                <br></br>
            </div>
            <div className='groupBy'>
                {/* {Get_GroupBy(GroupBy_list)} */}
                <br></br>
                <GetGroupBy list={GroupBy_list} form_Data={formDataUpdated} set_FormData={setFormDataUpdated} />
                <br></br>
            </div>
            <div className='aggregation'>
                <br></br>
                {/* {Get_Aggregation(Aggregation_list, formData)} */}
                <GetAggregation list={Aggregation_list} form_Data={formDataUpdated} set_FormData={setFormDataUpdated} field_status={type_fields_dict[formDataUpdated.field]} />
                <br></br>
            </div>
            <br></br>
            <div>
                {/* <button>submit</button> */}
                {/* <input type="reset" value="Reset" /> */}

                {/* <input type="submit" value="Submit" /> */}
                <Button type='reset' variant='contained' color='inherit' size='small' id="reset" endIcon={<DeleteIcon />}>Reset</Button>

                <Button type='submit' variant='contained' color='inherit' size='small' id="send" endIcon={<SendIcon />}>Send</Button>
                
            </div>
            <br></br>
        </form>

    )
}

export default Form;
