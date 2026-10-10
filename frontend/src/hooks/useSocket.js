import { useEffect, useRef } from "react";
import { io } from "socket.io-client";

export default function useSocket(projectId, onMessage) {
  const socketRef = useRef(null);

  useEffect(() => {
    if (!projectId) return;

    const token = localStorage.getItem("token");
    const socket = io(import.meta.env.VITE_SOCKET_URL || "http://localhost:5000", {
      auth: { token },
    });
    socketRef.current = socket;

    socket.on("connect", () => {
      socket.emit("join_project", { project_id: Number(projectId) });
    });

    socket.on("new_message", (msg) => {
      onMessage?.(msg);
    });

    return () => {
      socket.emit("leave_project", { project_id: Number(projectId) });
      socket.disconnect();
    };
  }, [projectId]);

  const send = (body) => {
    socketRef.current?.emit("send_message", {
      project_id: Number(projectId),
      body,
    });
  };

  return { send };
}
