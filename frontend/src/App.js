import './App.css';
import logoImage from './IconOnly_Transparent_NoBuffer.png';
import logoText from './TextOnly_NoBuffer.png';
import React, {useState} from 'react';

const apiUrl = process.env.REACT_APP_API_URL;

function App() {
    const [inputValue, setInputValue] = useState('');
    const [response, setResponse] = useState('');
    const [error, setError] = useState('');
    const [isValidUrl, setIsValidUrl] = useState(false);

    const isUrlValid = (url) => {
      // Regular expression for validating URLs
      const urlPattern = /^(ftp|http|https):\/\/[^ "]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?$/;

      // Test the URL against the pattern
      return urlPattern.test(url);
    };

    const handleInputChange = (e) => {
        const url = e.target.value;

        if (url && isUrlValid(url)) {
            setIsValidUrl(true);
        } else {
            setIsValidUrl(false);
        }

        if (url && !isUrlValid(url)) {
            // show error or messahe to hint the user
        }

        setInputValue(url);
    };

    const handleSubmit = async () => {
        try {
            const response = await fetch(`${apiUrl}/breve-me`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // 'Authorization': `Bearer ${apiToken}`
                },
                body: JSON.stringify({url: inputValue})
            });

            if (!response.ok) {
              throw new Error('Request failed: ' + response.status);
            }

            const data = await response.json();
            setError('');
            setResponse(data.breve_url);
        } catch (error) {
            setResponse('');
            setError('An error occurred. Please try again.');
        }
    };

    const handleResponseClick = () => {
        if (response) {
            window.open(response, '_blank'); // Open response URL in a new tab
        }
    };

    return (
        <div className="Container">
            <div className="LogoContainer">
                <img src={logoImage} alt="Logo" className="Logo"/>
                <img src={logoText} alt="Logo" className="LogoText"/>
            </div>
            <div className="InputContainer">
                <input
                    type="text"
                    value={inputValue}
                    onChange={handleInputChange}
                    className="InputField"
                />
                <button
                    disabled={!isValidUrl || !inputValue}
                    onClick={handleSubmit}
                    className="SubmitButton">
                    Breve me
                </button>
            </div>
            <div>
                {error && <p className="ErrorMessage">{error}</p>}
            </div>
            <div>
                {
                    response && (
                        <p className="Response" onClick={handleResponseClick}>{response}</p>
                    )
                }
            </div>
        </div>

    );
}

export default App;
