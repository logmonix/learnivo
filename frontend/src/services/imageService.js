// src/services/imageService.js
// Centralized Axios wrapper for all image‑management API calls.
// This service will be used by the admin UI components (gallery, picker, chapter manager).

import axios from 'axios';

// Base URL for the backend API – adjust if you run the server on a different host/port.
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

// Helper to include admin auth token if present in localStorage.
function authHeaders() {
    try {
        const token = localStorage.getItem('authToken');
        return token ? { Authorization: `Bearer ${token}` } : {};
    } catch (error) {
        console.warn('Unable to access localStorage for auth token:', error);
        return {};
    }
}

/**
 * Upload one or multiple image files.
 * @param {FileList|File[]} files - Files selected by the user.
 * @param {function} onUploadProgress - Optional callback receiving the native progress event.
 * @returns {Promise} Axios response promise.
 */
export function uploadImages(files, onUploadProgress) {
    const form = new FormData();
    // Accept both FileList and plain array.
    Array.from(files).forEach((file) => form.append('file', file));

    return axios.post(`${API_BASE}/api/v1/images/upload`, form, {
        headers: {
            ...authHeaders(),
            'Content-Type': 'multipart/form-data',
        },
        onUploadProgress,
    });
}

/** Fetch a paginated list of images.
 * @param {number} page - Page number (starting at 1).
 * @param {number} pageSize - Items per page.
 * @param {string} search - Optional search term (filename).
 */
export function listImages({ page = 1, pageSize = 20, search = '' } = {}) {
    return axios.get(`${API_BASE}/api/v1/images`, {
        params: { page, page_size: pageSize, search },
        headers: authHeaders(),
    });
}

/** Delete an image by its UUID.
 * @param {string} imageId
 */
export function deleteImage(imageId) {
    return axios.delete(`${API_BASE}/api/v1/images/${imageId}`, {
        headers: authHeaders(),
    });
}

/** Get the public URL for an image file.
 * @param {string} imageId
 */
export function getImageFileUrl(imageId) {
    // Public endpoint does not need auth.
    return `${API_BASE}/api/v1/images/${imageId}/file`;
}

/** Fetch image metadata (size, dimensions, etc.) */
export function getImageDetails(imageId) {
    return axios.get(`${API_BASE}/api/v1/images/${imageId}`, {
        headers: authHeaders(),
    });
}

// Export a default object for convenient destructuring if preferred.
export default {
    uploadImages,
    listImages,
    deleteImage,
    getImageFileUrl,
    getImageDetails,
};
