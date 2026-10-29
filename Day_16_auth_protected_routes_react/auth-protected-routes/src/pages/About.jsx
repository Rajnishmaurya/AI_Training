import {useAuth} from "../context/AuthContext";

export default function About(){
    const {user}=useAuth();

    return (
        <div className="container">
            <h1>About Page</h1>
            <p>This is a protected about page.</p>
            <p>Welcome, {user.email}!</p>

            <p>Only logged-in users can see this page.</p>
        </div>
    );
}