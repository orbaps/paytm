import { useState, useEffect } from 'react'

const API_BASE = 'http://localhost:8000/api/v1'

function App() {
  const [balance, setBalance] = useState({ balance: 0 })
  const [settings, setSettings] = useState({})
  const [queue, setQueue] = useState([])
  const [outage, setOutage] = useState({})
  const [transactions, setTransactions] = useState([])
  
  const refresh = async () => {
    setBalance(await (await fetch(`${API_BASE}/reserve/balance`)).json())
    setSettings(await (await fetch(`${API_BASE}/reserve/settings`)).json())
    setQueue(await (await fetch(`${API_BASE}/refill-queue`)).json())
    setOutage(await (await fetch(`${API_BASE}/outage-simulation`)).json())
    setTransactions(await (await fetch(`${API_BASE}/transactions`)).json())
  }
  
  useEffect(() => { refresh() }, [])

  const simulatePayment = async () => {
    await fetch(`${API_BASE}/payments`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ amount: 150 })
    })
    refresh()
  }

  const toggleOutage = async () => {
    await fetch(`${API_BASE}/outage-simulation/toggle`, { method: 'POST' })
    refresh()
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-8 text-blue-600">Smart Reserve Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-gray-500 font-semibold mb-2">Reserve Balance</h2>
          <p className="text-3xl font-bold">Rs.{balance?.balance}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-gray-500 font-semibold mb-2">Target / Threshold</h2>
          <p className="text-xl">Target: Rs.{settings?.target_balance}</p>
          <p className="text-xl text-red-500">Threshold: Rs.{settings?.threshold}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-gray-500 font-semibold mb-2">Outage Status</h2>
          <p className={`text-2xl font-bold ${outage?.is_active ? 'text-red-500' : 'text-green-500'}`}>
            {outage?.is_active ? 'ACTIVE OUTAGE' : 'OPERATIONAL'}
          </p>
          <button onClick={toggleOutage} className="mt-4 bg-gray-200 px-4 py-2 rounded">Toggle Outage</button>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-gray-500 font-semibold mb-2">Test Panel</h2>
          <button onClick={simulatePayment} className="bg-blue-600 text-white px-4 py-2 rounded w-full">Make Payment (Rs.150)</button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded-lg shadow h-96 overflow-auto">
          <h2 className="text-xl font-bold mb-4">Transaction History</h2>
          <ul>
            {transactions.map(t => (
              <li key={t.id} className="border-b py-2 flex justify-between">
                <span>Rs.{t.amount} ({t.routing})</span>
                <span className={t.status === 'success' ? 'text-green-500' : 'text-red-500'}>{t.status}</span>
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
            {queue.length === 0 && <p className="text-gray-500">Queue is empty</p>}
          </ul>
        </div>
      </div>
    </div>
  )
}

export default App
