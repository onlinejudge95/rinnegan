import React from "react";
import {
  Button,
  Divider,
  Header,
  Form,
  Input,
  Container,
} from "semantic-ui-react";

const LoginUser = () => {
  return (
    <main className="content">
      <Container>
        <div className="ui relaxed divided padded full grid">
          <div className="row">
            <div className="column">
              <Header as="h1">Sign-In</Header>
            </div>
          </div>
          <Divider />
          <div className="row">
            <div className="eleven wide column">
              <Form>
                <Form.Field>
                  <label>Email</label>
                  <Input placeholder="Email" type="email" />
                </Form.Field>
                <Form.Field>
                  <label>Password</label>
                  <Input placeholder="Password" type="password" />
                </Form.Field>
                <Button type="submit" color="green">
                  Submit
                </Button>
              </Form>
            </div>
          </div>
        </div>
      </Container>
    </main>
  );
};

export default LoginUser;
