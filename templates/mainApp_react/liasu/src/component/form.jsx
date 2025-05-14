import React, {useState} from 'react';
import validateEmail from './functions/sendCode';
import validateUser from './functions/validateUser';


function Form(props) {
    let [confirmPassword, setConfirmPassword] = useState("");
    async function handleSignUp () {
        if(props.password !== confirmPassword) {
            props.setMessage("Passwords do not match");
            props.notify();
        }else{
            if(props.password.length < 8 || props.password.length > 15) {
                props.setMessage("Password must be between 8 and 15 characters");
                props.notify();
            }else if (props.username.length < 8 || props.username.length > 15){
                props.setMessage("Username must be between 8 and 15 characters");
                props.notify();
            }else{
                let response = await validateEmail(props.username, props.email);
                if(response.status === "success") {
                    props.setAction("confirm");
                }else{
                    props.setMessage( String(response.error) );
                    props.notify();
                }

            }
        }
    }
    async function handleSignIn() {
        let response = await validateUser(props.username, props.password);
        if(response.status === "success") {
            window.location.href = "/accountPage";
        }else{
            props.setMessage(response.error);
            props.notify();
        }
    }
    return (<div className={"form"}>
        <div className={"form-field"}>
            <label htmlFor="username">Username:</label>
            <input type="text" onChange={(e)=>{
                props.setUsername(e.target.value);
            }} value={props.username} name="username" />
        </div>
        {(props.action === "signup") ?
            <div className={"form-field"}>
                <label htmlFor="email">Email:</label>
                <input onChange={(e)=>{
                props.setEmail(e.target.value);
            }} value={props.email} name={"email"} type="email" />
            </div>
            : <div></div>}
        <div className={"form-field"}>
            <label htmlFor="password">Password:</label>
            <input onChange={(e)=>{
                props.setPassword(e.target.value);
            }} value={props.password} type="password" />
        </div>
        {(props.action === "signup") ?
            <div className={"form-field"}>
                <label htmlFor="confirmPassword">Confirm Password:</label>
                <input onChange={(e)=>{
                setConfirmPassword(e.target.value);
            }} value={confirmPassword} name={"confirmPassword"} type="password" />
            </div>
            : <div></div>}
        <button onClick={()=>{
            if(props.action === "signup") {
                handleSignUp();
            }else {
                handleSignIn();
            }
        }} className={"form-submit-button"}>Submit</button>
    </div>);
}

export default Form;