import React, { useState, useRef, useEffect, useCallback } from "react";
import { Link } from "react-router-dom";
import { userManager, signOutRedirect } from "./auth/auth";

interface NavBarProps {
  user: any;
}

const NAV_HEIGHT = 64; // px

const NavBar: React.FC<NavBarProps> = ({ user }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef(null);

  const handleClickOutside = useCallback((event: MouseEvent) => {
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target as Node)
    ) {
      setOpen(false);
    }
  }, []);

  useEffect(() => {
    if (open) {
      document.addEventListener("mousedown", handleClickOutside);
      return () => {
        document.removeEventListener("mousedown", handleClickOutside);
      };
    }
  }, [open, handleClickOutside]);

  if (!user)
    return (
      <>
        <nav className="bg-primaryBackground text-[#F5E8D0] p-4 flex justify-between items-center shadow-md">
          <div className="text-xl font-bold">FIRE WHISPER</div>
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="focus:outline-none"
              aria-label="Open main menu"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          </div>
          <div className="hidden md:flex space-x-6">
            <button
              className="hover:text-[#FFB84D]"
              onClick={() => userManager.signinRedirect()}
            >
              LOGIN
            </button>
            <button className="hover:text-[#FFB84D]">REGISTER</button>
          </div>
        </nav>
        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="bg-primaryBackground px-4 py-2 flex flex-col space-y-2 md:hidden">
            <button
              className="hover:text-[#FFB84D] text-left"
              onClick={() => userManager.signinRedirect()}
            >
              LOGIN
            </button>
            <button className="hover:text-[#FFB84D] text-left">REGISTER</button>
          </div>
        )}
      </>
    );

  return (
    <nav className="fixed top-0 left-0 w-full z-10 bg-primaryBackground text-primaryText">
      <div className="mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center h-full">
              <img
                className="h-10 w-auto"
                src="/nav-logo.png"
                alt="Fire Whisper Logo"
                style={{
                  height: `${NAV_HEIGHT - 16}px`,
                  width: "auto",
                  objectFit: "contain",
                }}
              />
            </Link>
          </div>

          {/* Right user avatar + dropdown */}
          <div className="relative" ref={dropdownRef}>
            <button
              type="button"
              className="flex items-center rounded-full bg-gray-900 text-sm focus:outline-none focus:ring-2 focus:ring-white"
              id="user-menu-button"
              aria-expanded={open}
              aria-haspopup="true"
              onClick={() => setOpen((v) => !v)}
            >
              <span className="sr-only">Open user menu</span>
              <picture>
                <source srcSet="/logo-transparent-128.webp" type="image/webp" />
                <img
                  className="h-10 w-10 rounded-full object-cover"
                  src="/logo-transparent.png"
                  alt="User avatar"
                />
              </picture>
              <svg
                className={`ml-2 h-4 w-4 text-white transition-transform ${
                  open ? "rotate-180" : ""
                }`}
                fill="none"
                stroke="currentColor"
                strokeWidth={2}
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>

            {/* Dropdown panel */}
            {open && (
              <div
                className="absolute right-0 z-20 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                role="menu"
                aria-orientation="vertical"
                aria-labelledby="user-menu-button"
                tabIndex={-1}
              >
                <button
                  className="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-red-500 hover:text-white"
                  role="menuitem"
                  tabIndex={-1}
                  id="user-menu-item-0"
                  onClick={() => {
                    setOpen(false);
                    signOutRedirect();
                  }}
                >
                  Sign Out
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
