// Chapter Image Service – wraps backend chapter‑image association endpoints
import api from './axios';

/** Get all images associated with a chapter */
export function getChapterImages(chapterId) {
    return api.get(`/admin/chapters/${chapterId}/images`);
}

/** Add an existing image to a chapter (optionally with caption) */
export function addImageToChapter(chapterId, imageId, caption = '') {
    return api.post(`/admin/chapters/${chapterId}/images`, {
        image_id: imageId,
        caption,
    });
}

/** Remove an image from a chapter */
export function removeImageFromChapter(chapterId, imageId) {
    return api.delete(`/admin/chapters/${chapterId}/images/${imageId}`);
}

/** Reorder an image within a chapter */
export function updateImageOrder(chapterId, imageId, newOrder) {
    return api.put(`/admin/chapters/${chapterId}/images/${imageId}/order`, {
        order_index: newOrder,
    });
}
