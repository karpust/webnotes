import {useLocation} from "react-router-dom";
import React from "react";

//  компонент будет отображен при переходе по несуществующему адресу:
const NotFound404 = () => {
    let {pathname} = useLocation()
    return(
        <div>
            <h1>Page not found: {pathname}</h1>
        </div>
    )
}
export default NotFound404