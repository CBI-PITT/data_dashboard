import React from 'react';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
function ParaCheck({ isCheckedPara,setIsCheckedPara }) {
    const handleCheckboxChange = (event) => {
        setIsCheckedPara((prevChecked) => !prevChecked);
      };
    
      return (
        <FormControlLabel
          control={
            <Checkbox
              checked={isCheckedPara}
              onChange={handleCheckboxChange}
              color="primary" // Use "default" for a default color
            />
          }
          label="Error bar & N value"
        />
      );
}

export default ParaCheck;