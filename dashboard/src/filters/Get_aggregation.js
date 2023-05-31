import * as React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';


function Get_Aggregation({list,formData}) {
    // console.log(list)
    if (list !== undefined) {
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
            // <label for="aggregation">Aggregation:
            //     <select id='aggregation' name="aggregate" >
            //         {
            //             list.map((item) => (
            //                 <option value={item}>{item}</option>
            //             ))
            //         }
            //     </select>
            // </label>
            <FormControl required sx={{ m: 1, minWidth: 120 }}>
                <InputLabel id="aggregation-required-label">Aggregation</InputLabel>
                <Select
                    labelId="aggregation-required-label"
                    id="aggregation-required"
                    // value=''
                    defaultValue={''}
                    label="aggregation *"
                    onChange={(event) => {
                        console.log("component", event.target)
                        formData.aggregate = event.target.value
                    }}
                >
                    {
                        list.map((item) => (
                            <MenuItem value={item} key={item}>{item}</MenuItem>
                        ))
                    }


                </Select>

            </FormControl>
        )
    }
}

export default Get_Aggregation;