import apiClient from "./apiClient";

export const dashboardAPI = () => {
    getSummary: () => {
        return apiClient.get('/dashboard/summary')
    }
}

export const unitsAPI = {
    getUnits: () => {
        return apiClient.get('/units')
    }
}

export const incidentsAPI = {
    getIncidents: () => {
        return apiClient.get('/incidents')
    }
}

export const geofencesAPI = {
    getGeofences: () => {
        return apiClient.get('/geofences')
    }
}

export const zonesAPI = {
    getZones: () => {
        return apiClient.get('/zones')
    }
}

export const liveMapAPI = {
    getLivemap: () => {
        return apiClient.get('/livemap')
    }
}