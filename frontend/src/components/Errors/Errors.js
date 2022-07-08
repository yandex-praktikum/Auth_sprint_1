import React from 'react'
import '../Preloader/Preloader.css'

const Errors = (props) => {

    return (
        <div className={(props.errorFromServer.length > 0 && !props.isLoading) ? "preloader" : "preloader preloader__hided"}>
            <div className="preloader__errors">
                <p className="preloader__error">{props.errorFromServer}</p>
            </div>
        </div>
    )
};

export default Errors;




