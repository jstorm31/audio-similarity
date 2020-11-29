import React from 'react';
import { Typography, Table } from 'antd';
import PlayAudio from './PlayAudio';

const { Title } = Typography;

const columns = [
    {
        title: 'Filename',
        dataIndex: 'filename',
        key: 'filename',
    },
    {
        title: 'Similarity',
        dataIndex: 'similarity',
        key: 'similarity',
        render: (similarity) => Number(similarity).toFixed(2),
    },
    {
        key: 'action',
        render: (_, { filename }) => <PlayAudio filename={filename} />,
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
