import React, { useEffect } from "react";
import { userManager } from "./auth/auth";
import GameLoading from "./GameLoading";
import * as amplitude from "@amplitude/analytics-browser";

export default function Callback() {
  useEffect(() => {
    userManager.signinRedirectCallback().then(() => {
      userManager.getUser().then((user) => {
        amplitude.setUserId(user?.profile.sub);
        window.location.href = "/";
      });
    });
  }, []);

  return <GameLoading />;
}
