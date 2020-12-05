import React from 'react';
import { Button, Typography } from 'antd';
import { AudioOutlined } from '@ant-design/icons';

const { Text } = Typography;

const State = {
    INIT: 'init',
    RECORDING: 'recording',
    SEARCHING: 'searching',
};

const AudioRecord = ({ isSearching, upload }) => {
    const [state, setState] = React.useState(State.INIT);
    const [hasSearched, setSearched] = React.useState(false);

    const recorderRef = React.useRef(null);
    const streamRef = React.useRef(null);
    const chunksRef = React.useRef([]);

    const initRecorder = React.useCallback(async () => {
        if (!navigator.mediaDevices) {
            console.error('recording not supported');
            return;
        }

        streamRef.current = await navigator.mediaDevices.getUserMedia({ audio: true });
        recorderRef.current = new MediaRecorder(streamRef.current);

        recorderRef.current.ondataavailable = (e) => {
            chunksRef.current.push(e.data);
        };

        recorderRef.current.onstop = () => {
            const blob = new Blob(chunksRef.current, { type: 'audio/webm;codecs=opus' });
            const file = new File([blob], 'recording.webm');
            upload(file);
            chunksRef.current = [];
        };
    }, [upload]);

    const transition = React.useCallback(async () => {
        switch (state) {
            case State.INIT:
                if (!recorderRef.current) {
                    await initRecorder();
                }

                recorderRef.current.start();
                setState(State.RECORDING);
                break;

            case State.RECORDING:
                recorderRef.current.stop();
                streamRef.current.getTracks().forEach((track) => track.stop());
                setState(State.SEARCHING);
                break;

            case State.SEARCHING:
                setState(State.INIT);
                setSearched(false);
                recorderRef.current = null;
                streamRef.current = null;
                break;

            default:
                console.error('Undefiend state transition');
        }
    }, [state, setState, setSearched, initRecorder]);

    React.useEffect(() => {
        if (!hasSearched && isSearching && state === State.SEARCHING) {
            setSearched(true);
        }
    }, [isSearching, hasSearched, state]);

    React.useEffect(() => {
        if (!isSearching && hasSearched) {
            transition();
        }
    }, [isSearching, hasSearched, transition]);

    return (
        <div style={{ display: 'flex', flexDirection: 'column' }}>
            <Button
                type="primary"
                disabled={isSearching}
                loading={state === State.SEARCHING}
                icon={<AudioOutlined />}
                onClick={() => transition()}
            >
                {state === State.INIT && 'Record an audio'}
                {state === State.RECORDING && 'Recording...'}
                {state === State.SEARCHING && 'Searching...'}
            </Button>
            {state === State.RECORDING && (
                <Text style={{ fontSize: '0.75rem', marginTop: '0.25rem' }}>Record at least 4 seconds</Text>
            )}
        </div>
    );
};

export default AudioRecord;
