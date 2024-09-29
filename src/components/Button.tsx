
const Button = (props: buttonProps) => {
  const { icon, href, ...args } = props;
  return (
    (!href && (
      <button
        {...args}
        className="m-1 hover:ring-2"
      >
        {icon}
      </button>
    )) || (
      <a
        {...args}
        className="m-1 hover:ring-2"
      >
        {icon}
      </a>
    )
  );
};

export default Button;