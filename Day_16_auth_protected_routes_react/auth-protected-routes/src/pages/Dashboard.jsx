import {useAuth} from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Dashboard(){
    const {user,logout}=useAuth();
    const navigate=useNavigate();

    function handleLogout(){
        logout();
        navigate("/login",{replace:true});
    }

    return (
        <div className="container">
        <h1>Private Dashboard</h1>
        <p> Welcome, {user.email}!</p>
        <p>You can see thids page because you are logged in.</p>
        <button onClick={handleLogout}>Logout</button>
        </div>
    );

}