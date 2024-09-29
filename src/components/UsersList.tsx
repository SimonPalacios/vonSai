import { getUser } from "@api/getter";
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
        .then((usersData)=>{
          const badResponses = usersData.filter(({ok}) => !ok);
          if (!(badResponses.length)) throw { error: badResponses.map(({data}) => data) };
          setUsers(usersData.map(({data}) => data));
        })
        .catch((error) => {
          console.error(error);
          navigate("/Repositorios", { state: { user: null } });
        });
    })();
  }, []);

  return (
    users.length > 0 && (
      <article className={`grid grid-cols-4 grid-flow-row gap-4 p-4 select-none`}>
        {users.map((user) => (
          <section
            key={user.id}
            className="col p-4 border rounded-lg shadow-md shadow-gray-600"
          >
            <h2 className="text-xl font-semibold mb-2">{user.login}</h2>
            <a
              href={user.html_url}
              className="text-blue-500 hover:underline"
            >
              {user.html_url}
            </a>
            <p className="text-gray-700 mt-2">{user.bio}</p>
            <p className="text-gray-700 mt-2">Repos: {user.public_repos}</p>
            <p className="text-gray-700 mt-2">Updated: {/(.*)T(.*):\d+Z/.exec(user.updated_at)![1]}</p>
            <p>Fallowers: {user.followers}</p>
          </section>
        ))}
      </article>
    )
  );
}
