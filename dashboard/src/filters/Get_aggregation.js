import * as React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import OutlinedInput from '@mui/material/OutlinedInput';
import ListItemText from '@mui/material/ListItemText';
import Checkbox from '@mui/material/Checkbox';
const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
};
function Get_Aggregation({list,formData}) {
    const [aggregationSelected, setAggregationSelected] = React.useState([])
    const handleChange = (event) => {
        setAggregationSelected(event.target.value)
        formData.aggregate = event.target.value
    };
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
            // <FormControl required sx={{ m: 1, minWidth: 120 }}>
            //     <InputLabel id="aggregation-required-label">Aggregation</InputLabel>
            //     <Select
            //         labelId="aggregation-required-label"
            //         id="aggregation-required"
            //         // value=''
            //         defaultValue={''}
            //         label="aggregation *"
            //         name='aggregation'
            //         onChange={(event) => {
            //             console.log("component", event.target)
            //             // formData.aggregate.push(event.target.value)
            //             formData.aggregate = event.target.value
            //         }}
            //     >
            //         {
            //             list.map((item) => (
            //                 <MenuItem value={item} key={item}>{item}</MenuItem>
            //             ))
            //         }


            //     </Select>

            // </FormControl>
            <FormControl required sx={{ m: 1, width: '95%'}}>
            <InputLabel id="aggregation-multiple-checkbox-label">Aggregation</InputLabel>
            <Select
                labelId="aggregation-multiple-checkbox-label"
                id="aggregation-multiple-checkbox"
                multiple
                value={aggregationSelected}
                onChange={handleChange}
                input={<OutlinedInput label="Tag" />}
                renderValue={(selected) => selected.join(', ')}
                MenuProps={MenuProps}
            >
                {list.map((name) => (
                    <MenuItem key={name} value={name}>
                        <Checkbox checked={aggregationSelected.indexOf(name) > -1} />
                        <ListItemText primary={name} />
                    </MenuItem>
                ))}
            </Select>
        </FormControl>

        )
    }
}

export default Get_Aggregation;