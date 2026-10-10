import client from "./client";

export const listNotes = (projectId) => client.get(`/projects/${projectId}/notes`);
export const createNote = (projectId, data) =>
  client.post(`/projects/${projectId}/notes`, data);
export const updateNote = (id, data) => client.patch(`/notes/${id}`, data);
export const deleteNote = (id) => client.delete(`/notes/${id}`);
