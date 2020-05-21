import React from "react";
import axios from "axios";
import PropTypes from "prop-types";

class UserStatus extends React.Component {
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
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/auth/status`, {
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

UserStatus.propTypes = {
  accssToken: PropTypes.string,
};

export default UserStatus;
