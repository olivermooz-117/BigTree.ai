import client from "./client";

export const listFiles = (projectId) => client.get(`/projects/${projectId}/files`);

export const uploadFile = (projectId, formData) =>
  client.post(`/projects/${projectId}/files`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

export const deleteFile = (id) => client.delete(`/files/${id}`);

/** Download with JWT — returns a blob URL the browser can open/save */
export async function downloadFile(id, filename) {
  const res = await client.get(`/files/${id}/download`, { responseType: "blob" });
  const url = URL.createObjectURL(res.data);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename || "download";
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}
