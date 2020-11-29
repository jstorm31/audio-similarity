const upload = async (file) => {
    const data = new FormData();
    data.append('audiotrack', file);

    const response = await fetch(`${process.env.REACT_APP_SERVER_URL}/search`, {
        method: 'POST',
        body: data,
    });
    const body = await response.json();

    if (response.status !== 200) {
        throw new Error(body.error);
    }
    return body;
};

export default upload;
