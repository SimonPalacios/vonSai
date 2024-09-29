
const Toast = (props: toastProps) => {
  const { title, text, close, footer } = props;

  return (
    <article className="fixed transform -translate-x-1/2 top-1/4 left-1/2 p-4 rounded-xl
    w-1/3 dark:bg-teal-900/50 backdrop-blur-lg">
      <header className="border-b-2 font-bold text-black ">
        <h1><small className="text-slate-800">{title}</small>
          <span
            className="float-right mr-2 cursor-pointer hover:text-white"
            onClick={close}
          >
            X
          </span>
        </h1>
      </header>
      <p className="p-4 text-sm font-bold overflow-scroll max-h-[8rem]">{text}</p>
      {footer && (
        <footer className="flex flex-wrap border-t-2 pt-3 border-slate-300">
          {footer.map((topic: string) => (
            <span
              key={topic}
              className="m-1 py-1 px-2 bg-slate-50/50 text-sm text-gray-700 rounded-md"
            >
              {topic.toUpperCase()}
            </span>
          ))}
        </footer>
      )}
    </article>
  );
};

export default Toast;