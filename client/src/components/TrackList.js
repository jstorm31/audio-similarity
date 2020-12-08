import React from 'react';
import { Typography, Table } from 'antd';
import PlayAudio from './PlayAudio';

const { Title, Text } = Typography;

const columns = (engine) => [
    {
        title: 'Filename',
        dataIndex: 'filename',
        key: 'filename',
    },
    {
        title: engine === 'mfcc' ? 'Distance' : 'Similarity',
        dataIndex: engine === 'mfcc' ? 'distance' : 'similarity',
        key: engine === 'mfcc' ? 'distance' : 'similarity',
        render: (value) => Number(value).toFixed(engine === 'mfcc' ? 4 : 3),
    },
    {
        key: 'action',
        render: (_, { filename }) => <PlayAudio filename={filename} />,
    },
];

const TrackList = ({ tracks, searchTime, engine }) => (
    <>
        <Title level={2}>Best matches</Title>
        <Text>Search time: {Number(searchTime).toFixed(2)} s</Text>

        <section className="section section--table">
            <Table columns={columns(engine)} dataSource={tracks} rowKey="filename" pagination={false} />
        </section>
    </>
);

export default TrackList;
