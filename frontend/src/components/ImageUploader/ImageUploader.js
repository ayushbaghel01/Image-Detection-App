import React, { useState } from 'react';
import axios from 'axios';
import './ImageUploader.css';

const ImageUploader = ({ onResult }) => {
    const [file, setFile] = useState(null);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await axios.post("http://localhost:5000/yolo/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });
            const { id, labels } = response.data;
            onResult({ id, labels });

            const imageResponse = await axios.get(`http://localhost:5000/yolo/image/${id}`, {
                responseType: "blob"
            });
            const imageUrl = URL.createObjectURL(imageResponse.data);
            onResult({ id, labels, imageUrl });
        } catch (error) {
            console.error("Error uploading image:", error.response ? error.response.data : error.message);
        }
    };

    return (
        <div className="UploadContainer">
            <input 
                type="file" 
                onChange={handleFileChange} 
                accept="image/*" 
                className="FileInput" 
            />
            <button 
                onClick={handleUpload} 
                disabled={!file} 
                className="Button"
            >
                Detect Objects
            </button>
        </div>
    );
};

export default ImageUploader;
