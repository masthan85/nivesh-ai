// src/api/auth.js
import client from './client'

export const authAPI = {
  register: (data)  => client.post('/auth/register', data),
  login:    (email, password) => client.post('/auth/login',
    new URLSearchParams({ username: email, password }),
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  ),
  me:       ()       => client.get('/auth/me'),
  update:   (data)   => client.put('/auth/profile', data),
}
