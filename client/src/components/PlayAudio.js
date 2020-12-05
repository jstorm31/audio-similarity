import React from 'react';
import { Button } from 'antd';
import { CaretRightFilled, PauseOutlined } from '@ant-design/icons';

const PlayAudio = ({ audio: audioProp, filename }) => {
    const [audio, setAudio] = React.useState(null);
    const [playing, setPlaying] = React.useState(false);

    React.useEffect(() => {
        if (filename) {
            const url = `${process.env.REACT_APP_SERVER_URL}/audiotracks/${filename}`;
            setPlaying(false);
            setAudio(new Audio(url));
        }
    }, [filename]);

    React.useEffect(() => {
        if (audioProp) {
            setPlaying(false);
            setAudio(audioProp);
        }
    }, [audioProp]);

    const resetAudio = () => {
        setPlaying(false);
        audio.pause();
        audio.currentTime = 0;
    };

    const handleClick = () => {
        if (!audio) {
            console.warn('Audio not initialiized');
            return;
        }

        if (!playing) {
            setPlaying(true);
            audio.play();
        } else {
            resetAudio();
        }
    };

    React.useEffect(() => {
        let timeout;

        if (playing && audio) {
            timeout = setTimeout(() => {
                resetAudio();
            }, 10000);
        }

        return () => clearTimeout(timeout);
    }, [playing, audio]);

    return <Button shape="circle" icon={playing ? <PauseOutlined /> : <CaretRightFilled />} onClick={handleClick} />;
};

export default PlayAudio;
