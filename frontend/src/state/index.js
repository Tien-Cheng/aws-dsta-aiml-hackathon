import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    mode: "light",
    posts: []
};

export const checkerSlice = createSlice({
    name: "checker",
    initialState,
    reducers: {
        setMode: (state) => {
            state.mode = state.mode === "light" ? "dark" : "light";
        },
        setPosts: (state, action) => {
            state.posts = state.posts.concat(action.payload.posts);
        }
    },
});
  
export const { setMode, setPosts } = checkerSlice.actions;
export default checkerSlice.reducer;