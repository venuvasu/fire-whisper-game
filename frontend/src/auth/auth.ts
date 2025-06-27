import { UserManager, WebStorageStateStore, Log } from "oidc-client-ts";

const redirectUri = `${window.location.origin}/callback`;

const cognitoAuthConfig = {
  authority: "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_ZejduSmCw",
  client_id: "17004bfsq9mf4ptkrqc93v4hes",
  redirect_uri: redirectUri,
  response_type: "code",
  scope: "email openid profile",
  loadUserInfo: true,
  monitorSession: true,
  // Start renewal 5 minutes before token expires
  accessTokenExpiringNotificationTimeInSeconds: 300,
  silentRequestTimeoutInSeconds: 10000,
};

export const userManager = new UserManager({
  ...cognitoAuthConfig,
  userStore: new WebStorageStateStore({ store: window.localStorage }),
  silent_redirect_uri: `${window.location.origin}/silent-renew.html`,
  automaticSilentRenew: true,
  includeIdTokenInSilentRenew: true,
  validateSubOnSilentRenew: true,
});

// Proactive token management
let renewalTimer: number | null = null;

// Set up proactive renewal
userManager.events.addUserLoaded((user) => {
  scheduleProactiveRenewal(user);
});

userManager.events.addUserUnloaded(() => {
  if (renewalTimer) {
    clearTimeout(renewalTimer);
    renewalTimer = null;
  }
});

function scheduleProactiveRenewal(user: any) {
  if (renewalTimer) {
    clearTimeout(renewalTimer);
  }

  const now = Math.floor(Date.now() / 1000);
  const expiresAt = user.expires_at;
  const timeUntilExpiry = expiresAt - now;

  // Renew 5 minutes before expiry (or at 75% of token lifetime, whichever is sooner)
  const renewalBuffer = Math.min(300, timeUntilExpiry * 0.25);
  const timeUntilRenewal = (timeUntilExpiry - renewalBuffer) * 1000;

  if (timeUntilRenewal > 0) {
    console.log(
      `Scheduling proactive renewal in ${Math.floor(
        timeUntilRenewal / 1000
      )} seconds`
    );

    renewalTimer = window.setTimeout(async () => {
      try {
        console.log("Proactively renewing token...");
        await userManager.signinSilent();
      } catch (error) {
        console.error("Proactive renewal failed:", error);
      }
    }, timeUntilRenewal);
  }
}

// Enhanced axios interceptor with better error handling
export function setupAxiosInterceptor(axios: any) {
  // Track ongoing renewal to prevent multiple simultaneous attempts
  let renewalPromise: Promise<any> | null = null;

  axios.interceptors.request.use(
    async (config: any) => {
      try {
        const user = await userManager.getUser();

        if (user && !user.expired) {
          config.headers.Authorization = `Bearer ${user.access_token}`;
        } else if (user && user.expired) {
          // If renewal is already in progress, wait for it
          if (renewalPromise) {
            try {
              const renewedUser = await renewalPromise;
              if (renewedUser) {
                config.headers.Authorization = `Bearer ${renewedUser.access_token}`;
              }
            } catch (error) {
              console.error("Renewal in progress failed:", error);
            }
          } else {
            // Start new renewal
            renewalPromise = userManager.signinSilent();
            try {
              const renewedUser = await renewalPromise;
              if (renewedUser) {
                config.headers.Authorization = `Bearer ${renewedUser.access_token}`;
              }
            } catch (error) {
              console.error("Failed to renew token in interceptor:", error);
              // Don't redirect to login here - let the 401 handler deal with it
            } finally {
              renewalPromise = null;
            }
          }
        }
      } catch (error) {
        console.error("Error in request interceptor:", error);
      }

      return config;
    },
    (error: any) => Promise.reject(error)
  );

  // Add response interceptor to handle 401s
  axios.interceptors.response.use(
    (response: any) => response,
    async (error: any) => {
      const originalRequest = error.config;

      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;

        // If renewal is already in progress, wait for it
        if (renewalPromise) {
          try {
            const user = await renewalPromise;
            if (user) {
              originalRequest.headers.Authorization = `Bearer ${user.access_token}`;
              return axios(originalRequest);
            }
          } catch (renewError) {
            console.error("Renewal failed during 401 retry:", renewError);
          }
        } else {
          // Try one more renewal attempt
          try {
            renewalPromise = userManager.signinSilent();
            const user = await renewalPromise;
            if (user) {
              originalRequest.headers.Authorization = `Bearer ${user.access_token}`;
              return axios(originalRequest);
            }
          } catch (renewError) {
            console.error("Token renewal failed on 401:", renewError);
            // Only redirect to login after all renewal attempts fail
            await userManager.signinRedirect();
          } finally {
            renewalPromise = null;
          }
        }
      }

      return Promise.reject(error);
    }
  );
}

export async function signOutRedirect() {
  // Clear any pending renewal timers
  if (renewalTimer) {
    clearTimeout(renewalTimer);
    renewalTimer = null;
  }

  await userManager.removeUser();
  const clientId = "17004bfsq9mf4ptkrqc93v4hes";
  const logoutUri = window.location.origin + "/";
  const cognitoDomain =
    "https://us-east-1zejdusmcw.auth.us-east-1.amazoncognito.com";
  window.location.href = `${cognitoDomain}/logout?client_id=${clientId}&logout_uri=${encodeURIComponent(
    logoutUri
  )}`;
}

// Helper function to get valid access token
export async function getAccessToken(): Promise<string | null> {
  try {
    const user = await userManager.getUser();

    if (!user) {
      return null;
    }

    if (user.expired) {
      // Try to renew
      const renewedUser = await userManager.signinSilent();
      return renewedUser?.access_token || null;
    }

    return user.access_token;
  } catch (error) {
    console.error("Error getting access token:", error);
    return null;
  }
}
