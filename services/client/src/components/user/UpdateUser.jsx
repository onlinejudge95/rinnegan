import React from "react";
import {
  Button,
  Divider,
  Header,
  Form,
  Input,
  Container,
} from "semantic-ui-react";

const UpdateUser = () => {
  return (
    <main className="content">
      <Container>
        <div class="ui relaxed divided padded full grid">
          <div class="row">
            <div class="column">
              <Header as="h1">Update Profile</Header>
            </div>
          </div>
          <Divider />
          <div class="row">
            <div class="eleven wide column">
              <Form>
                <Form.Field>
                  <label>Username</label>
                  <Input placeholder="Username" type="text" />
                </Form.Field>
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

export default UpdateUser;
