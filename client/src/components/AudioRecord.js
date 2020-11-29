import React from 'react';
import { Button } from 'antd';
import { AudioOutlined } from '@ant-design/icons';

const AudioRecord = ({ handleUpload }) => {
    return (
        <Button type="primary" icon={<AudioOutlined />}>
            Record an audio
        </Button>
    );
};

export default AudioRecord;
