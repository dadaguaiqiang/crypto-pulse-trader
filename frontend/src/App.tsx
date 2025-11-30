import React from 'react';
import { Layout, Menu, Typography } from 'antd';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import MarketOverview from './pages/MarketOverview';
import './App.css';

const { Header, Content, Footer } = Layout;
const { Title } = Typography;

function App() {
  return (
    <Router>
      <Layout className="layout">
        <Header>
          <div className="logo">
            <Title level={3} style={{ color: 'white', margin: 0 }}>
              CryptoPulse Trader
            </Title>
          </div>
          <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
            <Menu.Item key="1">
              <Link to="/">市场概览</Link>
            </Menu.Item>
          </Menu>
        </Header>

        <Content style={{ padding: '0 50px', marginTop: 20 }}>
          <div className="site-layout-content">
            <Routes>
              <Route path="/" element={<MarketOverview />} />
            </Routes>
          </div>
        </Content>

        <Footer style={{ textAlign: 'center' }}>
          CryptoPulse Trader ©2023 - 开发中
        </Footer>
      </Layout>
    </Router>
  );
}

export default App;