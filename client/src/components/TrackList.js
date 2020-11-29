import React from "react";
import { Typography, Table, Button } from "antd";
import { PlayCircleOutlined } from "@ant-design/icons";

const { Title, Text } = Typography;

const columns = [
    {
        title: "Filename",
        dataIndex: "filename",
        key: "filename",
    },
    {
        title: "Similarity",
        dataIndex: "similarity",
        key: "similarity",
    },
    {
        key: "action",
        render: (_, { filename }) => <Button shape="circle" icon={<PlayCircleOutlined />} />,
    },
];

const TrackList = ({ tracks }) => (
    <>
        <Title level={2}>Best matches</Title>

        <section className="section section--table">
            <Table columns={columns} dataSource={tracks} rowKey="filename" pagination={false} />
        </section>
    </>
);

export default TrackList;
