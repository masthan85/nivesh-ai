import client from './client'

export const portfolioAPI = {
  getHoldings:    ()          => client.get('/portfolio/holdings'),
  getSummary:     ()          => client.get('/portfolio/summary'),
  addHolding:     (data)      => client.post('/portfolio/holdings', data),
  updateHolding:  (id, data)  => client.put(`/portfolio/holdings/${id}`, data),
  deleteHolding:  (id)        => client.delete(`/portfolio/holdings/${id}`),

  getTaxSummary:  (fy)        => client.get(`/tax/summary?fy=${fy}`),

  getGoals:       ()          => client.get('/goals/'),
  createGoal:     (data)      => client.post('/goals/', data),
  updateGoal:     (id, data)  => client.put(`/goals/${id}`, data),
  deleteGoal:     (id)        => client.delete(`/goals/${id}`),

  getWatchlist:   ()          => client.get('/watchlist/'),
  addWatch:       (data)      => client.post('/watchlist/', data),
  removeWatch:    (id)        => client.delete(`/watchlist/${id}`),

  getAlerts:      ()          => client.get('/alerts/'),
  createAlert:    (data)      => client.post('/alerts/', data),
  deleteAlert:    (id)        => client.delete(`/alerts/${id}`),

  getDailyBriefing: ()        => client.get('/briefing/daily'),
  getPortfolioNews: ()        => client.get('/news/portfolio'),

  compareBrokers: (price, qty, tradeType) =>
    client.post('/broker/calculate', { price, qty, trade_type: tradeType }),

  aiChat: (message, history)  => client.post('/ai/chat', { message, history }),
  chatHistory: ()             => client.get('/ai/history'),
}
