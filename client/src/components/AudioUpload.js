import React from 'react';
import { Upload, Button } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

const AudioUpload = ({ isSearching, upload }) => {
    const [isLoading, setLoading] = React.useState(false);

    React.useEffect(() => {
        if (!isSearching) {
            setLoading(false);
        }
    }, [isSearching]);

    const handleChange = ({ file }) => {
        setLoading(true);
        upload(file.originFileObj);
    };

    return (
        <Upload
            name="audiotrack"
            accept=".mp3,.mp4,.wav,.m4a"
            showUploadList={false}
            customRequest={() => null}
            onChange={handleChange}
        >
            <Button icon={<UploadOutlined />} loading={isLoading} disabled={isSearching}>
                {isLoading ? 'Searching...' : 'Upload an audiofile'}
            </Button>
        </Upload>
    );
};

export default AudioUpload;
