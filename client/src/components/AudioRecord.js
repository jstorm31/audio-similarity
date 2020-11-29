import React from 'react';
import { Button } from 'antd';
import { AudioOutlined } from '@ant-design/icons';

const State = {
    INIT: 'init',
    RECORDING: 'recording',
    SEARCHING: 'searching',
};

const AudioRecord = ({ isSearching, upload }) => {
    const [state, setState] = React.useState(State.INIT);
    const [hasSearched, setSearched] = React.useState(false);
    const [chunks, setChunks] = React.useState([]);
    const recorderRef = React.useRef(null);

    const initRecorder = React.useCallback(async () => {
        if (!navigator.mediaDevices) {
            console.error('recording not supported');
            return;
        }

        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recorderRef.current = new MediaRecorder(stream);

        recorderRef.current.onstop = () => {
            console.log('stop');
            const blob = new Blob(chunks, { type: 'audio/webm;codecs=opus' });
            const file = new File([blob], 'recording.webm');

            upload(file);
            setChunks([]);
        };

        recorderRef.current.ondataavailable = (e) => {
            setChunks((prevChunks) => {
                prevChunks.push(e.data);
                return prevChunks;
            });
        };
    }, [chunks, upload]);

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
                setState(State.SEARCHING);
                break;

            case State.SEARCHING:
                setState(State.INIT);
                setSearched(false);
                recorderRef.current = null;
                break;

            default:
                console.error('Undefiend state transition');
        }
    }, [state, setState, setSearched, initRecorder]);

    React.useEffect(() => {
        if (!hasSearched && isSearching) {
            setSearched(true);
        }
    }, [isSearching, hasSearched]);

    React.useEffect(() => {
        if (!isSearching && hasSearched) {
            transition();
        }
    }, [isSearching, hasSearched, transition]);

    return (
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
    );
};

export default AudioRecord;
