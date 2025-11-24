import LoginForm from '../components/auth/LoginForm.jsx';
import Card from '../components/common/Card.jsx';
import Link from '../components/common/Link.jsx';

const LoginPage = () => {
  return (
    <Card title="Login">
      <LoginForm />
      <p className="text-sm text-center mt-4">
         Don't have an account? <Link href="/register" text="Sign up" />
      </p>
    </Card>
  );
};

export default LoginPage;
