import React from "react";
import { PropTypes } from "prop-types";

const Message = (props) => {
  console.log(props);
  return (
    <div className={`ui floating massive message ${props.messageType}`}>
      <i className="close icon" onClick={props.removeMessage()} />
      <p>{props.messageText}</p>
    </div>
  );
};

Message.propTypes = {
  messageType: PropTypes.string.isRequired,
  messageText: PropTypes.string.isRequired,
  removeMessage: PropTypes.func.isRequired,
};

export default Message;
