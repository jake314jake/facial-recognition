import React, { useEffect, useRef, useState } from 'react';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import Webcam from 'react-webcam';
import axios from 'axios';

const Access = () => {
  const webcamRef = useRef(null);
  const [imageSrc, setImageSrc] = useState(null);
  const [loading, setLoading] = useState(false);
  const [resultImageSrc, setResultImageSrc] = useState(null);

  useEffect(() => {
    if (imageSrc) {
      setLoading(true);
      const formDataToSend = new FormData();
      formDataToSend.append('imageSrc', imageSrc);
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/verify_access/',
        data: formDataToSend,
        headers: { 'Content-Type': 'multipart/form-data' },
      })
        .then(response => {
          console.log(response.data);
          // Set the result image received from the server
          setResultImageSrc(`data:image/png;base64,${response.data.image}`);
        })
        .catch(error => {
          console.error('Error verifying access:', error);
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [imageSrc]);

  const handleCapture = () => {
    setLoading(true);
    const image = webcamRef.current.getScreenshot();
    setImageSrc(image);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100vh' }}>
      {loading ? (
        <CircularProgress
          style={{ marginTop: '20vh' }}
          size={100}
        />
      ) : (
        <>
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            width={640}
            height={480}
            mirrored={true}
          />
          <div style={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <Button
              onClick={handleCapture}
              variant="contained"
              color="primary"
              disabled={loading} // Disable the button during loading
            >
              Capture
            </Button>
            {resultImageSrc && (
              <img
                src={resultImageSrc}
                alt="Result"
                style={{ marginTop: '20px', maxWidth: '60vh', maxHeight: '60vh' }}
              />
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Access;
