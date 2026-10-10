import client from "./client";

export const listTasks = (projectId) => client.get(`/projects/${projectId}/tasks`);
export const createTask = (projectId, data) =>
  client.post(`/projects/${projectId}/tasks`, data);
export const updateTask = (id, data) => client.patch(`/tasks/${id}`, data);
export const deleteTask = (id) => client.delete(`/tasks/${id}`);
