import Input from '../common/Input.jsx';
import Button from '../common/Button.jsx';

function RegisterForm() {
    return (
        <form>  
            <Input type="text" label="Username" placeholder="Type your username" />
            <Input type="email" label="Email" placeholder="Type your email" />
            <Input type="password" label="Password" placeholder="Type your password" />
            <Input type="password" label="Confirm Password" placeholder="Confirm your password" />
            <Button text="Register" />
        </form>
    );
}
export default RegisterForm;