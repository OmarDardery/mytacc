import React from 'react';
import getCookie from "./components/getCookie"
import NavigationBar from "./components/components/navigationBar";
function App() {
  return (
    <div style={{ textAlign: 'center' }}>
      <NavigationBar />
        <div style={{ height: "10vh"}}>

        </div>
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
    </div>
  );
}

export default App;
