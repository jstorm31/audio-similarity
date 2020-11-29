const upload = async (file) => {
    const data = new FormData();
    data.append("audiotrack", file);

    const response = await fetch("http://127.0.0.1:5000/search", {
        method: "POST",
        body: data,
    });
    const body = await response.json();

    if (response.status !== 200) {
        throw new Error(body.error);
    }
    return body;
};

export default upload;
