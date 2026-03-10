import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  logs: [],
  chatHistory: [],
};

export const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    addLog: (state, action) => {
      state.logs.push(action.payload);
    },
    addChatMessage: (state, action) => {
      state.chatHistory.push(action.payload);
    }
  },
});

export const { addLog, addChatMessage } = interactionSlice.actions;
export default interactionSlice.reducer;