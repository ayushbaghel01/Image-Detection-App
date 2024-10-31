import React from 'react';
import axios from 'axios';
import './ResultDisplay.css';

const ResultDisplay = ({ result }) => {
    const handleDownload = async () => {
        try {
            const response = await axios.get(`http://localhost:5000/yolo/image/${result.id}`, {
                responseType: 'blob',
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `annotated_image_${result.id}.png`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error("Error downloading image:", error);
        }
    };

    const downloadJSON = () => {
        const json = JSON.stringify(result.labels, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'detection_results.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };
    
    return (
        <div className="ResultsContainer">
            <h2>Detection Results</h2>
            <div className="ResultsContent">
                <div>
                    <pre className="JSONText">{JSON.stringify({id: result.id,labels: result.labels},null, 2)}</pre>
                    <span className="JSONDownloadLink" onClick={downloadJSON}>
                        Download JSON
                    </span>
                </div>
                {result.imageUrl && (
                    <img 
                        src={result.imageUrl} 
                        alt="Annotated" 
                        className="ResultsImage"
                    />
                )}
            </div>
            {result.imageUrl && (
                <button 
                    onClick={handleDownload} 
                    className="DownloadButton"
                >
                    Download Annotated Image
                </button>
            )}
        </div>
    );
};

export default ResultDisplay;