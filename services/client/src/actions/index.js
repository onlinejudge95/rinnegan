import {
  SIGN_UP_USER,
  SIGN_IN_USER,
  REFRESH_TOKEN,
  GET_USERS,
  GET_USER,
  REMOVE_USER,
  UPDATE_USER,
} from "./types";

export const SignUpUser = (username, email, password) => {
  return {
    type: SIGN_UP_USER,
    payload: {
      username,
      email,
      password,
    },
  };
};

export const SignInUser = (email, password) => {
  return {
    type: SIGN_IN_USER,
    payload: {
      email,
      password,
    },
  };
};

export const RefreshToken = (refreshToken) => {
  return {
    type: REFRESH_TOKEN,
    payload: { refreshToken },
  };
};

export const GetUsers = () => {
  return {
    type: GET_USERS,
  };
};

export const GetUser = (userId) => {
  return {
    type: GET_USER,
    payload: { user_id: userId },
  };
};

export const RemoveUser = (userId) => {
  return {
    type: REMOVE_USER,
    payload: { user_id: userId },
  };
};

export const UpdateUser = (userId, username, email) => {
  return {
    type: UPDATE_USER,
    payload: { user_id: userId, username, email },
  };
};
