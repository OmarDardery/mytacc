import React, {useState, useEffect} from 'react';
import NavigationBar from "./components/navigationBar";
function App() {
    let [tasks, setTasks] = useState([]);
    let [debts, setDebts] = useState([]);
    useEffect(() => {
        fetch("/api/tasks").then(response => {
            if(response.status === 200) {
                response.json().then(data => {
                    setTasks(data.tasks);
                    setDebts(data.debts);
                })
            }else{
                console.log("Error fetching tasks");
            }
        })
    }, []);
  return (
    <div style={{ textAlign: 'center' }}>
        <NavigationBar />
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
                        return (
                            <div key={index} className={"task-container"}>
                                <h3>{task.name}</h3>
                                <p>{task.points} xp</p>
                                {task.completed ? <p>Completed</p> : <p>Not Completed</p>}
                            </div>
                        );
                    })}
                </div>
                <div style={{"gridRow": "2", "gridColumn": "2"}} className={"task-debt-container"}>
                    {debts.map((debt, index) => {
                        return (
                            <div key={index} className={"task-container"}>
                                <h3>{debt.name}</h3>
                                <p>{debt.points} xp</p>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    </div>
  );
}

export default App;
