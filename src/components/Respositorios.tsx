import { getRepos } from "@api/getter";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Toast from "./Toast";
import Card from "./Card";


export default function Repositorios() {
  const {
    state: { user },
  } = useLocation();
  const [repositorios, setRepositorios] = useState<RootObject[]>([]);
  const [toast, setToast] = useState<any>(false);

  useEffect(() => {
    (async () => {
      if (!user) {
        const props = {
          title: "No se ha seleccionado un usuario",
          text: "Parece que no se pudo obtener un usuario al entrar a la página. Se muestran todos los repositorios guardados. Capaz se bloqueo el acceso desde la api de github por la cantidad de requerimientos. Si pasa eso cada vez que entres a la página de usuarios te va a redireccionar a los repositorios.",
          close: closeToast,
        };
        setToast(<Toast {...props} />);
      }
      getRepos(user)
        .then(({ data, ok }) => {
          console.log({ data, ok });
          if (!ok && !data.length) throw { error: data };
          setRepositorios(data.sort((a, b) => b.stargazers_count - a.stargazers_count));
        })
        .catch((e) => {
          const { error: { message, repos} } = e;
          console.error("[ERROR][COMPONENT]", { message, repos });
          setToast(<Toast {...{
            title: "IP bloqueada. Repositorios locales",
            text: message,
            close: closeToast,
          }} />);
          setRepositorios(repos||[]);
        });
    })();
  }, []);

  const closeToast = () => setToast(false);

  return repositorios.length && (
    <article className="grid lg:grid-cols-3 md:grid-cols-2 sm:grid-cols-1 grid-flow-row gap-4 p-4 select-none relative max-h-screen overflow-scroll">
      {repositorios.map((repo) => (
        <Card
          key={repo.id}
          item={repo}
          {...{ setToast, closeToast }}
        />
      ))}
      {toast}
    </article>
  );
}
