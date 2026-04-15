import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token')
            localStorage.removeItem('user')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

// API Services
export const apiService = {
    // Health check
    healthCheck: async () => {
        const response = await api.get('/health')
        return response.data
    },

    // Predict ticket
    predictTicket: async (text) => {
        const response = await api.post('/predict', { text })
        return response.data
    },

    // Get tickets
    getTickets: async (limit = 100) => {
        const response = await api.get(`/tickets?limit=${limit}`)
        return response.data
    },

    // Get predictions
    getPredictions: async (limit = 100) => {
        const response = await api.get(`/predictions?limit=${limit}`)
        return response.data
    },

    // Get statistics
    getStatistics: async () => {
        const response = await api.get('/statistics')
        return response.data
    },
}

// Mock Auth API (since backend doesn't have auth yet)
export const authService = {
    login: async (email, password) => {
        // Simulate API call
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (email && password) {
                    resolve({
                        token: 'mock-jwt-token-' + Date.now(),
                        user: {
                            id: '1',
                            email: email,
                            name: email.split('@')[0],
                        },
                    })
                } else {
                    reject(new Error('Invalid credentials'))
                }
            }, 1000)
        })
    },

    signup: async (name, email, password) => {
        // Simulate API call
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (name && email && password) {
                    resolve({
                        token: 'mock-jwt-token-' + Date.now(),
                        user: {
                            id: '1',
                            email: email,
                            name: name,
                        },
                    })
                } else {
                    reject(new Error('Invalid data'))
                }
            }, 1000)
        })
    },

    logout: () => {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
    },

    getCurrentUser: () => {
        const userStr = localStorage.getItem('user')
        return userStr ? JSON.parse(userStr) : null
    },
}

export default api
