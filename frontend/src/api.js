// src/api.js
import axios from 'axios'

export const BASE_URL = "http://127.0.0.1:8000/"

const api = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    }
})

export const chatAPI = {
    healthCheck: () => api.get('health/'),
    sendMessage: (message) => api.post('chat/', { question: message }),
}

export default api