import { useEffect, useMemo, useState } from 'react'
import { Activity, Bell, BrainCircuit, BriefcaseBusiness, ChartNoAxesCombined, CircleUserRound, Home, Search, ShieldCheck, Sparkles } from 'lucide-react'
import { authAPI } from './api/auth'
import { brokerAPI } from './api/brokers'

const nav = [
  ['Home', Home], ['Markets', ChartNoAxesCombined], ['Research', Search],
  ['Portfolio', BriefcaseBusiness], ['Connections', ShieldCheck], ['Watch', Bell], ['Nia', BrainCircuit]
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

function providerById(catalog, id) {
  return catalog.find((item) => item.id === id)
}

export default function App() {
  const [active, setActive] = useState('Home')
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Ask me about your portfolio, market moves, company fundamentals, or risk. Demo mode is active, so I will not present simulated values as live data.' }
  ])
  const [user, setUser] = useState(null)
  const [authMode, setAuthMode] = useState('login')
  const [authForm, setAuthForm] = useState({ name: '', email: '', password: '' })
  const [authError, setAuthError] = useState('')
  const [authLoading, setAuthLoading] = useState(false)
  const [providers, setProviders] = useState([])
  const [showGroww, setShowGroww] = useState(false)
  const [growwToken, setGrowwToken] = useState('')
  const [growwSnapshot, setGrowwSnapshot] = useState(null)
  const [brokerError, setBrokerError] = useState('')
  const [brokerNotice, setBrokerNotice] = useState('')
  const [brokerLoading, setBrokerLoading] = useState(false)

  const total = useMemo(() => demoHoldings.reduce((a, h) => a + h.value, 0), [])

  useEffect(() => {
    brokerAPI.providers().then((res) => setProviders(res.data.providers || [])).catch(() => setProviders([]))

    const token = localStorage.getItem('nivara_token')
    if (token) {
      authAPI.me().then((res) => setUser(res.data)).catch(() => setUser(null))
    }

    const unauthorized = () => {
      setUser(null)
      setGrowwSnapshot(null)
      setActive('Account')
    }
    window.addEventListener('nivara:unauthorized', unauthorized)
    return () => window.removeEventListener('nivara:unauthorized', unauthorized)
  }, [])

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

  const submitAuth = async (event) => {
    event.preventDefault()
    setAuthError('')
    setAuthLoading(true)
    try {
      const res = authMode === 'login'
        ? await authAPI.login(authForm.email, authForm.password)
        : await authAPI.register({
            name: authForm.name,
            email: authForm.email,
            password: authForm.password,
            risk: 'Moderate',
            horizon: 7,
            monthly_sip: '10000',
          })
      localStorage.setItem('nivara_token', res.data.access_token)
      setUser(res.data.user)
      setAuthForm({ name: '', email: '', password: '' })
      setActive('Connections')
    } catch (err) {
      setAuthError(err.response?.data?.detail || 'Unable to sign in. Check your details and try again.')
    } finally {
      setAuthLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem('nivara_token')
    setUser(null)
    setGrowwSnapshot(null)
    setBrokerNotice('')
    setActive('Home')
  }

  const requestBrokerConnection = (provider) => {
    setBrokerError('')
    setBrokerNotice('')
    if (!user) {
      setAuthError('Sign in to Nivara before connecting a brokerage account.')
      setActive('Account')
      return
    }
    if (provider === 'groww') setShowGroww(true)
  }

  const connectGroww = async (event) => {
    event.preventDefault()
    if (!growwToken.trim()) return
    setBrokerError('')
    setBrokerNotice('')
    setBrokerLoading(true)
    try {
      const res = await brokerAPI.connectGrowwPreview(growwToken.trim())
      setGrowwSnapshot(res.data)
      setGrowwToken('')
      setShowGroww(false)
      setBrokerNotice('Groww verified. This is a read-only snapshot; the token was not stored by Nivara.')
    } catch (err) {
      setBrokerError(err.response?.data?.detail || 'Groww could not be verified. Check the token and try again.')
    } finally {
      setBrokerLoading(false)
    }
  }

  const startMotilal = async () => {
    if (!user) {
      setAuthError('Sign in to Nivara before connecting a brokerage account.')
      setActive('Account')
      return
    }
    setBrokerError('')
    setBrokerNotice('')
    setBrokerLoading(true)
    try {
      const res = await brokerAPI.motilalLogin()
      window.open(res.data.authorization_url, '_blank', 'noopener,noreferrer')
      setBrokerNotice('Motilal Oswal login opened in a new tab. Authentication stays on the broker website. A registered Nivara callback is still required to complete automatic syncing.')
    } catch (err) {
      setBrokerError(err.response?.data?.detail || 'Motilal Oswal connection is not configured yet.')
    } finally {
      setBrokerLoading(false)
    }
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
      <Metric label="Data freshness" value={growwSnapshot ? 'Groww snapshot' : 'Demo only'} detail={growwSnapshot ? 'Read-only session data available' : 'No live feed configured'} />
    </div>
    <div className="two-col">
      <Panel title="Portfolio intelligence" action={<button className="link" onClick={() => setActive('Portfolio')}>View portfolio</button>}>
        <div className="insight good"><ShieldCheck size={20}/><div><strong>What is working</strong><p>Holdings are user-scoped in the backend and portfolio summaries are calculated server side.</p></div></div>
        <div className="insight warn"><Activity size={20}/><div><strong>Next production step</strong><p>Connect authorised brokerage data, reconcile it, and retain source/freshness metadata without presenting stale values as live.</p></div></div>
      </Panel>
      <Panel title="Broker connections" action={<button className="link" onClick={() => setActive('Connections')}>Manage connections</button>}>
        <div className="briefing-card"><Badge>{growwSnapshot ? '1 VERIFIED SNAPSHOT' : 'READ-ONLY FIRST'}</Badge><h4>{growwSnapshot ? 'Groww snapshot connected' : 'Bring your existing investments into Nivara'}</h4><p>{growwSnapshot ? `${growwSnapshot.holding_count} holdings returned from Groww. Nivara did not persist the broker token.` : 'Start with secure, least-privilege broker connections. Nivara never asks for a broker password.'}</p></div>
      </Panel>
    </div>
  </>

  const renderPortfolio = () => <>
    <div className="hero compact"><div><Badge tone="live">DEMO DATA</Badge><h1>Portfolio</h1><p>Financial values below are illustrative until a production market data provider and canonical broker reconciliation are connected.</p></div></div>
    {growwSnapshot && <div className="notice success"><ShieldCheck size={18}/><div><strong>Groww snapshot available</strong><span>{growwSnapshot.holding_count} read-only holdings were verified at {new Date(growwSnapshot.as_of).toLocaleString()}.</span></div></div>}
    <Panel title="Holdings">
      <div className="table-wrap"><table><thead><tr><th>Asset</th><th>Value</th><th>P&amp;L</th><th>Weight</th></tr></thead><tbody>
        {demoHoldings.map(h => <tr key={h.symbol}><td><strong>{h.symbol}</strong><small>{h.name}</small></td><td>₹{h.value.toLocaleString('en-IN')}</td><td className={h.pnl >= 0 ? 'positive' : 'negative'}>{h.pnl > 0 ? '+' : ''}{h.pnl}%</td><td>{h.weight}%</td></tr>)}
      </tbody></table></div>
    </Panel>
  </>

  const renderConnections = () => {
    const groww = providerById(providers, 'groww')
    const motilal = providerById(providers, 'motilal-oswal')
    return <>
      <div className="hero compact"><div><Badge tone="ai">CONNECTIONS</Badge><h1>Connect your investments securely.</h1><p>Broker authentication stays with the broker. Nivara uses read-only data wherever possible and does not collect broker passwords.</p></div></div>
      {!user && <div className="notice warn"><ShieldCheck size={18}/><div><strong>Nivara sign-in required</strong><span>Sign in to your Nivara account before connecting financial accounts.</span></div><button className="link" onClick={() => setActive('Account')}>Sign in</button></div>}
      {brokerNotice && <div className="notice success"><ShieldCheck size={18}/><div><strong>Connection update</strong><span>{brokerNotice}</span></div></div>}
      {brokerError && <div className="notice error"><Activity size={18}/><div><strong>Connection issue</strong><span>{brokerError}</span></div></div>}

      <div className="broker-grid">
        <article className="broker-card">
          <div className="broker-head"><div className="broker-logo groww-logo">G</div><div><h3>Groww</h3><span>Direct API · read-only snapshot</span></div>{growwSnapshot ? <Badge tone="ai">VERIFIED</Badge> : <Badge>{groww?.status || 'AVAILABLE'}</Badge>}</div>
          <p>Verify your Groww account using a current Trading API access token. Nivara calls Groww directly for your user profile and demat holdings.</p>
          <div className="broker-features"><span><ShieldCheck size={15}/> Holdings</span><span><ShieldCheck size={15}/> Account profile</span><span><ShieldCheck size={15}/> No password</span></div>
          {growwSnapshot && <div className="connection-summary"><strong>UCC {growwSnapshot.profile?.ucc || '—'}</strong><span>{growwSnapshot.holding_count} holdings · snapshot {new Date(growwSnapshot.as_of).toLocaleTimeString()}</span></div>}
          <div className="broker-actions"><button className="primary" onClick={() => requestBrokerConnection('groww')}>{growwSnapshot ? <><Activity size={17}/> Refresh snapshot</> : <><CircleUserRound size={17}/> Connect Groww</>}</button><a className="secondary-link" href={groww?.docs_url || 'https://groww.in/trade-api/docs'} target="_blank" rel="noreferrer">API setup <span aria-hidden="true">↗</span></a></div>
          <small className="connection-footnote">Groww access tokens expire daily. This build validates the token once and does not persist it.</small>
        </article>

        <article className="broker-card">
          <div className="broker-head"><div className="broker-logo motilal-logo">MO</div><div><h3>Motilal Oswal</h3><span>Official broker redirect</span></div><Badge tone={motilal?.status === 'configured' ? 'ai' : 'neutral'}>{motilal?.status === 'configured' ? 'READY' : 'SETUP REQUIRED'}</Badge></div>
          <p>Nivara can use Motilal Oswal's official login portal so your client code, password, OTP and 2FA remain on the broker domain.</p>
          <div className="broker-features"><span><ShieldCheck size={15}/> DP holdings</span><span><ShieldCheck size={15}/> Positions</span><span><ShieldCheck size={15}/> Broker-hosted login</span></div>
          <div className="broker-actions"><button className="secondary" disabled={brokerLoading} onClick={startMotilal}><span aria-hidden="true">↗</span> Open broker login</button><a className="secondary-link" href={motilal?.docs_url || 'https://invest.motilaloswal.com/moAPI/APIDocumentation/Introduction'} target="_blank" rel="noreferrer">API docs <span aria-hidden="true">↗</span></a></div>
          <small className="connection-footnote">To complete automatic sync, configure Nivara's MOFSL API app key and register a callback URL with Motilal Oswal.</small>
        </article>
      </div>

      {growwSnapshot && <Panel title="Groww holdings snapshot" action={<Badge>NOT YET MERGED INTO CANONICAL PORTFOLIO</Badge>}>
        <div className="table-wrap"><table><thead><tr><th>Symbol</th><th>ISIN</th><th>Quantity</th><th>Average price</th><th>Free demat</th></tr></thead><tbody>
          {growwSnapshot.holdings.map((h, index) => <tr key={`${h.isin || h.symbol}-${index}`}><td><strong>{h.symbol || '—'}</strong></td><td>{h.isin || '—'}</td><td>{h.quantity ?? '—'}</td><td>{h.average_price == null ? '—' : `₹${Number(h.average_price).toLocaleString('en-IN')}`}</td><td>{h.demat_free_quantity ?? '—'}</td></tr>)}
          {!growwSnapshot.holdings.length && <tr><td colSpan="5">Groww returned no current stock holdings for this account.</td></tr>}
        </tbody></table></div>
        <p className="panel-note">Source: {growwSnapshot.source}. Nivara deliberately does not infer exchange, live market value or P&amp;L from this snapshot until instrument mapping and licensed market data are reconciled.</p>
      </Panel>}

      {showGroww && <div className="modal-backdrop" role="presentation" onMouseDown={() => !brokerLoading && setShowGroww(false)}><div className="modal" role="dialog" aria-modal="true" aria-labelledby="groww-title" onMouseDown={(e) => e.stopPropagation()}>
        <button className="modal-close" aria-label="Close" onClick={() => setShowGroww(false)}><span aria-hidden="true">×</span></button>
        <Badge tone="ai">READ-ONLY</Badge><h2 id="groww-title">Connect Groww</h2>
        <p>Generate a current access token inside Groww: <strong>Profile → Settings → Trading APIs → Generate API keys → Access Token</strong>. Paste only the access token below. Never enter your Groww password in Nivara.</p>
        <div className="security-callout"><ShieldCheck size={18}/><span>The token is sent to the Nivara backend only to verify your profile and fetch a holdings snapshot. This build does not store the token.</span></div>
        <form onSubmit={connectGroww} className="stack-form"><label>Groww access token<input type="password" autoComplete="off" value={growwToken} onChange={(e) => setGrowwToken(e.target.value)} placeholder="Paste access token" required minLength={20}/></label>{brokerError && <div className="form-error">{brokerError}</div>}<button className="primary wide" disabled={brokerLoading}>{brokerLoading ? 'Verifying…' : 'Verify & fetch holdings'}</button></form>
        <a className="secondary-link modal-doc" href="https://groww.in/trade-api/docs" target="_blank" rel="noreferrer">Open Groww Trading API documentation <span aria-hidden="true">↗</span></a>
      </div></div>}
    </>
  }

  const renderAccount = () => <div className="account-layout">
    <div className="account-copy"><Badge tone="ai">NIVARA ACCOUNT</Badge><h1>{user ? `Welcome, ${user.name}` : 'Sign in before connecting financial accounts.'}</h1><p>Your Nivara identity scopes portfolio data and broker connections to you. Broker passwords are never part of this account.</p>{user && <div className="account-card"><CircleUserRound size={28}/><div><strong>{user.name}</strong><span>{user.email}</span><small>Risk profile: {user.risk} · Horizon: {user.horizon} years</small></div></div>}</div>
    <div className="auth-card">{user ? <><h3>Account active</h3><p>You can now connect a supported brokerage account.</p><button className="primary wide" onClick={() => setActive('Connections')}><ShieldCheck size={17}/> Manage connections</button><button className="secondary wide" onClick={logout}><CircleUserRound size={17}/> Sign out</button></> : <>
      <div className="auth-tabs"><button className={authMode === 'login' ? 'active' : ''} onClick={() => {setAuthMode('login'); setAuthError('')}}>Sign in</button><button className={authMode === 'register' ? 'active' : ''} onClick={() => {setAuthMode('register'); setAuthError('')}}>Create account</button></div>
      <form className="stack-form" onSubmit={submitAuth}>{authMode === 'register' && <label>Name<input value={authForm.name} onChange={(e) => setAuthForm({...authForm, name: e.target.value})} minLength={2} maxLength={100} required/></label>}<label>Email<input type="email" autoComplete="email" value={authForm.email} onChange={(e) => setAuthForm({...authForm, email: e.target.value})} required/></label><label>Password<input type="password" autoComplete={authMode === 'login' ? 'current-password' : 'new-password'} value={authForm.password} onChange={(e) => setAuthForm({...authForm, password: e.target.value})} minLength={10} maxLength={128} required/></label>{authMode === 'register' && <small className="form-help">Use at least 10 characters with a letter and a number.</small>}{authError && <div className="form-error">{authError}</div>}<button className="primary wide" disabled={authLoading}>{authLoading ? 'Please wait…' : authMode === 'login' ? 'Sign in' : 'Create Nivara account'}</button></form>
    </>}</div>
  </div>

  const renderGeneric = () => <div className="empty-state"><Badge>FOUNDATION BUILD</Badge><h1>{active}</h1><p>This workspace is wired into the Nivara application shell. The next implementation step is to connect its production service contract and verified data source rather than fill it with fabricated content.</p></div>

  const renderNia = () => <div className="nia-layout"><div className="nia-header"><Badge tone="ai">NIA</Badge><h1>Investment intelligence, grounded in your context.</h1><p>Prototype responses clearly distinguish unavailable external data from deterministic portfolio logic.</p></div><div className="chat-panel">{messages.map((m,i)=><div key={i} className={`message ${m.role}`}><span>{m.role === 'assistant' ? 'Nia' : 'You'}</span><p>{m.text}</p></div>)}</div><div className="composer"><input value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>e.key==='Enter'&&askNia()} placeholder="Ask about portfolio risk, a company, or today's market..."/><button onClick={askNia}>Ask</button></div><small className="disclaimer">AI-assisted research only. Not certified financial advice. Demo mode may not contain current market information.</small></div>

  const page = active === 'Home' ? renderHome()
    : active === 'Portfolio' ? renderPortfolio()
    : active === 'Connections' ? renderConnections()
    : active === 'Nia' ? renderNia()
    : active === 'Account' ? renderAccount()
    : renderGeneric()

  return <div className="app-shell">
    <aside className="sidebar"><div className="brand"><div className="brand-mark">N</div><div><strong>NIVARA</strong><span>AI</span></div></div><nav>{nav.map(([label,Icon])=><button key={label} className={active===label?'active':''} onClick={()=>setActive(label)}><Icon size={19}/><span>{label}</span></button>)}</nav><div className="sidebar-bottom"><div className="env"><span></span>Development</div><button className={active === 'Account' ? 'active' : ''} onClick={() => setActive('Account')}><CircleUserRound size={19}/><span>{user ? user.name : 'Account'}</span></button></div></aside>
    <main><header className="topbar"><div><span className="eyebrow">NIVARA AI</span><strong>{active}</strong></div><div className="top-actions"><button aria-label="Notifications"><Bell size={18}/></button>{user && <Badge tone="ai">SIGNED IN</Badge>}<Badge>India</Badge></div></header><div className="content">{page}</div></main>
  </div>
}
