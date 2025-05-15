import React, {useState, useEffect} from 'react';
import NavigationBar from "./components/navigationBar";
import EcoJournal from "./components/EcoJournal";
import getCookie from "./components/getCookie";
function App() {
    let [tasks, setTasks] = useState([]);
    let [debts, setDebts] = useState([]);
    let [score, setScore] = useState(0);
    useEffect(() => {
        fetch("/api/tasks_and_debts").then(response => {
            if(response.status === 200) {
                response.json().then(data => {
                    setTasks(data.tasks);
                    setDebts(data.debts);
                    setScore(data.points);
                })
            }else{
                console.log("Error fetching tasks");
            }
        })
    }, []);
  return (
    <div style={{ textAlign: 'center' }}>
        <NavigationBar />
        <div style={{ height: "10vh"}}></div>
        {score}
        <div className={"home-container"}>
            <div className={"t-account"}>
                <h2 style={{"gridRow": "1", "gridColumn": "1"}}>
                    Tasks
                </h2>
                <h2 style={{"gridRow": "1", "gridColumn": "2"}}>
                    Debts
                </h2>
                <div style={{"gridRow": "2", "gridColumn": "1"}} className={"task-debt-container"}>
                    {tasks.map((task, index) => {
                        return !task.done && (
                            <div className="card">
                                <h3 className={"task-container"}>
                                    {task.name}
                                </h3>
                                <p>{task.points} xp</p>
                                <button onClick={()=>{
                                    fetch(`/api/delete-task/${task.id}`, {
                                        method: "DELETE",
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'X-CSRFToken': getCookie("csrftoken"),
                                        }
                                    }).then(response => {
                                        if(response.status === 200) {
                                            response.json().then(data => {
                                                console.log(data);
                                            })
                                        }else{
                                            console.log("Error fetching tasks");
                                        }
                                    })
                                }}>Delete</button>
                                <button onClick={()=>{
                                    fetch(`/api/task-is-done/${task.id}`, {
                                        method: "UPDATE",
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'X-CSRFToken': getCookie("csrftoken"),
                                        }
                                    }).then(response => {
                                        if(response.status === 200) {
                                            response.json().then(data => {
                                                console.log(data);
                                            })
                                        }else{
                                            console.log("Error fetching tasks");
                                        }
                                    })
                                }}>Done</button>
                            </div>
                        );
                    })}
                </div>
                <div style={{"gridRow": "2", "gridColumn": "2"}} className={"task-debt-container"}>
                    {debts.map((debt, index) => {
                        return (!debt.paid && (
                            <div key={index} className={"task-container"}>
                                <div className="card">
                                    <p>+ {debt.points} xp</p>
                                    <h3>{debt.name}</h3>
                                </div>
                                <button onClick={()=>{
                                    fetch(`/api/pay-off-debt/${debt.id}`, {
                                        method: "UPDATE",
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'X-CSRFToken': getCookie("csrftoken"),
                                        }
                                    }).then(response => {
                                        if(response.status === 200) {
                                            response.json().then(data => {
                                                console.log(data);
                                            })
                                        }else{
                                            console.log("Error fetching tasks");
                                        }
                                    })
                                }}>Pay off</button>
                            </div>
                        ));
                    })}
                </div>
            </div>
        </div>
        <EcoJournal />
    </div>
  );
}

export default App;
