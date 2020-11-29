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
    const [audio, setAudio] = React.useState(null);
    const [audioName, setAudioName] = React.useState('');
    const [tracks, setTracks] = React.useState([]);
    const [isSearching, setSearching] = React.useState(false);
    const [error, setError] = React.useState(null);

    const handleUpload = async (file) => {
        setSearching(true);
        setTracks([]);

        const url = URL.createObjectURL(file);
        setAudio(new Audio(url));
        setAudioName(file.name);

        try {
            const response = await upload(file);
            setTracks(response);
            setError(null);
        } catch (error) {
            setError(error.message);
        } finally {
            setSearching(false);
        }
    };

    return (
        <Layout>
            <Layout.Content className="content">
                <Title style={{ marginBottom: '0.5rem' }}>Search audio</Title>
                <Text>Record an audio or upload a file to search similar audiotracks.</Text>

                <section style={{ marginTop: '1rem' }} className="section">
                    <form>
                        <Row gutter={[16, 16]}>
                            <Col xs={24} sm={12}>
                                <div className="center">
                                    <AudioRecord isSearching={isSearching} upload={handleUpload} />
                                </div>
                            </Col>
                            <Col xs={24} sm={12}>
                                <div className="center">
                                    <AudioUpload isSearching={isSearching} upload={handleUpload} />
                                </div>
                            </Col>
                        </Row>

                        {audio && audioName && (
                            <div className="sample">
                                <Text style={{ marginRight: '1rem' }}>{audioName}</Text>
                                <PlayAudio audio={audio} />
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
