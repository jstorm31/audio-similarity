import React from "react";
import { Upload, Button } from "antd";
import { UploadOutlined } from "@ant-design/icons";

const AudioUpload = ({ isUploading, upload }) => (
    <Upload
        name="audiotrack"
        accept=".mp3,.mp4,.wav,.m4a"
        showUploadList={false}
        customRequest={() => null}
        onChange={({ file }) => upload(file)}
    >
        <Button icon={<UploadOutlined />} loading={isUploading} disabled={isUploading}>
            {isUploading ? "Searching..." : "Upload an audiofile"}
        </Button>
    </Upload>
);

export default AudioUpload;
