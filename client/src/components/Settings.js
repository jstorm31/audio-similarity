import React from 'react';
import { Typography, Form, InputNumber, Radio } from 'antd';

const { Title } = Typography;

const Settings = ({ settings: { engine, k }, setSettings }) => (
    <Form layout="vertical">
        <Title level={3}>Settings</Title>
        <Form.Item label="Engine">
            <Radio.Group onChange={(e) => setSettings({ k, engine: e.target.value })} value={engine}>
                <Radio value="chromaprint">Chromaprint - bit error</Radio>
                <Radio value="chromaprint_cc">Chromaprint - cross correlation</Radio>
                <Radio value="mfcc">MFCC</Radio>
            </Radio.Group>
        </Form.Item>
        <Form.Item label="Top k">
            <InputNumber min={1} max={20} value={k} onChange={(value) => setSettings({ engine, k: value })} />
        </Form.Item>
    </Form>
);

export default Settings;
