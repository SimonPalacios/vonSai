import { getUser } from "@api/getter";
import { usersData } from "@mocks/usersData";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";


async function getUsersData(users: string[]): Promise<getUserResponse[]> {
  return await Promise.all(users.map(getUser));
}

export default function UsersList() {
  const [users, setUsers] = useState<UserI[]>([]);
  const navigate = useNavigate();
  useEffect(() => {
    (async () => {
      getUsersData(["agusrnfr", "Fabian-Martinez-Rincon", "guadaevequoz", "EzequielReale", "MarianoGonzalez98"])
        .then((usersResponse)=>{
          const badResponses = usersResponse.filter(({ok}) => !ok);
          setUsers(!!(badResponses.length)?usersData:usersResponse.map(({data}) => data));
        })
        .catch((error) => {
          console.error("Error get user data", {error});
          navigate("/repositorios", { state: { user: null } });
        });
    })();
  }, []);

  const handleNavigate = (event: React.MouseEvent<HTMLButtonElement>) => {

    /* console.log(new Date().toLocaleTimeString(), "Navigate to: ", {name: event.currentTarget.name, event}); */

    navigate("/repositorios", { state: { user: event.currentTarget.name } });
  }

  return (
    users.length > 0 && (
      <article className={`grid grid-cols-[100%] md:grid-cols-4 grid-flow-row gap-4 p-2 md:p-4 select-none overflow-scroll`}>
        {users.map((user) => (
          <section
            key={user.id}
            className="p-2 md:p-4 border rounded-lg shadow-md shadow-gray-600 "
          >
            <h2 className="text-xl font-semibold mb-2 text-wrap">{user.login?.replace(/[-_]/g, " ")}</h2>
            <a
              href={user.html_url}
              className="text-blue-500 hover:underline max-h-10 overflow-x-hidden text-ellipsis "
            >
              {user.html_url?.replace(/(https:\/\/).*(\.\w{2,3})/, "")}
            </a>
            <p className="text-gray-700 mt-2">{user.bio}</p>
            <p className="text-gray-700 mt-2">Repos: {user.public_repos}</p>
            <p className="text-gray-700 mt-2">Updated: {/(.*)T(.*):\d+Z/.exec(user.updated_at)![1]}</p>
            <p>Fallowers: {user.followers}</p>
            {/* ADD rigth arrow svg */}
            <button name={user.login} className="ring-2 hover:ring-blue-300 float-right" onClick={handleNavigate}>
            <ArrowSvg className="w-6 h-6"/>

            </button>
          </section>
        ))}
      </article>
    )
  );
}


const ArrowSvg = (props:any) => (
  <svg
  xmlns="http://www.w3.org/2000/svg"
  fill="none"
  viewBox="0 0 24 24"
  strokeWidth={1.5}
  stroke="currentColor"
  {...props}
>
  <path
    strokeLinecap="round"
    strokeLinejoin="round"
    d="M8.25 4.5l7.5 7.5-7.5 7.5"
  />
</svg>)