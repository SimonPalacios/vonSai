import Button from "./Button";
import Toast from "./Toast";

const Card = (props: cardProps) => {
  const { item, setToast, closeToast } = props;
  const arrowDownload = "⬇️";
  const arrowGo = "🔗";
  const infoIcon = "ℹ️";
  const date = (created: string) => /\d{4}-\d{2}-\d{2}/.exec(created)![0];

  const onClick = () => {
    const props = {
      title: "Repositorio ->" + item.name,
      text: item.description??"No hay descripción",
      footer: item.topics,
      close: closeToast,
    };
    setToast(<Toast {...props} />);
  };

  const buttons = [
    { icon: arrowGo, title: "Ir", href: item.html_url, id: "ir" },
    { icon: arrowDownload, title: "Descargar", id: "download", href: item.clone_url },
    { icon: infoIcon, title: "Descripción", id: "info", onClick },
  ];

  return (
    <section className="card border-2 border-spacing-2 border-gray-200 rounded-xl p-4 shadow-lg shadow-gray-400">
      <p className="text-sm text-slate-600">{item.owner.login.toUpperCase().replace(/-/g, " ")}</p>
      <header className="px-2 text-lg bg-slate-200 rounded-md">
        <p className="text-ellipsis font-bold ">{item.name.replace(/[-_]/g, " ")}</p>
        <small className="mx-2 text-gray-500 font-bold ">
          Creado: {date(item.created_at)} | Modificado: {date(item.updated_at)}
        </small>
      </header>
      <nav className="flex justify-around mt-2 pt-3 border-t border-teal-400">
        {item.stargazers_count} ⭐
        <div id="buttons">
          {buttons.map((button) => (
            <Button
              key={button.id}
              {...button}
            />
          ))}
        </div>
      </nav>
    </section>
  );
};

export default Card;