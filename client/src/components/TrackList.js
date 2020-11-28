import React from "react";
import { Typography } from "antd";

const { Title } = Typography;

const TrackList = ({ tracks }) => (
    <section>
        <Title level={2}>Best matches</Title>
        {tracks.map((track) => (
            <span>{track}</span>
        ))}
    </section>
);

export default TrackList;
