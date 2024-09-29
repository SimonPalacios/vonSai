import { repos } from "@mocks/repos";

export async function getter(endpoint: string): Promise<getterResponse> {
  return fetch(endpoint)
    .then(async (response) => ({ status: response.status === 200, response: await response.json() }))
    .then(({ status, response }) => ({ data: response, ok: status }))
    .catch((error) => {
      throw { data: error, ok: false };
    });
}

export async function getUser(user: string): Promise<getUserResponse> {
  return getter(`https://api.github.com/users/${user}`);
}

export async function getRepos(user: string | null): Promise<getReposResponse> {
  if (!user) return { data: repos, ok: false };
  return getter(`https://api.github.com/users/${user}/repos`).then(({ data, ok }) => {
    return ok ? { data, ok } : { data: { ...data, repos }, ok };
  });
}
