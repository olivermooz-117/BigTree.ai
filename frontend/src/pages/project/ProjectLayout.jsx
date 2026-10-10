import { useEffect, useState } from "react";
import { Outlet, useParams } from "react-router-dom";
import { useDispatch } from "react-redux";
import { getProject } from "../../api/projects";
import { setCurrent, clearCurrent } from "../../store/projectSlice";
import ProjectTabs from "../../components/ProjectTabs";
import Loading from "../../components/Loading";

export default function ProjectLayout() {
  const { id } = useParams();
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getProject(id)
      .then(({ data }) => {
        if (!cancelled) {
          dispatch(setCurrent(data));
          setError(null);
        }
      })
      .catch((err) => {
        if (!cancelled) setError(err.response?.data?.error || "Failed to load project");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
      dispatch(clearCurrent());
    };
  }, [id, dispatch]);

  if (loading) return <Loading text="Loading project…" />;
  if (error) return <div className="container"><p className="error">{error}</p></div>;

  return (
    <div className="container">
      <ProjectTabs />
      <Outlet />
    </div>
  );
}
