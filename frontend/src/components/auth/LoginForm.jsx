import Input from '../common/Input';
import Button from '../common/Button';
import Link from '../common/Link';

function LoginForm() {
    return (
        <>
        <form>
            <Input type="text" label="Email" placeholder="Type your Email" />
            <Input type="password" label="Password" placeholder="Type your password" />
            <Button text="Login" />
        </form>
        </>
    );
}
export default LoginForm;