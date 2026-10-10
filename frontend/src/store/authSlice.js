import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import * as authApi from "../api/auth";

export const login = createAsyncThunk("auth/login", async (payload, { rejectWithValue }) => {
  try {
    const { data } = await authApi.login(payload);
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));
    return data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.error || "Login failed");
  }
});

export const register = createAsyncThunk("auth/register", async (payload, { rejectWithValue }) => {
  try {
    const { data } = await authApi.register(payload);
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));
    return data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.error || "Registration failed");
  }
});

export const fetchMe = createAsyncThunk("auth/me", async (_, { rejectWithValue }) => {
  try {
    const { data } = await authApi.me();
    localStorage.setItem("user", JSON.stringify(data));
    return data;
  } catch (err) {
    return rejectWithValue("Session expired");
  }
});

const savedUser = localStorage.getItem("user");
const initialState = {
  user: savedUser ? JSON.parse(savedUser) : null,
  token: localStorage.getItem("token"),
  status: "idle",
  error: null,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logout(state) {
      state.user = null;
      state.token = null;
      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },
    clearError(state) {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (s) => { s.status = "loading"; s.error = null; })
      .addCase(login.fulfilled, (s, a) => {
        s.status = "succeeded";
        s.user = a.payload.user;
        s.token = a.payload.access_token;
      })
      .addCase(login.rejected, (s, a) => { s.status = "failed"; s.error = a.payload; })
      .addCase(register.pending, (s) => { s.status = "loading"; s.error = null; })
      .addCase(register.fulfilled, (s, a) => {
        s.status = "succeeded";
        s.user = a.payload.user;
        s.token = a.payload.access_token;
      })
      .addCase(register.rejected, (s, a) => { s.status = "failed"; s.error = a.payload; })
      .addCase(fetchMe.fulfilled, (s, a) => { s.user = a.payload; });
  },
});

export const { logout, clearError } = authSlice.actions;
export default authSlice.reducer;
