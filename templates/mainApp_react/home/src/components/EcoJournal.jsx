// src/components/EcoJournal/EcoJournal.jsx
import React, { useState } from 'react';
import getCookie from "./getCookie";
const EcoJournal = (props) => {
    let [taskName, setTaskName] = useState("");
    let [debtName, setDebtName] = useState("");
    let [action, setAction] = useState("Task")
  // Handle dept entry submission
  const handleDebtSubmit = (name) => {
      fetch('/api/add/debt', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie("csrftoken"),
          },
          body: JSON.stringify({
              name
          })
      }).then(response => {
          if(response.status === 200) {
              response.json().then(data => {
                  console.log(data);
              })
            props.setRefresh(!props.refresh);
              setTaskName("");
                setDebtName("");
          }else{
              console.log("Error fetching tasks");
          }
      })
  };

  // Handle eco task submission
  const handleTaskSubmit = (name) => {
      fetch('/api/add/task', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie("csrftoken"),
          },
          body: JSON.stringify({
              name
          })
      }).then(response => {
          if(response.status === 200) {
              response.json().then(data => {
                  console.log(data);
              })

            props.setRefresh(!props.refresh);
                setDebtName("");
                setTaskName("");
          }else{
              console.log("Error fetching tasks");
          }
      })
  };

  return (
    <div className={"form"}>
        <div className={"form-button-slider"}>
            <button onClick={() => {
                setAction("Task");
            }} className={action === "Task" ? "active" : ""}>
            <h1>Add Task</h1>
            </button>
            <button onClick={() => {
                setAction("Debt");
            }} className={action === "Task" ? "" : "active"}>
            <h1>Add debt</h1>
            </button>
        </div>
        <div className={"form-field"}>
            <label htmlFor={"name"}>{action} name:</label>
            <input type="text" onChange={(e)=>{
                if(action === "Task") {
                    setTaskName(e.target.value);
                }else {
                    setDebtName(e.target.value);
                }
            }} value={action === "Task" ? taskName : debtName} name="name" />
        </div>

        <button onClick={()=>{
            if(action === "Task") {
                handleTaskSubmit(taskName);
            }else {
                handleDebtSubmit(debtName);
            }
        }} className={"form-submit-button"}>Submit</button>
    </div>
  );
};


export default EcoJournal;