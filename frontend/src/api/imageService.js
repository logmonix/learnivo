// Image Service – wraps the backend image‑management API
import api from './axios';

/**
 * Fetch paginated list of images.
 * @param {number} page - page number (default 1)
 * @param {number} pageSize - items per page (default 20)
 */
export function fetchImages(page = 1, pageSize = 20) {
    return api.get('/images', { params: { page, page_size: pageSize } });
}

/**
 * Upload one or more image files.
 * @param {FileList|File[]} files - files to upload
 * @param {function} onProgress - optional progress callback (0‑100)
 */
export function uploadImages(files, onProgress) {
    const form = new FormData();
    for (const file of files) {
        form.append('file', file);
    }
    return api.post('/images/upload', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (e) => {
            if (onProgress) {
                const percent = Math.round((e.loaded * 100) / e.total);
                onProgress(percent);
            }
        },
    });
}

/**
 * Upload one or more image files.
 * @param {FileList|File[]} files - files to upload
 * @param {function} onProgress - optional progress callback (0‑100)
 */
export function uploadStudentImages(files, onProgress) {
    const form = new FormData();
    for (const file of files) {
        form.append('file', file);
    }
    return api.post('/images/upload/student', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (e) => {
            if (onProgress) {
                const percent = Math.round((e.loaded * 100) / e.total);
                onProgress(percent);
            }
        },
    });
}

/** Delete an image by its ID */
export function deleteImage(imageId) {
    return api.delete(`/images/${imageId}`);
}

/** Get the public URL for an image file */
export function getImageUrl(imageId) {
    // Backend serves the file at /images/{id}/file
    return `${api.defaults.baseURL}/images/${imageId}/file`;
}
