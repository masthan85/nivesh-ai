import client from './client'

export const brokerAPI = {
  providers: () => client.get('/broker/providers'),
  connectGrowwPreview: (accessToken) => client.post('/broker/connect/groww/preview', { access_token: accessToken }),
  motilalLogin: () => client.get('/broker/connect/motilal-oswal'),
}
