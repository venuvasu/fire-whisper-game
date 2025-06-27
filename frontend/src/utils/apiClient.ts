import { userManager } from "../auth/auth";

const BASE_URL = "https://dev.firewhisper.io/api";

interface ApiRequestOptions {
  path: string;
  method?: string;
  token?: string | null;
  body?: any;
  headers?: Record<string, string>;
}

export async function apiRequest({
  path,
  method = "GET",
  token,
  body,
  headers = {},
}: ApiRequestOptions) {
  const url = `${BASE_URL}${path}`;

  // Get fresh token if not provided
  let authToken = token;
  if (!authToken) {
    const user = await userManager.getUser();
    authToken = user?.id_token || null;
  }

  const options = {
    method,
    headers: {
      ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
      ...(body ? { "Content-Type": "application/json" } : {}),
      ...headers,
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  };

  const res = await fetch(url, options);

  // Handle 401 with one retry
  if (res.status === 401 && authToken) {
    try {
      // Try to get a fresh token
      const renewedUser = await userManager.signinSilent();
      if (renewedUser?.id_token) {
        // Retry the request with the new token
        const retryOptions = {
          ...options,
          headers: {
            ...options.headers,
            Authorization: `Bearer ${renewedUser.id_token}`,
          },
        };

        const retryRes = await fetch(url, retryOptions);

        if (!retryRes.ok) {
          const errorText = await retryRes.text();
          throw new Error(
            `API error: ${retryRes.status} ${retryRes.statusText} - ${errorText}`
          );
        }

        return retryRes.json();
      }
    } catch (error) {
      console.error("Token renewal failed:", error);
    }
  }

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(
      `API error: ${res.status} ${res.statusText} - ${errorText}`
    );
  }

  return res.json();
}
