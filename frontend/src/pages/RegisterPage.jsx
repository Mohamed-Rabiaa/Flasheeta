import Card from "../components/common/Card";
import RegisterForm from "../components/auth/RegisterForm";
import Link from '../components/common/Link.jsx';

const RegisterPage = () => {
  return (
    <Card title="Register">
      <RegisterForm />
      <p className="text-sm text-center mt-4">
         Already have an account? <Link href="/login" text="Login" />
      </p>
    </Card>);
};

export default RegisterPage;
