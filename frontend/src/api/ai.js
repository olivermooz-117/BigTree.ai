import client from "./client";

export const listPersonas = () => client.get("/personas");

export const listConversations = (projectId) =>
  client.get(`/projects/${projectId}/ai/conversations`);

export const getMessages = (projectId, conversationId) =>
  client.get(`/projects/${projectId}/ai/conversations/${conversationId}/messages`);

export const chat = (projectId, data) =>
  client.post(`/projects/${projectId}/ai/chat`, data);
