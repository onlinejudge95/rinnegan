import React from "react";
import { Route, Switch } from "react-router-dom";
import axios from "axios";

import authComponents from "./components/auth";
import userComponents from "./components/user";
import navBarComponents from "./components/navbar";
import staticComponents from "./components/static";

class App extends React.Component {
  state = { accessToken: null };

  onRegisterFormSubmit = async (payload) => {
    const registerApiUrl = `${process.env.REACT_APP_SERVER_URL}/auth/register`;
    const headers = {
      Accept: "application/json",
      "Content-Type": "application/json",
    };
    try {
      const response = await axios.post(registerApiUrl, payload, { headers });
      console.log(response);
    } catch (error) {
      console.log("User with given email already exists");
    }
  };

  onLoginFormSubmit = async (payload) => {
    const loginApiUrl = `${process.env.REACT_APP_SERVER_URL}/auth/login`;
    const headers = {
      Accept: "application/json",
      "Content-Type": "application/json",
    };
    try {
      const response = await axios.post(loginApiUrl, payload, { headers });
      console.log(response);
      this.setState({ accessToken: response.data.access_token });
      window.localStorage.setItem("refreshToken", response.data.refresh_token);
    } catch (error) {
      console.log("Invalid credentials");
    }
  };

  onLogOutClick = () => {
    window.localStorage.removeItem("refreshToken");
    this.setState({ accessToken: null });
  };

  isAuthenticated = () => {
    if (this.state.accessToken) {
      return true;
    }
    return false;
  };

  render() {
    return (
      <div className="ui">
        <navBarComponents.NavBar
          isAuthenticated={this.isAuthenticated}
          onLogOutClick={this.onLogOutClick}
        />
        <div className="ui container">
          <div className="ui segment">
            {/* TODO:- Display Messages */}
            <div className="ui grid">
              <div className="two wide column"></div>
              <div className="twelve wide column">
                <Switch>
                  <Route path="/" exact component={staticComponents.About} />
                  <Route
                    path="/register"
                    exact
                    component={() => (
                      <authComponents.RegisterUser
                        onRegisterFormSubmit={this.onRegisterFormSubmit}
                        isAuthenticated={this.isAuthenticated}
                      />
                    )}
                  />
                  <Route
                    path="/login"
                    exact
                    component={() => (
                      <authComponents.LoginUser
                        onLoginFormSubmit={this.onLoginFormSubmit}
                        isAuthenticated={this.isAuthenticated}
                      />
                    )}
                  />
                  <Route
                    path="/profile"
                    exact
                    component={() => <userComponents.ShowUser />}
                  />
                  <Route
                    path="/update"
                    exact
                    component={() => <userComponents.UpdateUser />}
                  />
                  <Route
                    path="/remove"
                    exact
                    component={() => <userComponents.RemoveUser />}
                  />
                </Switch>
              </div>
              <div className="two wide column"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
