import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useRef,
} from "react";
import { userManager, signOutRedirect } from "./auth";
import { User } from "oidc-client-ts";

interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  login: () => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
  isRenewing: boolean; // Add this for components that need to know
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true); // Only true on initial load
  const [isRenewing, setIsRenewing] = useState(false);
  const tokenExpirationHandlerRef = useRef<(() => void) | null>(null);

  // Initial user load - only time we set loading to true
  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      const u = await userManager.getUser();
      if (u && !u.expired) {
        setUser(u);
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error("Error loading user:", error);
      setUser(null);
    } finally {
      setLoading(false); // Only set to false, never back to true
    }
  };

  // Storage event listener for cross-tab synchronization
  useEffect(() => {
    const onStorage = (e: StorageEvent) => {
      if (e.key?.includes("oidc.user")) {
        // Don't set loading state for cross-tab updates
        userManager.getUser().then((u) => {
          setUser(u && !u.expired ? u : null);
        });
      }
    };

    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  // Token expiration and renewal handlers
  useEffect(() => {
    // Handler for token about to expire
    const handleTokenExpiring = () => {
      console.log("Access token expiring soon, preparing for silent renew...");
      setIsRenewing(true);
    };

    // Handler for token expiration
    const handleTokenExpired = async () => {
      console.log("Access token expired, attempting silent renew...");
      setIsRenewing(true);

      try {
        const renewedUser = await userManager.signinSilent();
        if (renewedUser) {
          setUser(renewedUser);
          console.log("Silent renew successful");
        }
      } catch (err) {
        console.error("Silent renew failed:", err);
        setUser(null);
      } finally {
        setIsRenewing(false);
      }
    };

    // Handler for successful silent renew
    const handleUserLoaded = (loadedUser: User) => {
      console.log("User loaded/renewed:", loadedUser);
      setUser(loadedUser);
      setIsRenewing(false);
      // Don't touch loading state - it stays false after initial load
    };

    // Handler for signout
    const handleUserUnloaded = () => {
      console.log("User signed out");
      setUser(null);
      // Don't set loading - user explicitly signed out
    };

    // Handler for silent renew error
    const handleSilentRenewError = (error: Error) => {
      console.error("Silent renew error:", error);
      setIsRenewing(false);
      // Don't immediately clear user - let token expiration handler deal with it
    };

    // Store reference to handler for cleanup
    tokenExpirationHandlerRef.current = handleTokenExpired;

    // Add event listeners
    userManager.events.addAccessTokenExpiring(handleTokenExpiring);
    userManager.events.addAccessTokenExpired(handleTokenExpired);
    userManager.events.addUserLoaded(handleUserLoaded);
    userManager.events.addUserUnloaded(handleUserUnloaded);
    userManager.events.addSilentRenewError(handleSilentRenewError);

    // Cleanup
    return () => {
      userManager.events.removeAccessTokenExpiring(handleTokenExpiring);
      userManager.events.removeAccessTokenExpired(handleTokenExpired);
      userManager.events.removeUserLoaded(handleUserLoaded);
      userManager.events.removeUserUnloaded(handleUserUnloaded);
      userManager.events.removeSilentRenewError(handleSilentRenewError);
    };
  }, []);

  const login = async () => {
    try {
      await userManager.signinRedirect();
    } catch (error) {
      console.error("Login error:", error);
    }
  };

  const logout = async () => {
    try {
      await signOutRedirect();
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  const value: AuthContextValue = {
    user,
    isAuthenticated: !!user && !user.expired,
    login,
    logout,
    loading,
    isRenewing, // Expose this for components that care
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
