
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';

import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { Paper } from '@mui/material';
import React, { useEffect, useState } from 'react';
import axios from "axios";
const urlPrefix = "http://127.0.0.1:5000"
const url_dataset = "/api/datasets"
const url_dataset_choosen = "/api/dataset_choosen/"

function Dataset({ setFormFrame, setDisplayData }) {
    const [dataset, setDataset] = useState([])
    useEffect(() => {
        // Request for field list
        axios.get(urlPrefix + url_dataset).then((response) => {
            setDataset(response.data)
        })
    }, [])
    // console.log(list)
    // console.log(resetSwitch)
    return (
        // <div>
        //     {
        //         list.map((item) => (
        //             <span>
        //                 {item} /
        //             </span>
        //         ))
        //     }
        // </div>
        // <label for="x_axis"> X axis:
        //     <select id='x_axis' name="x">
        //         {
        //             list.map((item) => (
        //                 <option value={item}>{item}</option>
        //             ))
        //         }
        //     </select>
        // </label>


        <Paper elevation={10} className='dataset' style={{ backgroundColor: "#feeeed" }}>

            <br></br>
            <FormControl required sx={{ m: 1, minWidth: 120 }} >
                <InputLabel id="dataset-required-label">Dataset</InputLabel>
                <Select
                    labelId="dataset-required-label"
                    id="dataset-required"
                    // value=''
                    defaultValue={''}
                    label="dataset *"
                    name="dataset"
                    onChange={(event) => {
                        setFormFrame('dataset retrieving')
                        setDisplayData()
                        let dataset_name = event.target.value
                        axios.get(urlPrefix + url_dataset_choosen + dataset_name).then((response) => {
                            // console.log("groupBy return", typeof (response.data))
                            console.log(response)
                            setFormFrame(response.data)
                            // if (resetSwitch)
                            // {
                            //     setResetSwitch(false)
                            // }
                            // else{
                            //     setResetSwitch(true)
                            // }
                            
                            // const updatedFormData = {...formDataCurrent}
                            // updatedFormData.field = ''
                            // updatedFormData.filter = { "categorical": {}, "continuous": {} }
                            // updatedFormData.group_by = []
                            // updatedFormData.aggregate = []

                            // setFormDataCurrent(updatedFormData)
                            //  console.log(GroupBy_list)
                        })

                    }}
                >
                    {
                        dataset.map((item) => (
                            <MenuItem value={item} key={item}>{item}</MenuItem>
                        ))
                    }


                </Select>
            </FormControl>
            <br></br>

        </Paper>


    )

}

export default Dataset;