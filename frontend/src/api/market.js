import client from './client'

export const marketAPI = {
  getPrice:   (symbol)   => client.get(`/market/price/${symbol}`),
  getPrices:  (symbols)  => client.get(`/market/prices?symbols=${symbols.join(',')}`),
  getQuote:   (symbol)   => client.get(`/market/quote/${symbol}`),
  search:     (query)    => client.get(`/market/search/${query}`),
}
