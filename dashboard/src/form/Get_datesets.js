function Get_field({list,  form_Data,  set_FormData}) {
    
    // console.log(list)
    if (list !== undefined) {
        return (
            <FormControl required sx={{ m: 1, minWidth: 120 }}>
                <InputLabel id="x-axis-required-label">Field</InputLabel>
                <Select
                    labelId="x-axis-required-label"
                    id="x-axis-required"
                    // value=''
                    defaultValue={''}
                    label="field *"
                    name="field"
                    onChange={(event) => {
                        console.log("component", event.target)
                        
                        const updatedFormData = {...form_Data}
                        updatedFormData.field = event.target.value

                        // let newFormData = form_Data
                        
                        
                        // newFormData.field = event.target.value
                        set_FormData(updatedFormData)

                        // formData.field = event.target.value
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

export default Get_field;