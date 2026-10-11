import { useEffect, useRef, useCallback } from "react";
import { io } from "socket.io-client";

export default function useSocket(projectId, onMessage) {
  const socketRef = useRef(null);
  const onMessageRef = useRef(onMessage);
  onMessageRef.current = onMessage;

  useEffect(() => {
    if (!projectId) return;

    const token = localStorage.getItem("token");
    const url = import.meta.env.VITE_SOCKET_URL || undefined; // same origin → proxy
    const socket = io(url, {
      path: "/socket.io",
      auth: { token },
    });
    socketRef.current = socket;

    socket.on("connect", () => {
      socket.emit("join_project", { project_id: Number(projectId) });
    });

    socket.on("new_message", (msg) => {
      onMessageRef.current?.(msg);
    });

    socket.on("error", (payload) => {
      console.warn("socket error", payload);
    });

    socket.on("connect_error", (err) => {
      console.warn("socket connect_error", err.message);
    });

    return () => {
      socket.emit("leave_project", { project_id: Number(projectId) });
      socket.disconnect();
      socketRef.current = null;
    };
  }, [projectId]);

  const send = useCallback((body) => {
    socketRef.current?.emit("send_message", {
      project_id: Number(projectId),
      body,
    });
  }, [projectId]);

  return { send };
}
