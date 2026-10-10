import client from "./client";

export const listProjects = () => client.get("/projects");
export const createProject = (data) => client.post("/projects", data);
export const getProject = (id) => client.get(`/projects/${id}`);
export const updateProject = (id, data) => client.patch(`/projects/${id}`, data);
export const deleteProject = (id) => client.delete(`/projects/${id}`);
export const addMember = (id, data) => client.post(`/projects/${id}/members`, data);
