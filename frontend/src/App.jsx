import React, { useMemo, useState } from 'react'
import { Activity, Bell, BrainCircuit, BriefcaseBusiness, ChartNoAxesCombined, CircleUserRound, House, Search, ShieldCheck, Sparkles } from 'lucide-react'

const nav = [
  ['Home', House], ['Markets', ChartNoAxesCombined], ['Research', Search],
  ['Portfolio', BriefcaseBusiness], ['Watch', Bell], ['Nia', BrainCircuit]
]

const demoHoldings = [
  { symbol: 'RELIANCE', name: 'Reliance Industries', value: 40875, pnl: 11.2, weight: 31 },
  { symbol: 'INFY', name: 'Infosys', value: 49890, pnl: 20.5, weight: 37 },
  { symbol: 'HDFCBANK', name: 'HDFC Bank', value: 32020, pnl: 1.3, weight: 24 },
  { symbol: 'WIPRO', name: 'Wipro', value: 10710, pnl: -43.3, weight: 8 },
]

function Badge({ children, tone='neutral' }) { return <span className={`badge ${tone}`}>{children}</span> }
function Metric({ label, value, detail }) { return <div className="metric"><span>{label}</span><strong>{value}</strong><small>{detail}</small></div> }
function Panel({ title, action, children }) { return <section className="panel"><div className="panel-head"><h3>{title}</h3>{action}</div>{children}</section> }

export default function App() {
  const [active, setActive] = useState('Home')
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Ask me about your portfolio, market moves, company fundamentals, or risk. Demo mode is active, so I will not present simulated values as live data.' }
  ])
  const total = useMemo(() => demoHoldings.reduce((a, h) => a + h.value, 0), [])

  const askNia = () => {
    const q = query.trim()
    if (!q) return
    const lower = q.toLowerCase()
    let answer = 'This prototype does not yet have a connected research provider. I can still explain the product flow, but I will not invent a market fact or price.'
    if (lower.includes('risk')) answer = 'Your demo portfolio is concentrated in IT and a few large-cap names. The production version will calculate concentration, volatility, correlation and scenario risk from timestamped source data.'
    if (lower.includes('portfolio')) answer = 'The demo portfolio value shown in this interface is illustrative. In production, Nia will read authorised holdings, then combine deterministic calculations with sourced market and news context.'
    setMessages([...messages, { role: 'user', text: q }, { role: 'assistant', text: answer }])
    setQuery('')
  }

  const renderHome = () => <>
    <div className="hero">
      <div><Badge tone="live">DEMO DATA</Badge><h1>Good afternoon. Here’s what matters.</h1><p>Nivara turns portfolio, market, risk and research signals into one decision workspace.</p></div>
      <button className="primary" onClick={() => setActive('Nia')}><Sparkles size={18}/> Ask Nia</button>
    </div>
    <div className="metrics-grid">
      <Metric label="Portfolio value" value={`₹${total.toLocaleString('en-IN')}`} detail="Illustrative demo value" />
      <Metric label="Today" value="Data unavailable" detail="Live provider not connected" />
      <Metric label="Risk posture" value="Moderate" detail="Profile setting, not a recommendation" />
      <Metric label="Data freshness" value="Demo only" detail="No live feed configured" />
    </div>
    <div className="two-col">
      <Panel title="Portfolio intelligence" action={<button className="link" onClick={() => setActive('Portfolio')}>View portfolio</button>}>
        <div className="insight good"><ShieldCheck size={20}/><div><strong>What is working</strong><p>Holdings are user-scoped in the backend and portfolio summaries are calculated server side.</p></div></div>
        <div className="insight warn"><Activity size={20}/><div><strong>What needs production data</strong><p>Prices, news and AI grounding still need licensed providers, freshness metadata and failure handling.</p></div></div>
      </Panel>
      <Panel title="Nivara briefing">
        <div className="briefing-card"><Badge>PRODUCT PREVIEW</Badge><h4>From information to investment intelligence</h4><p>The production briefing will explain only portfolio-relevant moves, cite sources and separate retrieved facts from AI interpretation.</p></div>
      </Panel>
    </div>
  </>

  const renderPortfolio = () => <>
    <div className="hero compact"><div><Badge tone="live">DEMO DATA</Badge><h1>Portfolio</h1><p>Financial values below are illustrative until a production market data provider is connected.</p></div></div>
    <Panel title="Holdings">
      <div className="table-wrap"><table><thead><tr><th>Asset</th><th>Value</th><th>P&amp;L</th><th>Weight</th></tr></thead><tbody>
        {demoHoldings.map(h => <tr key={h.symbol}><td><strong>{h.symbol}</strong><small>{h.name}</small></td><td>₹{h.value.toLocaleString('en-IN')}</td><td className={h.pnl >= 0 ? 'positive' : 'negative'}>{h.pnl > 0 ? '+' : ''}{h.pnl}%</td><td>{h.weight}%</td></tr>)}
      </tbody></table></div>
    </Panel>
  </>

  const renderGeneric = () => <div className="empty-state"><Badge>FOUNDATION BUILD</Badge><h1>{active}</h1><p>This workspace is wired into the Nivara application shell. The next implementation step is to connect its production service contract and verified data source rather than fill it with fabricated content.</p></div>

  const renderNia = () => <div className="nia-layout"><div className="nia-header"><Badge tone="ai">NIA</Badge><h1>Investment intelligence, grounded in your context.</h1><p>Prototype responses clearly distinguish unavailable external data from deterministic portfolio logic.</p></div><div className="chat-panel">{messages.map((m,i)=><div key={i} className={`message ${m.role}`}><span>{m.role === 'assistant' ? 'Nia' : 'You'}</span><p>{m.text}</p></div>)}</div><div className="composer"><input value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>e.key==='Enter'&&askNia()} placeholder="Ask about portfolio risk, a company, or today's market..."/><button onClick={askNia}>Ask</button></div><small className="disclaimer">AI-assisted research only. Not certified financial advice. Demo mode may not contain current market information.</small></div>

  return <div className="app-shell">
    <aside className="sidebar"><div className="brand"><div className="brand-mark">N</div><div><strong>NIVARA</strong><span>AI</span></div></div><nav>{nav.map(([label,Icon])=><button key={label} className={active===label?'active':''} onClick={()=>setActive(label)}><Icon size={19}/><span>{label}</span></button>)}</nav><div className="sidebar-bottom"><div className="env"><span></span>Development</div><button><CircleUserRound size={19}/><span>Account</span></button></div></aside>
    <main><header className="topbar"><div><span className="eyebrow">NIVARA AI</span><strong>{active}</strong></div><div className="top-actions"><button aria-label="Notifications"><Bell size={18}/></button><Badge>India</Badge></div></header><div className="content">{active==='Home'?renderHome():active==='Portfolio'?renderPortfolio():active==='Nia'?renderNia():renderGeneric()}</div></main>
  </div>
}
