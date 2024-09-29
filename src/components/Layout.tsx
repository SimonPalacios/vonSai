import { Outlet } from "react-router-dom";

interface AsideItem {
  name: string;
  path: string;
  icon?: string;
}

const StyleAside = (props:any) => {
  const items = (props.items as AsideItem[]);
  return (
    <aside className="flex flex-col p-4  bg-gray-600 dark:bg-teal-900 shadow-xl shadow-gray-900 rounded-sm">
      <span className="border-b border-amber-700 text-2xl font-bold text-gray-300">
        Sp
        </span>
      {items.map(({path, name, icon}) => (
        <>
        {icon}
        <a
          href={path}
          className="p-2 text-white"
          key={name}
        >
          {name}
        </a>
        </>
      ))}
    </aside>
  );
};

export default function Layout() {

  const items = [
    { name: "Home", path: "/" },
    { name: "Users", path: "/users" },
  ]

  return (
    <main className="grid grid-cols-[8rem_1fr] grid-rows-[100dvh]">
      <StyleAside {...{items}}/>
      <Outlet />
    </main>
  );
}
