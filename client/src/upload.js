const upload = async (file, settings) => {
    const { k, engine } = settings;

    const data = new FormData();
    data.append('audiotrack', file);
    data.append('top_k', k);
    data.append('engine', engine);

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
