// src/silent-renew.ts
import { UserManager, WebStorageStateStore } from "oidc-client-ts";

// Use the same config as your main auth.ts
const cognitoAuthConfig = {
  authority: "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_ZejduSmCw",
  client_id: "17004bfsq9mf4ptkrqc93v4hes",
  redirect_uri: `${window.location.origin}/callback`,
  response_type: "code",
  scope: "email openid profile",
};

const userManager = new UserManager({
  ...cognitoAuthConfig,
  userStore: new WebStorageStateStore({ store: window.localStorage }),
  silent_redirect_uri: `${window.location.origin}/silent-renew.html`,
  automaticSilentRenew: true,
});

// Handle the silent renewal callback
userManager
  .signinSilentCallback()
  .then(() => {
    console.log("Silent renew successful");
  })
  .catch((err) => {
    console.error("Silent renew error:", err);
  });
