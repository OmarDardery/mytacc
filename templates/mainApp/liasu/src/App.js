import React, {useState} from 'react';
import Form from './component/form';
import "./css/index.css"
import Message from "./component/message";
import validateCode from "./component/functions/validateCode";


function App() {
    let [message, setMessage] = useState("");
    let [display, setDisplay] = useState("none");
    let [action, setAction] = useState("login");
    let [code , setCode] = useState("");
    let [error, setError] = useState("");
    let [username, setUsername] = useState("");
    let [email, setEmail] = useState("");
    let [password, setPassword] = useState("");
    return (
    <div className={"form-container"}>
        <Message message={message} display={display} close={()=>{
            setDisplay("none");
        }}  />
        <div className={"form-button-slider"}>
            <button onClick={() => {
                setAction("login");
            }} className={action === "login" ? "active" : ""}>
            <h1>Login</h1>
            </button>
            <button onClick={() => {
                setAction("signup");
            }} className={action === "login" ? "" : "active"}>
            <h1>Sign Up</h1>
            </button>
        </div>
        {action !== "confirm" ?
            <Form notify={()=>{
            setDisplay("block");
        }} email={email} password={password} username={username} setMessage= {setMessage} action = {action} setAction={setAction} setUsername={setUsername} setPassword={setPassword} setEmail={setEmail} />
            : <div className={"form"}>
        <h1>Confirm your email</h1>
        <p>We have sent you a confirmation email. Please check your inbox and click on the link to confirm your email address.</p>
                <input onChange={(e)=>{
                    setCode(e.target.value);
                }} type="text" value={code} name={"code"} />
                <p>{error}</p>
            <button onClick={()=>{
            if(code.length !== 6) {
                setError("Code must be 6 characters long");
            }else if(code.includes(" ")) {
                setError("Code must not contain spaces");
            }else {
                setError("");
                validateCode(code, email, username, password).then((response) => {
                    if(response.status === "success") {
                        window.location.href = "/home";
                    }else{
                        setError(response.error);
                    }
                })

            }
        }} className={"form-submit-button"}>Submit</button>
        </div>}

    </div>
    );
}

export default App;
