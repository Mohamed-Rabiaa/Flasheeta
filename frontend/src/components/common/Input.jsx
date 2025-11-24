function Input({type, label, placeholder}) {
    return (
    <div>
        <label>{label}</label>
        <input type={type} placeholder={placeholder} />
    </div>
    );
}
export default Input;