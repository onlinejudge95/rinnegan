import React from "react";
import { Redirect } from "react-router-dom";
import axios from "axios";
import PropTypes from "prop-types";

class UserProfile extends React.Component {
  state = { email: "", username: "" };

  componentDidMount() {
    this.getUserStatus();
  }

  getUserStatus = (event) => {
    const headers = {
      Accept: "application/json",
      Authorization: `Bearer ${this.props.accessToken}`,
      "Content-Type": "application/json",
    };
    return axios
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/auth/profile`, {
        headers,
      })
      .then((response) => {
        this.setState({
          email: response.data.email,
          username: response.data.username,
        });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  render() {
    if (!this.props.isAuthenticated()) {
      return <Redirect to="/login" />;
    }
    return (
      <div>
        <ul>
          <li>
            <strong>Email:</strong>&nbsp;
            <span data-testid="user-email">{this.state.email}</span>
          </li>
          <li>
            <strong>Username:</strong>&nbsp;
            <span data-testid="user-username">{this.state.username}</span>
          </li>
        </ul>
      </div>
    );
  }
}

UserProfile.propTypes = {
  // eslint-disable-next-line
  accssToken: PropTypes.string,
  isAuthenticated: PropTypes.func.isRequired,
};

export default UserProfile;
