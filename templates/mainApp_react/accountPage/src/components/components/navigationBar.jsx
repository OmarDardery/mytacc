import React from "react";

function NavigationBar() {
    return (
        <div className={"navigation-bar-container"}>
            <div className="navigation-bar">
                <h1 className={"header-title"} onClick={()=>{
                    window.location.href = "/";
                }}>MyTacc</h1>
            </div>
            <div style={{height: "10vh"}}>

            </div>
        </div>
    );
}

export default NavigationBar;