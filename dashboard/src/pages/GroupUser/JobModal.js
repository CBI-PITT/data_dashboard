import React, { useState } from 'react';
import ImageAnalysisForm from './Form'

const Modal = ({ isOpen, onClose }) => {
  const [formData, setFormData] = useState(/* initial form data here */);

  const handleInputChange = (e) => {
    // Handle form input changes
  };

  const handleSubmit = () => {
    // Handle form submission
  };

  return (
    <div className={`modal ${isOpen ? 'open' : 'closed'}`}>
      <div className="modal-content">
        <ImageAnalysisForm/>
        <button onClick={onClose}>Close</button>
        <button onClick={handleSubmit}>Create job</button>
      </div>
    </div>
  );
};

export default Modal;