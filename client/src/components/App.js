import React from "react";
import { Layout, Typography, Row, Col } from "antd";
import "antd/dist/antd.css";

// import AudioUpload from "./AudioUpload";
import AudioRecord from "./AudioRecord";
import TrackList from "./TrackList";

const { Title } = Typography;

export const App = () => {
    const [file, setFile] = React.useState(null);
    const [tracks, setTracks] = React.useState([]);

    return (
        <Layout>
            <Layout.Content style={{ width: "100%", maxWidth: 800, margin: "2rem auto" }}>
                <Title>Search audio</Title>

                <section>
                    <Row>
                        <Col xs={24} sm={12}>
                            {/* <Upload /> */}
                        </Col>
                        <Col xs={24} sm={12}>
                            <AudioRecord />
                        </Col>
                    </Row>
                </section>

                <TrackList tracks={tracks} />
            </Layout.Content>
        </Layout>
    );
};

export default App;
