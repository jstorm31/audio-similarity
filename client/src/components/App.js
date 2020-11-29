import React from 'react';
import { Layout, Typography, Row, Col, Alert } from 'antd';
import 'antd/dist/antd.css';

import './App.css';
import AudioUpload from './AudioUpload';
import AudioRecord from './AudioRecord';
import TrackList from './TrackList';
import upload from '../upload';
import PlayAudio from './PlayAudio';

const { Title, Text } = Typography;

export const App = () => {
    const [filename, setFilename] = React.useState(null);
    const [tracks, setTracks] = React.useState([]);
    const [isUploading, setUploading] = React.useState(false);
    const [error, setError] = React.useState(null);

    const handleUpload = async (file) => {
        setUploading(true);
        setTracks([]);
        setFilename(file.name);

        try {
            const response = await upload(file.originFileObj);
            setTracks(response);
            setError(null);
        } catch (error) {
            setError(error.message);
        } finally {
            setUploading(false);
        }
    };

    return (
        <Layout>
            <Layout.Content className="content">
                <Title>Search audio</Title>

                <section className="section">
                    <form>
                        <Row>
                            <Col xs={24} sm={12}>
                                <div className="center">
                                    <AudioRecord upload={handleUpload} />
                                </div>
                            </Col>
                            <Col xs={24} sm={12}>
                                <div className="center">
                                    <AudioUpload isUploading={isUploading} upload={handleUpload} />
                                </div>
                            </Col>
                        </Row>

                        {filename && (
                            <div className="sample">
                                <Text style={{ marginRight: '1rem' }}>{filename}</Text>
                                <PlayAudio filename={filename} />
                            </div>
                        )}

                        {error && <Alert type="error" message={error} style={{ marginTop: '2rem' }} />}
                    </form>
                </section>

                {tracks.length > 0 && <TrackList tracks={tracks} />}
            </Layout.Content>
        </Layout>
    );
};

export default App;
