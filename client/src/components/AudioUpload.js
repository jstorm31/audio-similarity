import React from "react";
import { Typography, Upload } from "antd";
// import { InboxOutlined } from "@ant-design/icons";

const { Title, Text } = Typography;

const AudioUpload = () => (
    <>
        <Title level={2}>Upload a file</Title>
        <Upload.Dragger name="audiotrack" accept=".mp3,.mp4,.wav,.m4a" showUploadList={false}>
            {/* <InboxOutlined /> */}
            <Text>Upload an audiofile</Text>
        </Upload.Dragger>
    </>
);

export default AudioUpload;
