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

    const handleClick = () => {
        if (!audio) {
            console.warn('Audio not initialiized');
            return;
        }

        if (!playing) {
            setPlaying(true);
            audio.play();
        } else {
            setPlaying(false);
            audio.pause();
        }
    };

    return <Button shape="circle" icon={playing ? <PauseOutlined /> : <CaretRightFilled />} onClick={handleClick} />;
};

export default PlayAudio;
