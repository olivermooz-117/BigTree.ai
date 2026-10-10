import client from "./client";

export const listFiles = (projectId) => client.get(`/projects/${projectId}/files`);
export const uploadFile = (projectId, formData) =>
  client.post(`/projects/${projectId}/files`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
export const deleteFile = (id) => client.delete(`/files/${id}`);
