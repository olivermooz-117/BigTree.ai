import client from "./client";

export const listMessages = (projectId) =>
  client.get(`/projects/${projectId}/messages`);
