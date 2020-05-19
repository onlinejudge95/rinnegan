import React from "react";
import { Route, Switch } from "react-router-dom";
import axios from "axios";
import UserList from "./components/UserList";
import AddUser from "./components/AddUser";
import About from "./components/About";
import NavBar from "./components/NavBar";
import RegisterForm from "./components/RegisterForm";
import LoginForm from "./components/LoginForm";

class App extends React.Component {
  state = {
    users: [],
    title: "Sentimental",
    accessToken: null,
  };

  addUser = (data) => {
    const headers = {
      Accept: "application/json",
      "Content-Type": "application/json",
    };

    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data, {
        headers,
      })
      .then((response) => {
        this.getUsers();
      })
      .catch((err) => console.log(err));
  };

  componentDidMount() {
    this.getUsers();
  }

  getUsers = () => {
    const headers = { Accept: "application/json" };

    axios
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, { headers })
      .then((response) => {
        this.setState({ users: response.data });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  handleRegisterFormSubmit = (data) => {
    const headers = {
      Accept: "application/json",
      "Content-Type": "application/json",
    };

    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/auth/register`, data, {
        headers,
      })
      .then((response) => {
        console.log(response.data);
      })
      .catch((err) => console.log(err));
  };

  handleLoginFormSubmit = (data) => {
    const headers = {
      Accept: "application/json",
      "Content-Type": "application/json",
    };

    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/auth/login`, data, {
        headers,
      })
      .then((response) => {
        this.setState({ accessToken: response.data.access_token });
        this.getUsers();
        window.localStorage.setItem(
          "refreshToken",
          response.data.refresh_token
        );
      })
      .catch((err) => console.log(err));
  };

  isAuthenticated = () => {
    if (this.state.accessToken) {
      return true;
    }
    return false;
  };

  logoutUser = () => {
    window.localStorage.removeItem("refreshToken");
    this.setState({ accessToken: null });
  };

  render() {
    return (
      <div>
        <NavBar title={this.state.title} logoutUser={this.logoutUser} />
        <section className="section">
          <div className="container">
            <div className="columns">
              <div className="column is-half">
                <br />
                <Switch>
                  <Route
                    path="/"
                    exact
                    render={() => {
                      return (
                        <div>
                          <h1 className="title is-1">Sentimental</h1>
                          <hr />
                          <br />
                          <AddUser addUser={this.addUser} />
                          <br />
                          <br />
                          <UserList users={this.state.users} />
                        </div>
                      );
                    }}
                  />
                  <Route path="/about" component={About} exact />
                  <Route
                    path="/register"
                    render={() => {
                      return (
                        <RegisterForm
                          isAuthenticated={this.isAuthenticated}
                          handleRegisterFormSubmit={
                            this.handleRegisterFormSubmit
                          }
                        />
                      );
                    }}
                    exact
                  />
                  <Route
                    path="/login"
                    render={() => {
                      return (
                        <LoginForm
                          isAuthenticated={this.isAuthenticated}
                          handleLoginFormSubmit={this.handleLoginFormSubmit}
                        />
                      );
                    }}
                    exact
                  />
                </Switch>
              </div>
            </div>
          </div>
        </section>
      </div>
    );
  }
}

export default App;
