import axios from 'axios'

const apiClient = axios.create({
    baseURL: process.env.API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
})

apiClient.interceptors.response.use(
    (response) => {
        console.log("API Response: ", response)
        return response
    },
    (error) => {
        console.log("API Error: ", error)
        if(error.response?.status >= 500) console.error('Server Error: ', error.response.status)
        else if(error.code === 'ECONNABORTED') console.error('Request Timeout: Please check your Connection.')
        else if(error.response?.status === 404) console.error(`${error.response?.status}: The requested resource was not found`)

        return Promise.reject(error)
    }
)

export default apiClient