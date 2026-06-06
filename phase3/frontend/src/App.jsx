import { useState, useEffect } from 'react'

const API_BASE = 'http://localhost:8000/api/v1'

function App() {
  const [balance, setBalance] = useState({ balance: 0, health_status: 'healthy' })
  const [outageActive, setOutageActive] = useState(false)
  const [bankHealth, setBankHealth] = useState([])
  const [userRisk, setUserRisk] = useState([])
  const [events, setEvents] = useState([])
  const [protectedTx, setProtectedTx] = useState({ protected_count: 0 })
  const [queue, setQueue] = useState([])
  
  const refresh = async () => {
    setBalance(await (await fetch(`${API_BASE}/reserve/balance`)).json())
    const outStatus = await (await fetch(`${API_BASE}/outage-status`)).json()
    setOutageActive(outStatus.active)
    setBankHealth(await (await fetch(`${API_BASE}/bank-health`)).json())
    setUserRisk(await (await fetch(`${API_BASE}/user-risk`)).json())
    setEvents(await (await fetch(`${API_BASE}/events`)).json())
    setProtectedTx(await (await fetch(`${API_BASE}/protected-transactions`)).json())
    setQueue(await (await fetch(`${API_BASE}/refill-queue`)).json())
  }
  
  useEffect(() => { 
    refresh()
    const intv = setInterval(refresh, 5000)
    return () => clearInterval(intv)
  }, [])

  const simulatePayment = async (userId) => {
    await fetch(`${API_BASE}/payments`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ amount: 150, user_id: userId })
    })
    refresh()
  }

  const toggleOutage = async () => {
    if(outageActive) {
      await fetch(`${API_BASE}/outage/end`, { method: 'POST' })
    } else {
      await fetch(`${API_BASE}/outage/start`, { method: 'POST' })
    }
    refresh()
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-indigo-600">Smart Reserve Phase 3 - Intelligence Engine</h1>
        <button onClick={toggleOutage} className={`px-4 py-2 font-bold rounded text-white ${outageActive ? 'bg-green-600' : 'bg-red-600'}`}>
          {outageActive ? 'Resolve Outage' : 'Simulate Outage'}
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className={`p-6 rounded-lg shadow ${balance.health_status === 'critical' ? 'bg-red-100' : 'bg-white'}`}>
          <h2 className="text-gray-500 font-semibold mb-2">Reserve Balance</h2>
          <p className="text-3xl font-bold">Rs.{balance?.balance}</p>
          <p className="text-sm mt-2 font-bold text-gray-700 uppercase">{balance.health_status}</p>
        </div>
        
        <div className={`p-6 rounded-lg shadow ${outageActive ? 'bg-red-100' : 'bg-green-100'}`}>
          <h2 className="text-gray-600 font-semibold mb-2">Bank Health Status</h2>
          <p className="text-3xl font-bold">Score: {bankHealth[0]?.health_score || 0}</p>
          <p className="text-sm font-bold uppercase mt-2">{bankHealth[0]?.status || 'UNKNOWN'}</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-2 border-indigo-200">
          <h2 className="text-gray-500 font-semibold mb-2">Protected Txs</h2>
          <p className="text-4xl font-bold text-indigo-600">{protectedTx.protected_count}</p>
          <p className="text-sm text-gray-500 mt-2">Saved from outage</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-gray-500 font-semibold mb-2">Simulation Tools</h2>
          <button onClick={() => simulatePayment('user_1')} className="bg-blue-500 text-white px-3 py-1 rounded w-full mb-2">Pmt (Low Risk)</button>
          <button onClick={() => simulatePayment('user_bad')} className="bg-purple-500 text-white px-3 py-1 rounded w-full">Pmt (High Risk)</button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="bg-white p-6 rounded-lg shadow h-96 overflow-auto">
          <h2 className="text-xl font-bold mb-4">Audit Events</h2>
          <ul>
            {events.map(e => (
              <li key={e.id} className="border-b py-2 flex flex-col text-sm">
                <span className="font-semibold text-gray-700">{e.event_type}</span>
                <span className="text-gray-600">{e.description}</span>
                <span className="text-xs text-gray-400">{new Date(e.created_at).toLocaleTimeString()}</span>
              </li>
            ))}
          </ul>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow h-96 overflow-auto">
          <h2 className="text-xl font-bold mb-4">Refill Queue</h2>
          <ul>
             {queue.map(q => (
              <li key={q.id} className="border-b py-2 flex justify-between">
                <span>Topup: Rs.{q.amount}</span>
                <span className={q.status === 'pending' ? 'text-yellow-500' : 'text-green-500'}>{q.status}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-white p-6 rounded-lg shadow h-96 overflow-auto">
          <h2 className="text-xl font-bold mb-4">User Risk Profiles</h2>
          <ul>
            {userRisk.map(u => (
              <li key={u.id} className="border-b py-2 flex justify-between">
                <span>{u.user_id}</span>
                <span className={`font-bold ${u.risk_level === 'high' ? 'text-red-500' : 'text-green-500'}`}>
                  {u.risk_level} ({u.risk_score})
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}

export default App
