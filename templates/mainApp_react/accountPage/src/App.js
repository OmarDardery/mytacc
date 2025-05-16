import React, {useEffect, useState} from 'react';
import getCookie from "./components/getCookie"
import NavigationBar from "./components/components/navigationBar";
function App() {
    let [user, setUser] = useState({});
    useEffect(() => {
        fetch("/api/get-user", {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie("csrftoken"),
            }
        }).then(response => {
            if(response.status === 200) {
                response.json().then(data => {
                    setUser(data);
                    console.log(data);
                })
            }else{
                console.log("Error fetching user");
            }
        })
    }, []);
  return (
    <div>
      <NavigationBar />
        <div style={{ height: "10vh"}}>

        </div>
        <div style={{ textAlign: 'left' }}>
            <h1>@{user.username}</h1>
            <h1>Email: {user.email}</h1>
            <h2>Eco-Points: {user.points}</h2>
          <button onClick={() => {
            const token = getCookie("csrftoken");
            fetch('/api/logout/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token,
              },
            }).then(response => {
              window.location.href = "/";

            })
          }}>
            logout
          </button>
            <div style={{"textAlign": "center"}}>
                <h3> -- About MyTacc --</h3>
                <p>
                    MyTacc stands for My T-Account. which is a concept in accounting that matches debit against credit.
                    <br />
                    Which incpired MyTacc, an app that helps people show their gratitude through actions that give back to their environment/community.
                    <br />
                    The app allows users to create a list of tasks that they can do to earn points, which acts as debit.
                    <br />
                    Users can also add debts, which are the things they are grateful for, which they need to pay off using the points they earn.
                    <br />
                    Everyone should start with themselves💚
                </p>
            </div>
        </div>
    </div>
  );
}

export default App;
