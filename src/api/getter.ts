import {repos} from "@mocks/repos";

export async function getter(endpoint: string):Promise<getterResponse> {
  return fetch(endpoint).then((response) => response.json())
  .then((data) => ({ data, ok: true }))
  .catch((error) => {throw { data: error, ok: false }});
}


export async function getUser(user: string):Promise<getUserResponse> {
  return getter(`https://api.github.com/users/${user}`);
}

export async function getRepos(user: string | null):Promise<getReposResponse> {
  if(!user) return { data: repos, ok: false };
  return getter(`https://api.github.com/users/${user}/repos`);
}