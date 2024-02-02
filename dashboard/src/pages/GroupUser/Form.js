import React, { useState } from 'react';

function ImageAnalysisForm() {
  // State to store user selections
  const [selectedFile, setSelectedFile] = useState('');
  const [selectedFolder, setSelectedFolder] = useState('');
  const [preProcessChecked, setPreProcessChecked] = useState(false);
  const [extractTiffsChecked, setExtractTiffsChecked] = useState(false);
  const [alignChecked, setAlignChecked] = useState(false);
  const [spotCountChecked, setSpotCountChecked] = useState(false);
  const [customMethodChecked, setCustomMethodChecked] = useState(false);
  // const [preProcessMethod, setPreProcessMethod] = useState('');
  const [alignMethod, setAlignMethod] = useState('');
  const [spotCountMethod, setSpotCountMethod] = useState('');
  const [customMethod, setCustomMethod] = useState('');
  const [preProcessComputer, setPreProcessComputer] = useState('pollux');
  const [extractTiffsComputer, setExtractTiffsComputer] = useState('pollux');
  const [alignComputer, setAlignComputer] = useState('pollux');
  const [spotCountComputer, setSpotCountComputer] = useState('pollux');
  const [customMethodComputer, setCustomMethodComputer] = useState('pollux');

  // Handler for file selection
  const handleFileSelect = (e) => {
//    setSelectedFile(e.target.files[0]);
  };
  
  // Handler for folder selection
  const handleFolderSelect = (e) => {
//    setSelectedFolder(e.target.files[0]);
  };

function downloadJSON(data, filename) {
  // Step 1: Create a JSON object
  const jsonData = JSON.stringify(data, null, 2); // null and 2 for pretty formatting

  // Step 2: Convert JSON object to string

  // Step 3: Create a Blob from the string
  const blob = new Blob([jsonData], { type: 'application/json' });

  // Step 4: Create a download link
  const link = document.createElement('a');
  link.href = window.URL.createObjectURL(blob);
  link.download = filename;

  // Step 5: Trigger a click on the download link
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

  // Handler for form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // Perform task creation here with the selected options
    // console.log('Selected File:', selectedFile);
    // console.log('Selected Folder:', selectedFolder);
    // console.log('Pre-process Checked:', preProcessChecked);
    // console.log('Align Checked:', alignChecked);
    // console.log('Spot Count Checked:', spotCountChecked);
    // console.log('Pre-process Method:', preProcessMethod);
    // console.log('Align Method:', alignMethod);
    // console.log('Spot Count Method:', spotCountMethod);
    // console.log('Pre-process Computer:', preProcessComputer);
    // console.log('Align Computer:', alignComputer);
    // console.log('Spot Count Computer:', spotCountComputer);

    // Initialize an empty object to store form data
    const formData = {};

    // Populate the object with values from the state
    formData.selectedFile = selectedFile;
    formData.selectedFolder = selectedFolder;
    formData.extractTiffsChecked = extractTiffsChecked;
    formData.preProcessChecked = preProcessChecked;
    formData.alignChecked = alignChecked;
    formData.spotCountChecked = spotCountChecked;
    // formData.preProcessMethod = preProcessMethod;
    formData.alignMethod = alignMethod;
    formData.spotCountMethod = spotCountMethod;
    formData.customMethod = customMethod;
    formData.preProcessComputer = preProcessComputer;
    formData.extractTiffsComputer = extractTiffsComputer;
    formData.alignComputer = alignComputer;
    formData.spotCountComputer = spotCountComputer;
    formData.customMethodComputer = customMethodComputer;

    // Serialize the object to JSON
//    const jsonData = JSON.stringify(formData);
//    console.log('Form Data JSON:', jsonData);
    downloadJSON(formData, "example.json")
  };

  return (
    <div className="dark-widget">
      <h2 className="dark-heading">New job</h2>
      <form onSubmit={handleSubmit} className="dark-form">
        <div className="dark-input-group">
          <label>Select a file to process:</label>
          <input type="text" placeholder="/path/to/input.ims" onChange={handleFileSelect} className="dark-input" />
        </div>

        <div className="dark-input-group">
          <label>Select output folder:</label>
          <input type="text" placeholder="/path/to/output/folder" onChange={handleFolderSelect} className="dark-input" />
        </div>

        <div className="dark-input-group">
          <label className="dark-label dark-checkbox-label">Extract tiffs:</label>
          <input type="checkbox" checked={extractTiffsChecked} onChange={() => setExtractTiffsChecked(!extractTiffsChecked)} className="dark-checkbox" />
          {extractTiffsChecked && (
            <select onChange={(e) => setExtractTiffsComputer(e.target.value)} className="dark-select">
              <option value="pollux">pollux</option>
              <option value="deneb">deneb</option>
            </select>
          )}
        </div>

        <div className="dark-input-group">
          <label className="dark-label dark-checkbox-label">Pre-process:</label>
          <input type="checkbox" checked={preProcessChecked} onChange={() => setPreProcessChecked(!preProcessChecked)} className="dark-checkbox" />
          {/* <select multiple onChange={(e) => setPreProcessMethod(Array.from(e.target.selectedOptions, (option) => option.value))} className="dark-select">
            <option value="contrast">stretch contrast</option>
            <option value="background">remove background</option>
          </select> */}
          {preProcessChecked && (
              <select onChange={(e) => setPreProcessComputer(e.target.value)} className="dark-select">
                <option value="pollux">pollux</option>
                <option value="deneb">deneb</option>
              </select>
          )}
        </div>

        <div className="dark-input-group">
          <label className="dark-label dark-checkbox-label">Align:</label>
          <input type="checkbox" checked={alignChecked} onChange={() => setAlignChecked(!alignChecked)} className="dark-checkbox" />
          {alignChecked && (
            <>
              <select multiple onChange={(e) => setAlignMethod(Array.from(e.target.selectedOptions, (option) => option.value))} className="dark-select">
                <option value="ants">ants</option>
                <option value="brainreg">brainreg</option>
              </select>
              <select onChange={(e) => setAlignComputer(e.target.value)} className="dark-select">
                <option value="pollux">pollux</option>
                <option value="deneb">deneb</option>
              </select>
            </>
          )}
        </div>

        <div className="dark-input-group">
          <label className="dark-label dark-checkbox-label">Spot Count:</label>
          <input type="checkbox" checked={spotCountChecked} onChange={() => setSpotCountChecked(!spotCountChecked)} className="dark-checkbox" />
          {spotCountChecked && (
            <>
              <select multiple onChange={(e) => setSpotCountMethod(Array.from(e.target.selectedOptions, (option) => option.value))} className="dark-select">
                <option value="cellfinder">cellfinder</option>
                <option value="deepblink">deepblink</option>
              </select>
              <select onChange={(e) => setSpotCountComputer(e.target.value)} className="dark-select">
                <option value="pollux">pollux</option>
                <option value="deneb">deneb</option>
              </select>
            </>
          )}
        </div>

        <div className="dark-input-group">
          <label className="dark-label dark-checkbox-label">Custom method:</label>
          <input type="checkbox" checked={customMethodChecked} onChange={() => setCustomMethodChecked(!customMethodChecked)} className="dark-checkbox" />
          {customMethodChecked && (
            <>
              <input
                type="text"
                placeholder="Enter custom method name"
                value={customMethod}
                onChange={(e) => setCustomMethod(e.target.value)}
                className="dark-input"
              />
              <select
                value={customMethodComputer}
                onChange={(e) => setCustomMethodComputer(e.target.value)}
                className="dark-select"
              >
                <option value="pollux">pollux</option>
                <option value="deneb">deneb</option>
              </select>
            </>
          )}
        </div>
        <button type="submit" className="dark-button">Create Job</button>
      </form>
    </div>
  );
}

export default ImageAnalysisForm;
