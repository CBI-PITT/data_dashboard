import React, { useState } from 'react';
import ImageAnalysisForm from './Form'
import { Box, Modal } from "@mui/material";

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

const JobModal = ({ isOpen, onClose }) => {
  const [formData, setFormData] = useState(/* initial form data here */);

  const handleSubmit = () => {
    // Handle form submission
  };

  return (
  <Modal
    open={isOpen}
    onClose={onClose}
    aria-labelledby="modal-modal-title"
    aria-describedby="modal-modal-description"
  >
    <Box sx={style}>
    <div className={`modal ${isOpen ? 'open' : 'closed'}`}>
      <div className="modal-content">
        <ImageAnalysisForm/>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
    </Box>
  </Modal>
  );
};

export default JobModal;
