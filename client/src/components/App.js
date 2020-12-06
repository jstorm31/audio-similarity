import React from 'react';
import { Layout, Typography, Row, Col, Alert } from 'antd';
import 'antd/dist/antd.css';

import './App.css';
import AudioUpload from './AudioUpload';
import AudioRecord from './AudioRecord';
import TrackList from './TrackList';
import upload from '../upload';
import PlayAudio from './PlayAudio';
import Settings from './Settings';

const { Title, Text } = Typography;

export const App = () => {
    const [audio, setAudio] = React.useState(null);
    const [audioName, setAudioName] = React.useState('');
    const [tracks, setTracks] = React.useState([]);
    const [searchTime, setSearchTime] = React.useState(0);
    const [isSearching, setSearching] = React.useState(false);
    const [error, setError] = React.useState(null);
    const [settings, setSettings] = React.useState({ k: 5, engine: 'chromaprint' });

    const handleUpload = async (file) => {
        setSearching(true);
        setTracks([]);

        const url = URL.createObjectURL(file);
        setAudio(new Audio(url));
        setAudioName(file.name);

        try {
            const { data, time } = await upload(file, settings);
            setTracks(data);
            setSearchTime(time);
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
                <Text>Record an audio or upload a file to search for similar audiotracks.</Text>

                <section className="section">
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
                    </form>

                    {audio && audioName && (
                        <div className="sample">
                            <Text style={{ marginRight: '1rem' }}>{audioName}</Text>
                            <PlayAudio audio={audio} />
                        </div>
                    )}

                    <Settings settings={settings} setSettings={setSettings} />

                    {error && <Alert type="error" message={error} style={{ marginTop: '2rem' }} />}
                </section>

                {tracks.length > 0 && <TrackList tracks={tracks} searchTime={searchTime} />}
            </Layout.Content>
        </Layout>
    );
};

export default App;
