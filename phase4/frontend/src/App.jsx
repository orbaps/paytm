import { useState, useEffect, useRef } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
const USER_ID = 'user_1'

function App() {
  const [dashboard, setDashboard] = useState(null)
  const [trends, setTrends] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')
  const [modal, setModal] = useState(null)
  const [topupAmount, setTopupAmount] = useState('')
  const [notification, setNotification] = useState(null)
  const [cameraActive, setCameraActive] = useState(false)
  const [cameraError, setCameraError] = useState(null)
  const videoRef = useRef(null)
  
  const refresh = async () => {
    setLoading(true)
    try {
      await fetch(`${API_BASE}/analytics/user/${USER_ID}/run`, { method: 'POST' })
      const dashData = await (await fetch(`${API_BASE}/analytics/dashboard/${USER_ID}`)).json()
      const trendData = await (await fetch(`${API_BASE}/analytics/trends/${USER_ID}`)).json()
      setDashboard(dashData)
      setTrends(trendData)
      showNotification('Analytics updated successfully!', 'success')
    } catch (e) {
      console.error('Error loading dashboard:', e)
      showNotification('Error updating analytics', 'error')
    } finally {
      setLoading(false)
    }
  }

  const showNotification = (message, type = 'info') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  const openModal = (modalType) => {
    setModal(modalType)
  }

  const closeModal = () => {
    if (modal === 'camera') {
      stopCamera()
    }
    setModal(null)
    setTopupAmount('')
  }

  const handleTopup = () => {
    if (!topupAmount || parseFloat(topupAmount) <= 0) {
      showNotification('Please enter a valid amount', 'error')
      return
    }
    showNotification(`Successfully added Rs.${topupAmount} to your reserve!`, 'success')
    closeModal()
  }

  const handleQuickAction = (action) => {
    const messages = {
      'Transfer': 'Transfer feature coming soon! Navigate to your bank app or contact support.',
      'Request': 'Request money from friends. Share your payment link.',
      'Pay Bills': 'Pay utility bills, mobile recharge, insurance & more.',
      'Analytics': 'View detailed analytics and spending reports.',
      'Settings': 'Manage your account, security, and preferences.',
      'Support': 'Chat with our support team 24/7.'
    }
    showNotification(messages[action])
    openModal('action-' + action)
  }

  const startCamera = async () => {
    try {
      setCameraError(null)
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false
      })
      if (videoRef && videoRef.current) {
        videoRef.current.srcObject = stream
      }
      setCameraActive(true)
      showNotification('Camera access granted! Ready to scan QR code', 'success')
    } catch (err) {
      setCameraError('Camera access denied. Please enable camera permissions in your browser settings.')
      showNotification('Camera access denied', 'error')
      console.error('Camera error:', err)
    }
  }

  const stopCamera = () => {
    if (videoRef && videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks()
      tracks.forEach(track => track.stop())
    }
    setCameraActive(false)
  }

  useEffect(() => {
    if (modal === 'camera' && !cameraActive) {
      const timer = setTimeout(() => startCamera(), 100)
      return () => clearTimeout(timer)
    }
    if (modal !== 'camera' && cameraActive) {
      stopCamera()
    }
  }, [modal, cameraActive])
  
  useEffect(() => { refresh() }, [])

  if (loading || !dashboard) {
    return (
      <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #F3F0EE 0%, #FCFBFA 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '32px' }}>
        <div style={{ position: 'relative', width: '80px', height: '80px' }}>
          <div style={{ width: '100%', height: '100%', borderRadius: '50%', border: '3px solid rgba(207, 69, 0, 0.1)', animation: 'spin 3s linear infinite' }}></div>
          <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', borderRadius: '50%', border: '3px solid #CF4500', borderTop: '3px solid transparent', animation: 'spin 0.8s linear infinite' }}></div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <p style={{ fontSize: '20px', fontWeight: '500', color: '#141413', margin: '0 0 8px 0' }}>Analyzing your financial profile...</p>
          <p style={{ fontSize: '14px', color: '#696969', margin: '0' }}>Processing transactions and generating personalized insights</p>
        </div>
      </div>
    )
  }

  const { profile, recommendation: rec, risk, insights } = dashboard
  const riskColor = risk?.risk_level === 'high' ? '#CF4500' : risk?.risk_level === 'medium' ? '#F37338' : '#2E7D32'
  const riskBgColor = risk?.risk_level === 'high' ? '#FFEBEE' : risk?.risk_level === 'medium' ? '#FFF3E0' : '#E8F5E9'

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #F3F0EE 0%, #FCFBFA 100%)' }}>
      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideInTop {
          from { opacity: 0; transform: translateY(-20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideDown {
          0% { transform: translateY(-100%); }
          50% { transform: translateY(200px); }
          100% { transform: translateY(200px); }
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }
        .card-premium {
          background: #FFFFFF;
          border-radius: 28px;
          padding: 32px;
          box-shadow: 0 2px 12px rgba(0,0,0,0.06);
          animation: slideUp 0.5s ease;
          transition: all 0.3s ease;
        }
        .card-premium:hover {
          box-shadow: 0 8px 32px rgba(0,0,0,0.1);
          transform: translateY(-4px);
        }
        .card-gradient {
          background: linear-gradient(135deg, #CF4500 0%, #F37338 100%);
          color: #FFFFFF;
          border-radius: 28px;
          padding: 40px;
          box-shadow: 0 8px 32px rgba(207, 69, 0, 0.2);
        }
        .icon-circle {
          width: 56px;
          height: 56px;
          border-radius: 16px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 28px;
          font-weight: 700;
        }
        .action-btn {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 12px;
          padding: 20px;
          border-radius: 20px;
          background: #FFFFFF;
          border: 2px solid #E0E0E0;
          cursor: pointer;
          transition: all 0.3s ease;
          text-decoration: none;
          color: #141413;
        }
        .action-btn:hover {
          background: #F3F0EE;
          border-color: #CF4500;
          box-shadow: 0 4px 16px rgba(207, 69, 0, 0.1);
          transform: translateY(-4px);
        }
        .action-btn.active {
          border-color: #141413;
          background: #141413;
          color: #FFFFFF;
        }
        .badge {
          display: inline-block;
          padding: 6px 14px;
          border-radius: 20px;
          font-size: 12px;
          font-weight: 600;
          letter-spacing: 0.4px;
        }
        .badge-success {
          background: #E8F5E9;
          color: #2E7D32;
        }
        .badge-warning {
          background: #FFF3E0;
          color: #E65100;
        }
        .badge-alert {
          background: #FFEBEE;
          color: #CF4500;
        }
        .tab-button {
          padding: 10px 24px;
          border: none;
          background: transparent;
          color: #696969;
          font-weight: 500;
          font-size: 14px;
          cursor: pointer;
          border-bottom: 2px solid transparent;
          transition: all 0.2s ease;
          letter-spacing: -0.28px;
        }
        .tab-button.active {
          color: #141413;
          border-bottom-color: #CF4500;
        }
        .metric-box {
          display: flex;
          flex-direction: column;
          gap: 8px;
          padding: 24px;
          border-radius: 20px;
          background: #FCFBFA;
          border: 1px solid #E0E0E0;
        }
        .metric-label {
          font-size: 12px;
          font-weight: 600;
          color: #696969;
          text-transform: uppercase;
          letter-spacing: 0.4px;
        }
        .metric-value {
          font-size: 28px;
          font-weight: 600;
          color: #141413;
        }
        .metric-value.accent {
          color: #CF4500;
        }
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0,0,0,0.5);
          display: flex;
          align-items: flex-end;
          z-index: 1000;
          animation: fadeIn 0.3s ease;
        }
        .modal-content {
          background: #FFFFFF;
          border-radius: 32px 32px 0 0;
          padding: 40px;
          width: 100%;
          max-width: 600px;
          max-height: 90vh;
          overflow-y: auto;
          animation: slideUp 0.4s ease;
        }
        .modal-close {
          float: right;
          background: none;
          border: none;
          font-size: 24px;
          cursor: pointer;
          color: #696969;
          transition: color 0.2s ease;
        }
        .modal-close:hover {
          color: #141413;
        }
        .input-field {
          width: 100%;
          padding: 12px 16px;
          border: 2px solid #E0E0E0;
          border-radius: 12px;
          font-size: 16px;
          margin: 12px 0;
          transition: border-color 0.2s ease;
        }
        .input-field:focus {
          outline: none;
          border-color: #CF4500;
        }
        .button-primary {
          background: linear-gradient(135deg, #CF4500 0%, #F37338 100%);
          color: #FFFFFF;
          padding: 14px 32px;
          border: none;
          border-radius: 20px;
          font-weight: 600;
          font-size: 16px;
          cursor: pointer;
          transition: all 0.3s ease;
          box-shadow: 0 4px 12px rgba(207, 69, 0, 0.2);
          width: 100%;
          margin-top: 16px;
        }
        .button-primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 20px rgba(207, 69, 0, 0.3);
        }
        .button-secondary {
          background: #FCFBFA;
          color: #141413;
          padding: 12px 32px;
          border: 2px solid #E0E0E0;
          border-radius: 20px;
          font-weight: 500;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.2s ease;
        }
        .button-secondary:hover {
          border-color: #CF4500;
          background: #F3F0EE;
        }
        .notification {
          position: fixed;
          top: 20px;
          right: 20px;
          padding: 16px 24px;
          border-radius: 12px;
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
          animation: slideInTop 0.3s ease;
          z-index: 2000;
          max-width: 400px;
        }
        .notification.success {
          background: #E8F5E9;
          color: #2E7D32;
          border-left: 4px solid #2E7D32;
        }
        .notification.error {
          background: #FFEBEE;
          color: #CF4500;
          border-left: 4px solid #CF4500;
        }
        .notification.info {
          background: #E3F2FD;
          color: #1565C0;
          border-left: 4px solid #1565C0;
        }
      `}</style>

      {/* Notification Toast */}
      {notification && (
        <div className={`notification ${notification.type}`}>
          <p style={{ margin: '0', fontWeight: '500', fontSize: '14px' }}>
            {notification.type === 'success' && '✓ '}
            {notification.type === 'error' && '✕ '}
            {notification.type === 'info' && 'ℹ '}
            {notification.message}
          </p>
        </div>
      )}

      {/* Modal Overlay */}
      {modal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={closeModal}>✕</button>

            {modal === 'topup' && (
              <div>
                <h2 style={{ margin: '0 0 24px 0', fontSize: '28px', fontWeight: '600', color: '#141413' }}>Add Funds to Reserve</h2>
                <p style={{ color: '#696969', marginBottom: '24px', lineHeight: '20px' }}>
                  Increase your smart reserve to improve payment protection and unlock higher limits.
                </p>
                
                <div style={{ marginBottom: '24px' }}>
                  <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px', color: '#141413' }}>
                    Amount (Rs.)
                  </label>
                  <input
                    type="number"
                    className="input-field"
                    placeholder="Enter amount"
                    value={topupAmount}
                    onChange={(e) => setTopupAmount(e.target.value)}
                  />
                </div>

                <div style={{ background: '#FCFBFA', padding: '16px', borderRadius: '12px', marginBottom: '24px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginBottom: '8px' }}>
                    <span style={{ color: '#696969' }}>Amount:</span>
                    <span style={{ fontWeight: '600', color: '#141413' }}>Rs.{topupAmount || '0'}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px' }}>
                    <span style={{ color: '#696969' }}>Bonus (5%):</span>
                    <span style={{ fontWeight: '600', color: '#2E7D32' }}>+Rs.{(parseFloat(topupAmount || 0) * 0.05).toFixed(0)}</span>
                  </div>
                </div>

                <button className="button-primary" onClick={handleTopup}>Proceed with Payment</button>
                <button className="button-secondary" onClick={closeModal} style={{ width: '100%', marginTop: '12px' }}>Cancel</button>
              </div>
            )}

            {modal === 'action-Transfer' && (
              <div>
                <h2 style={{ margin: '0 0 24px 0', fontSize: '28px', fontWeight: '600', color: '#141413' }}>Transfer Money</h2>
                <p style={{ color: '#696969', marginBottom: '24px' }}>Send money to any bank account or UPI ID instantly.</p>
                <div style={{ background: '#FCFBFA', padding: '20px', borderRadius: '16px', marginBottom: '24px', border: '2px solid #CF4500' }}>
                  <p style={{ margin: '0 0 12px 0', fontSize: '12px', fontWeight: '600', color: '#CF4500', textTransform: 'uppercase' }}>Current Balance</p>
                  <p style={{ margin: '0', fontSize: '28px', fontWeight: '600', color: '#141413' }}>Rs.{rec?.recommended_reserve?.toFixed(0)}</p>
                </div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px', color: '#141413' }}>Recipient UPI ID</label>
                <input type="text" className="input-field" placeholder="name@bank" />
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px', marginTop: '16px', color: '#141413' }}>Amount (Rs.)</label>
                <input type="number" className="input-field" placeholder="Enter amount" />
                <button className="button-primary" onClick={() => { showNotification('Transfer initiated! Please verify with your bank.'); closeModal(); }}>Send Money</button>
              </div>
            )}

            {modal === 'action-Request' && (
              <div>
                <h2 style={{ margin: '0 0 24px 0', fontSize: '28px', fontWeight: '600', color: '#141413' }}>Request Money</h2>
                <p style={{ color: '#696969', marginBottom: '24px' }}>Create a payment request and share with friends.</p>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px', color: '#141413' }}>Amount (Rs.)</label>
                <input type="number" className="input-field" placeholder="Enter amount" />
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px', marginTop: '16px', color: '#141413' }}>Description</label>
                <textarea className="input-field" placeholder="Rent, dinner, etc." style={{ minHeight: '80px' }}></textarea>
                <button className="button-primary" onClick={() => { showNotification('Payment request created! Share link with friends.'); closeModal(); }}>Create Request</button>
              </div>
            )}

            {modal === 'action-Pay Bills' && (
              <div>
                <h2 style={{ margin: '0 0 24px 0', fontSize: '28px', fontWeight: '600', color: '#141413' }}>Pay Bills</h2>
                <p style={{ color: '#696969', marginBottom: '24px' }}>Manage all your utility payments in one place.</p>
                <div style={{ display: 'grid', gap: '12px' }}>
                  {['Electricity', 'Water', 'Internet', 'Mobile Recharge'].map((bill, idx) => (
                    <button key={idx} className="action-btn" style={{ flexDirection: 'row', justifyContent: 'space-between', padding: '16px 20px' }}>
                      <span style={{ marginLeft: '12px' }}>{['⚡', '💧', '📡', '📱'][idx]} {bill}</span>
                      <span style={{ fontSize: '14px', color: '#CF4500', fontWeight: '600' }}>→</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {modal === 'action-Analytics' && (
              <div>
                <h2 style={{ margin: '0 0 24px 0', fontSize: '28px', fontWeight: '600', color: '#141413' }}>Detailed Analytics</h2>
                <p style={{ color: '#696969', marginBottom: '24px' }}>View comprehensive spending insights and reports.</p>
                <div style={{ display: 'grid', gap: '12px' }}>
                  {['Monthly Trends', 'Category Breakdown', 'Merchant Analysis', 'Spending Forecast'].map((report, idx) => (
                    <button key={idx} className="action-btn" style={{ flexDirection: 'row', justifyContent: 'space-between', padding: '16px 20px' }}>
                      <span style={{ marginLeft: '12px' }}>{['📊', '🎯', '🏪', '🔮'][idx]} {report}</span>
                      <span style={{ fontSize: '14px', color: '#CF4500', fontWeight: '600' }}>→</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {modal === 'action-Settings' && (
              <div>
                <h2 style={{ margin: '0 0 24px 0', fontSize: '28px', fontWeight: '600', color: '#141413' }}>Settings</h2>
                <p style={{ color: '#696969', marginBottom: '24px' }}>Manage your account preferences and security.</p>
                <div style={{ display: 'grid', gap: '12px' }}>
                  {['Account Details', 'Security Settings', 'Notifications', 'Auto Top-up', 'Linked Accounts'].map((setting, idx) => (
                    <button key={idx} className="action-btn" style={{ flexDirection: 'row', justifyContent: 'space-between', padding: '16px 20px' }}>
                      <span style={{ marginLeft: '12px' }}>{['👤', '🔒', '🔔', '⚡', '🔗'][idx]} {setting}</span>
                      <span style={{ fontSize: '14px', color: '#CF4500', fontWeight: '600' }}>→</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {modal === 'action-Support' && (
              <div>
                <h2 style={{ margin: '0 0 24px 0', fontSize: '28px', fontWeight: '600', color: '#141413' }}>Customer Support</h2>
                <p style={{ color: '#696969', marginBottom: '24px' }}>We're here to help 24/7.</p>
                <div style={{ display: 'grid', gap: '12px' }}>
                  {['Chat with Agent', 'FAQ & Help', 'Report an Issue', 'Call Us'].map((support, idx) => (
                    <button key={idx} className="action-btn" style={{ flexDirection: 'row', justifyContent: 'space-between', padding: '16px 20px' }}>
                      <span style={{ marginLeft: '12px' }}>{['💬', '❓', '⚠️', '☎️'][idx]} {support}</span>
                      <span style={{ fontSize: '14px', color: '#CF4500', fontWeight: '600' }}>→</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {modal === 'learnmore' && (
              <div>
                <h2 style={{ margin: '0 0 24px 0', fontSize: '28px', fontWeight: '600', color: '#141413' }}>Smart Reserve Explained</h2>
                <div style={{ display: 'grid', gap: '16px', color: '#696969', lineHeight: '1.6' }}>
                  <div>
                    <h4 style={{ margin: '0 0 8px 0', color: '#141413', fontWeight: '600' }}>What is Smart Reserve?</h4>
                    <p style={{ margin: '0' }}>Your dedicated safety fund that protects your payments even during bank outages. It works alongside your bank account seamlessly.</p>
                  </div>
                  <div>
                    <h4 style={{ margin: '0 0 8px 0', color: '#141413', fontWeight: '600' }}>How is it calculated?</h4>
                    <p style={{ margin: '0' }}>We analyze your spending patterns over 30 days and recommend a reserve that covers 5 days of your average spending plus a 20% safety buffer.</p>
                  </div>
                  <div>
                    <h4 style={{ margin: '0 0 8px 0', color: '#141413', fontWeight: '600' }}>Is it safe?</h4>
                    <p style={{ margin: '0' }}>Yes! Your funds are protected by bank-grade encryption and 24/7 fraud monitoring. FDIC insured and compliant with all regulations.</p>
                  </div>
                </div>
              </div>
            )}

            {modal === 'camera' && (
              <div>
                <h2 style={{ margin: '0 0 24px 0', fontSize: '28px', fontWeight: '600', color: '#141413' }}>Scan QR Code</h2>
                <p style={{ color: '#696969', marginBottom: '24px' }}>Position QR code within the frame to scan and pay instantly.</p>
                
                {cameraError ? (
                  <div style={{
                    background: '#FFEBEE',
                    border: '2px solid #CF4500',
                    borderRadius: '16px',
                    padding: '24px',
                    marginBottom: '24px',
                    textAlign: 'center'
                  }}>
                    <p style={{ margin: '0', fontSize: '14px', color: '#CF4500', fontWeight: '600', marginBottom: '12px' }}>⚠️ Camera Access Denied</p>
                    <p style={{ margin: '0', fontSize: '13px', color: '#696969', lineHeight: '18px', marginBottom: '16px' }}>
                      {cameraError}
                    </p>
                    <button className="button-primary" onClick={startCamera} style={{ background: '#CF4500' }}>🔄 Try Again</button>
                  </div>
                ) : (
                  <div>
                    <div style={{
                      width: '100%',
                      height: '360px',
                      background: '#000000',
                      borderRadius: '20px',
                      marginBottom: '24px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      position: 'relative',
                      overflow: 'hidden'
                    }}>
                      {cameraActive ? (
                        <video
                          ref={videoRef}
                          autoPlay
                          playsInline
                          style={{
                            width: '100%',
                            height: '100%',
                            objectFit: 'cover'
                          }}
                        />
                      ) : (
                        <div style={{ textAlign: 'center', color: '#FFFFFF' }}>
                          <div style={{ fontSize: '48px', marginBottom: '12px' }}>📷</div>
                          <p style={{ margin: '0', fontSize: '14px' }}>Initializing camera...</p>
                        </div>
                      )}
                      
                      {/* Scanner Frame Overlay */}
                      <div style={{
                        position: 'absolute',
                        inset: '60px',
                        border: '3px solid #CF4500',
                        borderRadius: '12px',
                        boxShadow: 'inset 0 0 20px rgba(207, 69, 0, 0.3)'
                      }}></div>

                      {/* Dummy QR Code in center */}
                      <div style={{
                        position: 'absolute',
                        width: '120px',
                        height: '120px',
                        background: '#FFFFFF',
                        borderRadius: '8px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        padding: '8px',
                        boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
                        animation: 'pulse 2s infinite'
                      }}>
                        <div style={{
                          width: '100%',
                          height: '100%',
                          background: 'linear-gradient(45deg, #000 25%, transparent 25%, transparent 75%, #000 75%, #000), linear-gradient(45deg, #000 25%, transparent 25%, transparent 75%, #000 75%, #000)',
                          backgroundSize: '20px 20px',
                          backgroundPosition: '0 0, 10px 10px',
                          backgroundColor: '#FFFFFF',
                          borderRadius: '4px'
                        }}></div>
                      </div>

                      {/* Scanning lines animation */}
                      <div style={{
                        position: 'absolute',
                        inset: '60px',
                        borderRadius: '12px',
                        overflow: 'hidden'
                      }}>
                        <div style={{
                          width: '100%',
                          height: '3px',
                          background: 'linear-gradient(90deg, transparent 0%, #CF4500 50%, transparent 100%)',
                          animation: 'slideDown 1.5s infinite',
                          position: 'absolute',
                          top: '20%'
                        }}></div>
                      </div>
                    </div>

                    <button className="button-primary" onClick={() => { 
                      showNotification('✓ QR Code Detected! Merchant: Starbucks Coffee');
                      stopCamera();
                      setTimeout(() => {
                        openModal('payment-confirm');
                      }, 800);
                    }}>✓ QR Detected - Proceed</button>
                    
                    <button className="button-secondary" onClick={() => { 
                      stopCamera();
                      closeModal();
                    }} style={{ width: '100%', marginTop: '12px' }}>Cancel</button>
                  </div>
                )}
              </div>
            )}

            {modal === 'qr-pay' && (
              <div>
                <h2 style={{ margin: '0 0 24px 0', fontSize: '28px', fontWeight: '600', color: '#141413' }}>Display Your QR Code</h2>
                <p style={{ color: '#696969', marginBottom: '24px' }}>Share your UPI QR code with merchants to receive payments instantly.</p>
                
                <div style={{
                  width: '100%',
                  padding: '32px',
                  background: 'linear-gradient(135deg, #F3F0EE 0%, #FCFBFA 100%)',
                  borderRadius: '16px',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  marginBottom: '24px',
                  border: '2px solid #E0E0E0'
                }}>
                  <div style={{
                    width: '220px',
                    height: '220px',
                    background: '#FFFFFF',
                    border: '2px solid #CF4500',
                    borderRadius: '12px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: '20px',
                    boxShadow: '0 4px 16px rgba(207, 69, 0, 0.15)',
                    padding: '8px'
                  }}>
                    <div style={{
                      width: '100%',
                      height: '100%',
                      background: `
                        linear-gradient(45deg, #000 25%, transparent 25%, transparent 75%, #000 75%, #000),
                        linear-gradient(45deg, #000 25%, transparent 25%, transparent 75%, #000 75%, #000)
                      `,
                      backgroundSize: '16px 16px',
                      backgroundPosition: '0 0, 8px 8px',
                      backgroundColor: '#FFFFFF',
                      borderRadius: '4px',
                      position: 'relative',
                      overflow: 'hidden'
                    }}>
                      {/* Dummy QR pattern */}
                      <div style={{ position: 'absolute', top: '8px', left: '8px', width: '32px', height: '32px', border: '2px solid #000' }}></div>
                      <div style={{ position: 'absolute', top: '8px', right: '8px', width: '32px', height: '32px', border: '2px solid #000' }}></div>
                      <div style={{ position: 'absolute', bottom: '8px', left: '8px', width: '32px', height: '32px', border: '2px solid #000' }}></div>
                      <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', fontSize: '32px' }}>⚡</div>
                    </div>
                  </div>
                  
                  <p style={{ margin: '0 0 8px 0', fontSize: '12px', fontWeight: '600', color: '#696969', textTransform: 'uppercase', letterSpacing: '0.4px' }}>Your UPI ID</p>
                  <p style={{ margin: '0 0 16px 0', fontSize: '18px', fontWeight: '600', color: '#141413', letterSpacing: '-0.36px' }}>user_1@smartreserve</p>
                  <p style={{ margin: '0', fontSize: '11px', color: '#696969', textAlign: 'center' }}>Save or scan to receive payments</p>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '12px' }}>
                  <button className="button-primary" onClick={() => { 
                    showNotification('✓ QR Code copied to clipboard!', 'success');
                  }} style={{ background: '#CF4500' }}>
                    📋 Copy UPI ID
                  </button>
                  <button className="button-primary" onClick={() => { 
                    showNotification('✓ Shared on WhatsApp!', 'success');
                  }} style={{ background: '#25D366' }}>
                    💬 Share WhatsApp
                  </button>
                </div>

                <button 
                  className="button-secondary" 
                  onClick={closeModal} 
                  style={{ width: '100%' }}
                >
                  Close
                </button>
              </div>
            )}

            {modal === 'payment-confirm' && (
              <div>
                <h2 style={{ margin: '0 0 24px 0', fontSize: '28px', fontWeight: '600', color: '#141413' }}>Confirm Payment</h2>
                <p style={{ color: '#696969', marginBottom: '24px' }}>Verify the merchant details before completing payment.</p>
                
                <div style={{ background: 'linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%)', padding: '20px', borderRadius: '16px', marginBottom: '24px', border: '2px solid #F37338' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '16px' }}>
                    <div style={{ fontSize: '40px' }}>☕</div>
                    <div>
                      <p style={{ margin: '0 0 4px 0', fontSize: '12px', fontWeight: '600', color: '#696969', textTransform: 'uppercase' }}>Merchant Name</p>
                      <p style={{ margin: '0', fontSize: '18px', fontWeight: '600', color: '#141413' }}>Starbucks Coffee</p>
                    </div>
                  </div>
                  <div style={{ fontSize: '12px', color: '#696969', lineHeight: '18px' }}>
                    <p style={{ margin: '0 0 4px 0' }}>📍 Location: Mumbai, Maharashtra</p>
                    <p style={{ margin: '0' }}>🏪 Category: Food & Beverage</p>
                  </div>
                </div>

                <div style={{ background: '#FCFBFA', padding: '20px', borderRadius: '16px', marginBottom: '24px', border: '2px solid #CF4500' }}>
                  <p style={{ margin: '0 0 8px 0', fontSize: '12px', fontWeight: '600', color: '#696969', textTransform: 'uppercase' }}>Payment Amount</p>
                  <p style={{ margin: '0 0 16px 0', fontSize: '36px', fontWeight: '700', color: '#CF4500' }}>Rs.500</p>
                  
                  <p style={{ margin: '0 0 8px 0', fontSize: '12px', fontWeight: '600', color: '#696969', textTransform: 'uppercase', marginTop: '16px' }}>Your Balance After</p>
                  <p style={{ margin: '0', fontSize: '18px', fontWeight: '600', color: '#141413' }}>Rs.{(rec?.recommended_reserve - 500).toFixed(0)}</p>
                </div>

                <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px', color: '#141413' }}>Enter Amount to Confirm (Rs.)</label>
                <input type="number" className="input-field" defaultValue="500" />
                
                <button className="button-primary" onClick={() => { 
                  showNotification('✓ Payment of Rs.500 successful! TXN ID: TXN20260606001234', 'success');
                  closeModal();
                }}>✓ Confirm & Pay</button>
                <button className="button-secondary" onClick={() => openModal('camera')} style={{ width: '100%', marginTop: '12px' }}>← Back to Scan</button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Header */}
      <header style={{
        background: '#FFFFFF',
        borderBottom: '1px solid #E0E0E0',
        padding: '20px 40px',
        position: 'sticky',
        top: 0,
        zIndex: 50,
        boxShadow: '0 2px 8px rgba(0,0,0,0.04)'
      }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ fontSize: '28px', fontWeight: '700', color: '#CF4500' }}>💳</div>
            <div>
              <h1 style={{ margin: '0', fontSize: '24px', fontWeight: '600', color: '#141413' }}>Smart Reserve</h1>
              <p style={{ margin: '2px 0 0 0', fontSize: '12px', color: '#696969' }}>AI-Powered Payment Intelligence</p>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <button onClick={refresh} style={{
              background: 'linear-gradient(135deg, #CF4500 0%, #F37338 100%)',
              color: '#FFFFFF',
              padding: '12px 28px',
              border: 'none',
              borderRadius: '20px',
              fontWeight: '500',
              fontSize: '14px',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              boxShadow: '0 4px 12px rgba(207, 69, 0, 0.2)'
            }} onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'} onMouseOut={(e) => e.target.style.transform = ''}>
              ⟳ Refresh Analytics
            </button>
            <div style={{
              width: 48,
              height: 48,
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #CF4500 0%, #F37338 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#FFFFFF',
              fontWeight: '600',
              fontSize: '18px'
            }}>
              👤
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '40px' }}>
        
        {/* Primary Reserve Account Card */}
        <div className="card-gradient" style={{ marginBottom: '40px' }}>
          <div style={{ marginBottom: '32px' }}>
            <p style={{ margin: '0 0 8px 0', fontSize: '12px', fontWeight: '600', opacity: 0.9, textTransform: 'uppercase', letterSpacing: '0.4px' }}>Available Balance</p>
            <h2 style={{ margin: '0 0 16px 0', fontSize: '56px', fontWeight: '600' }}>Rs.{rec?.recommended_reserve?.toFixed(0)}</h2>
            <p style={{ margin: '0', fontSize: '14px', opacity: 0.9, lineHeight: '20px' }}>Your Smart Reserve is actively protecting your payments</p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '32px' }}>
            <div>
              <p style={{ margin: '0 0 8px 0', fontSize: '11px', fontWeight: '500', opacity: 0.8, textTransform: 'uppercase', letterSpacing: '0.4px' }}>Daily Limit</p>
              <p style={{ margin: '0', fontSize: '24px', fontWeight: '600' }}>Rs.100,000</p>
            </div>
            <div>
              <p style={{ margin: '0 0 8px 0', fontSize: '11px', fontWeight: '500', opacity: 0.8, textTransform: 'uppercase', letterSpacing: '0.4px' }}>Cash Back</p>
              <p style={{ margin: '0', fontSize: '24px', fontWeight: '600' }}>1.5%</p>
            </div>
          </div>
        </div>

        {/* UPI Light Money Section */}
        <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '24px', marginBottom: '40px' }}>
          <div className="card-premium" style={{ background: 'linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 100%)', borderLeft: '4px solid #3860BE' }}>
            <p style={{ margin: '0 0 12px 0', fontSize: '12px', fontWeight: '600', color: '#1565C0', textTransform: 'uppercase', letterSpacing: '0.4px' }}>UPI Light Money</p>
            <div style={{ fontSize: '48px', fontWeight: '700', color: '#1565C0', margin: '16px 0' }}>
              Rs.750
            </div>
            <p style={{ margin: '0', fontSize: '13px', color: '#696969', lineHeight: '18px' }}>
              Use your UPI Light for payments when your main balance is unavailable. No KYC required.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <button 
              className="action-btn"
              onClick={() => openModal('camera')}
              style={{ 
                padding: '32px 16px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                borderColor: '#3860BE',
                borderWidth: '2px'
              }}
            >
              <div style={{ fontSize: '36px' }}>📷</div>
              <p style={{ margin: '0', fontSize: '11px', fontWeight: '600', color: '#1565C0' }}>Scan QR</p>
            </button>
            <button 
              className="action-btn"
              onClick={() => openModal('qr-pay')}
              style={{ 
                padding: '32px 16px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                borderColor: '#2E7D32',
                borderWidth: '2px'
              }}
            >
              <div style={{ fontSize: '36px' }}>⚡</div>
              <p style={{ margin: '0', fontSize: '11px', fontWeight: '600', color: '#2E7D32' }}>Pay QR</p>
            </button>
          </div>
        </div>

        {/* Quick Actions */}
        <div style={{ marginBottom: '48px' }}>
          <h3 style={{ margin: '0 0 20px 0', fontSize: '18px', fontWeight: '600', color: '#141413', letterSpacing: '-0.36px' }}>Quick Actions</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', gap: '16px' }}>
            {[
              { icon: '📤', label: 'Transfer' },
              { icon: '🔔', label: 'Request' },
              { icon: '💰', label: 'Pay Bills' },
              { icon: '📊', label: 'Analytics' },
              { icon: '⚙️', label: 'Settings' },
              { icon: '📞', label: 'Support' }
            ].map((action, idx) => (
              <button 
                key={idx} 
                className={`action-btn ${modal === 'action-' + action.label ? 'active' : ''}`}
                onClick={() => handleQuickAction(action.label)}
              >
                <div style={{ fontSize: '32px' }}>{action.icon}</div>
                <p style={{ margin: '0', fontSize: '12px', fontWeight: '500' }}>{action.label}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Tab Navigation */}
        <div style={{ display: 'flex', gap: '40px', borderBottom: '1px solid #E0E0E0', marginBottom: '40px' }}>
          <button
            className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button
            className={`tab-button ${activeTab === 'analytics' ? 'active' : ''}`}
            onClick={() => setActiveTab('analytics')}
          >
            Analytics
          </button>
          <button
            className={`tab-button ${activeTab === 'risk' ? 'active' : ''}`}
            onClick={() => setActiveTab('risk')}
          >
            Risk Profile
          </button>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div>
            {/* Key Metrics */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '24px', marginBottom: '40px' }}>
              <div className="metric-box">
                <div className="metric-label">Daily Average Spending</div>
                <div className="metric-value accent">Rs.{profile?.avg_daily_spend?.toFixed(0)}</div>
                <div style={{ fontSize: '12px', color: '#696969' }}>Based on last 30 days</div>
              </div>
              <div className="metric-box">
                <div className="metric-label">Recent Velocity</div>
                <div className="metric-value accent">Rs.{profile?.recent_velocity?.toFixed(0)}</div>
                <div style={{ fontSize: '12px', color: '#696969' }}>Last 3 days activity</div>
              </div>
              <div className="metric-box">
                <div className="metric-label">Reserve Gap</div>
                <div className="metric-value" style={{ color: rec?.gap > 0 ? '#CF4500' : '#2E7D32' }}>
                  Rs.{rec?.gap?.toFixed(0)}
                </div>
                <div style={{ fontSize: '12px', color: '#696969' }}>
                  {rec?.gap > 0 ? 'Top-up recommended' : 'Healthy buffer'}
                </div>
              </div>
            </div>

            {/* Profile & Status */}
            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px', marginBottom: '40px' }}>
              <div className="card-premium">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '24px' }}>
                  <div>
                    <h3 style={{ margin: '0 0 8px 0', fontSize: '16px', fontWeight: '600', color: '#141413' }}>Your Profile</h3>
                    <div style={{ fontSize: '24px', fontWeight: '600', color: '#CF4500', letterSpacing: '-0.48px' }}>
                      {profile?.profile_type}
                    </div>
                  </div>
                  <span className={`badge badge-${profile?.profile_type === 'Burst Spender' ? 'warning' : 'success'}`}>
                    {profile?.profile_type === 'High Spender' ? 'Active User' : 'Variable Spender'}
                  </span>
                </div>
                <p style={{ fontSize: '14px', color: '#696969', margin: '0', lineHeight: '20px' }}>
                  {profile?.profile_type === 'High Spender' && 'You are a consistent, high-value user. Your smart reserve is tailored for your spending patterns.'}
                  {profile?.profile_type === 'Burst Spender' && 'You have variable spending with occasional high-value transactions. Your smart reserve accounts for sudden spikes.'}
                  {profile?.profile_type === 'Standard' && 'You maintain moderate, predictable spending patterns. Your smart reserve is optimized for stability.'}
                </p>
              </div>

              <div className="card-premium" style={{ background: riskBgColor, border: `2px solid ${riskColor}`, cursor: 'pointer', position: 'relative' }} onClick={() => setActiveTab('risk')}>
                <p style={{ margin: '0 0 12px 0', fontSize: '12px', fontWeight: '600', color: riskColor, textTransform: 'uppercase', letterSpacing: '0.4px' }}>Overall Risk</p>
                <div style={{ fontSize: '48px', fontWeight: '700', color: riskColor, margin: '12px 0' }}>
                  {risk?.risk_score?.toFixed(0)}/100
                </div>
                <span className={`badge badge-${risk?.risk_level === 'high' ? 'alert' : risk?.risk_level === 'medium' ? 'warning' : 'success'}`} style={{ textTransform: 'uppercase' }}>
                  {risk?.risk_level}
                </span>
                <p style={{ position: 'absolute', bottom: '16px', right: '16px', fontSize: '20px', cursor: 'pointer' }}>→</p>
              </div>
            </div>

            {/* Insights */}
            <div className="card-premium">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <h3 style={{ margin: '0', fontSize: '16px', fontWeight: '600', color: '#141413' }}>💡 Smart Insights</h3>
                <button 
                  onClick={() => openModal('learnmore')}
                  style={{
                    background: '#F3F0EE',
                    border: '1px solid #E0E0E0',
                    padding: '8px 16px',
                    borderRadius: '16px',
                    fontSize: '12px',
                    fontWeight: '500',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseOver={(e) => {
                    e.target.style.background = '#E0E0E0'
                    e.target.style.borderColor = '#CF4500'
                  }}
                  onMouseOut={(e) => {
                    e.target.style.background = '#F3F0EE'
                    e.target.style.borderColor = '#E0E0E0'
                  }}
                >
                  Learn More
                </button>
              </div>
              <div style={{ display: 'grid', gap: '16px' }}>
                {insights?.slice(0, 3).map((ins, idx) => (
                  <div key={idx} style={{
                    padding: '16px',
                    border: '1px solid #E0E0E0',
                    borderRadius: '16px',
                    borderLeft: `4px solid ${ins.insight_type === 'spending_trend' ? '#3860BE' : '#CF4500'}`,
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.background = '#FCFBFA'
                    e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.06)'
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.background = 'transparent'
                    e.currentTarget.style.boxShadow = 'none'
                  }}
                  >
                    <p style={{ margin: '0 0 8px 0', fontSize: '12px', fontWeight: '600', color: '#696969', textTransform: 'uppercase', letterSpacing: '0.4px' }}>
                      {ins.insight_type.replace('_', ' ')}
                    </p>
                    <p style={{ fontSize: '14px', color: '#141413', margin: '0', lineHeight: '20px' }}>
                      {ins.content}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
          <div>
            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
              <div className="card-premium">
                <h3 style={{ margin: '0 0 24px 0', fontSize: '16px', fontWeight: '600', color: '#141413' }}>📈 Spending Trends</h3>
                <div style={{ height: '380px' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={trends}>
                      <defs>
                        <linearGradient id="colorAmount" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#CF4500" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#CF4500" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#E0E0E0" />
                      <XAxis dataKey="date" stroke="#696969" style={{ fontSize: '12px' }} />
                      <YAxis stroke="#696969" style={{ fontSize: '12px' }} />
                      <Tooltip contentStyle={{ background: '#FFFFFF', border: `2px solid #CF4500`, borderRadius: '12px', padding: '12px' }} />
                      <Area type="monotone" dataKey="amount" stroke="#CF4500" strokeWidth={2} fillOpacity={1} fill="url(#colorAmount)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="card-premium">
                <h3 style={{ margin: '0 0 24px 0', fontSize: '16px', fontWeight: '600', color: '#141413' }}>📊 Statistics</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div style={{ padding: '16px', background: '#F3F0EE', borderRadius: '12px' }}>
                    <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#696969' }}>Total 14-Day Spend</p>
                    <p style={{ margin: '0', fontSize: '20px', fontWeight: '600', color: '#141413' }}>
                      Rs.{trends?.reduce((sum, t) => sum + t.amount, 0).toFixed(0)}
                    </p>
                  </div>
                  <div style={{ padding: '16px', background: '#F3F0EE', borderRadius: '12px' }}>
                    <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#696969' }}>Average Per Day</p>
                    <p style={{ margin: '0', fontSize: '20px', fontWeight: '600', color: '#141413' }}>
                      Rs.{(trends?.reduce((sum, t) => sum + t.amount, 0) / Math.max(1, trends?.length)).toFixed(0)}
                    </p>
                  </div>
                  <div style={{ padding: '16px', background: '#F3F0EE', borderRadius: '12px' }}>
                    <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#696969' }}>Peak Daily Spend</p>
                    <p style={{ margin: '0', fontSize: '20px', fontWeight: '600', color: '#CF4500' }}>
                      Rs.{Math.max(...trends?.map(t => t.amount) || [0]).toFixed(0)}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Risk Profile Tab */}
        {activeTab === 'risk' && (
          <div>
            <div className="card-premium" style={{ marginBottom: '24px', background: riskBgColor, border: `2px solid ${riskColor}` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <div>
                  <h3 style={{ margin: '0 0 16px 0', fontSize: '20px', fontWeight: '600', color: riskColor }}>Risk Assessment</h3>
                  <p style={{ margin: '0', fontSize: '14px', color: '#696969', lineHeight: '20px', maxWidth: '600px' }}>
                    Your account is{' '}
                    <strong style={{ color: riskColor, textTransform: 'uppercase' }}>
                      {risk?.risk_level}
                    </strong>
                    {' '}risk. This assessment considers your spending patterns, velocity, and reserve buffer.
                  </p>
                </div>
                <div style={{
                  width: '120px',
                  height: '120px',
                  borderRadius: '50%',
                  background: 'rgba(255, 255, 255, 0.5)',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  textAlign: 'center'
                }}>
                  <div style={{ fontSize: '40px', fontWeight: '700', color: riskColor }}>
                    {risk?.risk_score?.toFixed(0)}
                  </div>
                  <p style={{ margin: '4px 0 0 0', fontSize: '10px', fontWeight: '600', color: '#696969', textTransform: 'uppercase', letterSpacing: '0.2px' }}>
                    / 100
                  </p>
                </div>
              </div>
            </div>

            <h3 style={{ margin: '32px 0 20px 0', fontSize: '16px', fontWeight: '600', color: '#141413' }}>🔍 Contributing Factors</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '16px' }}>
              {risk?.factors?.map((factor, idx) => (
                <div key={idx} className="card-premium" style={{ borderLeft: `4px solid ${riskColor}` }}>
                  <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                    <div style={{
                      width: '36px',
                      height: '36px',
                      borderRadius: '8px',
                      background: riskColor,
                      color: '#FFFFFF',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: '600',
                      flexShrink: 0
                    }}>
                      ⚠️
                    </div>
                    <div>
                      <p style={{ margin: '0', fontSize: '14px', fontWeight: '500', color: '#141413', lineHeight: '20px' }}>
                        {factor}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Recommendations */}
            <div style={{ marginTop: '40px' }}>
              <h3 style={{ margin: '0 0 20px 0', fontSize: '16px', fontWeight: '600', color: '#141413' }}>💎 Recommendations</h3>
              <div style={{ display: 'grid', gap: '16px' }}>
                {rec?.gap > 0 && (
                  <div className="card-premium" style={{ borderLeft: `4px solid #CF4500` }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                      <div>
                        <h4 style={{ margin: '0 0 8px 0', fontSize: '14px', fontWeight: '600', color: '#141413' }}>Increase Your Reserve</h4>
                        <p style={{ margin: '0', fontSize: '13px', color: '#696969', lineHeight: '18px' }}>
                          Consider adding Rs.{rec?.gap?.toFixed(0)} to your smart reserve for better payment protection.
                        </p>
                      </div>
                      <button 
                        style={{
                          background: '#CF4500',
                          color: '#FFFFFF',
                          padding: '10px 20px',
                          border: 'none',
                          borderRadius: '16px',
                          fontWeight: '500',
                          fontSize: '12px',
                          cursor: 'pointer',
                          whiteSpace: 'nowrap',
                          flexShrink: 0,
                          transition: 'all 0.2s ease'
                        }}
                        onClick={() => openModal('topup')}
                        onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
                        onMouseOut={(e) => e.target.style.transform = ''}
                      >
                        Top Up Now
                      </button>
                    </div>
                  </div>
                )}
                <div className="card-premium" style={{ borderLeft: `4px solid #2E7D32` }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                    <div>
                      <h4 style={{ margin: '0 0 8px 0', fontSize: '14px', fontWeight: '600', color: '#141413' }}>Enable Auto Top-Up</h4>
                      <p style={{ margin: '0', fontSize: '13px', color: '#696969', lineHeight: '18px' }}>
                        Automatically maintain your ideal reserve balance when it drops below the threshold. No manual intervention needed.
                      </p>
                    </div>
                    <button 
                      style={{
                        background: '#2E7D32',
                        color: '#FFFFFF',
                        padding: '10px 20px',
                        border: 'none',
                        borderRadius: '16px',
                        fontWeight: '500',
                        fontSize: '12px',
                        cursor: 'pointer',
                        whiteSpace: 'nowrap',
                        flexShrink: 0,
                        transition: 'all 0.2s ease'
                      }}
                      onClick={() => { showNotification('Auto top-up enabled! You will receive notifications when your reserve drops below the threshold.'); }}
                      onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
                      onMouseOut={(e) => e.target.style.transform = ''}
                    >
                      Enable Now
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  )
}

export default App
