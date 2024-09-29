
const Button = (props: buttonProps) => {
  const { icon, href, ...args } = props;
  return (
    (!href && (
      <button
        {...args}
        className="m-1 hover:ring-2"
        type="button"
      >
        {icon}
      </button>
    )) || (
      <a
        {...{...args, href}}
        className="m-1 hover:ring-2 cursor-pointer"
      >
        {icon}
      </a>
    )
  );
};

export default Button;