import React, { useEffect, useState } from 'react';
import { Card, Table, Tag, Spin, Alert, Typography } from 'antd';
import { TickerData } from '../types/market';
import { marketAPI } from '../services/api';

const { Title } = Typography;

const MarketOverview: React.FC = () => {
  const [tickers, setTickers] = useState<Record<string, TickerData>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTickers = async () => {
      try {
        setLoading(true);
        const data = await marketAPI.getTickers();
        setTickers(data);
        setError(null);
      } catch (err) {
        setError('获取市场数据失败');
        console.error('Error fetching tickers:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTickers();
  }, []);

  const columns = [
    {
      title: '交易对',
      dataIndex: 'symbol',
      key: 'symbol',
    },
    {
      title: '价格',
      dataIndex: 'price',
      key: 'price',
      render: (price: number) => `$${price.toLocaleString()}`,
    },
    {
      title: '24h涨跌幅',
      dataIndex: 'change_24h',
      key: 'change_24h',
      render: (change: number) => (
        <Tag color={change >= 0 ? 'green' : 'red'}>
          {change >= 0 ? '+' : ''}{change}%
        </Tag>
      ),
    },
    {
      title: '24h交易量',
      dataIndex: 'volume_24h',
      key: 'volume_24h',
      render: (volume: number) => `$${(volume / 1000000).toFixed(2)}M`,
    },
  ];

  const dataSource = Object.values(tickers).map(ticker => ({
    key: ticker.symbol,
    ...ticker,
  }));

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
        <div style={{ marginTop: 16 }}>加载市场数据中...</div>
      </div>
    );
  }

  return (
    <div>
      <Title level={2}>市场概览</Title>

      {error && (
        <Alert
          message="错误"
          description={error}
          type="error"
          showIcon
          style={{ marginBottom: 16 }}
        />
      )}

      <Card>
        <Table
          columns={columns}
          dataSource={dataSource}
          pagination={false}
          size="middle"
        />
      </Card>

      <div style={{ marginTop: 16, textAlign: 'center', color: '#999' }}>
        <p>这是基础框架展示，真实市场数据将在后续 Sprint 中接入</p>
      </div>
    </div>
  );
};

export default MarketOverview;