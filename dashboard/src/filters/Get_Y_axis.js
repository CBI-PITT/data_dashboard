import * as React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
function Get_Y_axis({list, formData}) {
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
            // <label for="y_axis"> Y axis:
            //     <select id='y_axis' name="y">
            //         {
            //             list.map((item) => (
            //                 <option value={item}>{item}</option>
            //             ))
            //         }
            //     </select>
            // </label>
            <FormControl required sx={{ m: 1, minWidth: 120 }}>
                <InputLabel id="y-axis-required-label">Y axis</InputLabel>
                <Select
                    labelId="y-axis-required-label"
                    id="y-axis-required"
                    // value=''
                    defaultValue={''}
                    label="Y axis *"
                    onChange={(event) => {
                        console.log("component", event.target)
                        formData.y = event.target.value
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
export default Get_Y_axis;