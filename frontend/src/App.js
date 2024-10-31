import React, { useState } from 'react';
import ImageUploader from './components/ImageUploader/ImageUploader';
import ResultDisplay from './components/ResultDisplay/ResultDisplay';
import Header from './components/header/Header';
const App = () => {
    const [result, setResult] = useState(null);

    const handleResult = (data) => {
        setResult(data);
    };

    return (
        <div>
            <Header />
            <ImageUploader onResult={handleResult} />
            {result && <ResultDisplay result={result} />}

        </div>
    );
};

export default App;
