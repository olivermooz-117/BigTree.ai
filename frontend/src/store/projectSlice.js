import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import * as projectsApi from "../api/projects";

export const fetchProjects = createAsyncThunk("projects/list", async (_, { rejectWithValue }) => {
  try {
    const { data } = await projectsApi.listProjects();
    return data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.error || "Failed to load projects");
  }
});

export const createProject = createAsyncThunk("projects/create", async (payload, { rejectWithValue }) => {
  try {
    const { data } = await projectsApi.createProject(payload);
    return data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.error || "Failed to create project");
  }
});

const projectSlice = createSlice({
  name: "projects",
  initialState: {
    items: [],
    current: null,
    status: "idle",
    error: null,
  },
  reducers: {
    setCurrent(state, action) {
      state.current = action.payload;
    },
    clearCurrent(state) {
      state.current = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchProjects.pending, (s) => { s.status = "loading"; })
      .addCase(fetchProjects.fulfilled, (s, a) => {
        s.status = "succeeded";
        s.items = a.payload;
      })
      .addCase(fetchProjects.rejected, (s, a) => {
        s.status = "failed";
        s.error = a.payload;
      })
      .addCase(createProject.fulfilled, (s, a) => {
        s.items.unshift(a.payload);
      });
  },
});

export const { setCurrent, clearCurrent } = projectSlice.actions;
export default projectSlice.reducer;
