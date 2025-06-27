import React from "react";
import { userManager } from "./auth/auth";
import NavBar from "./NavBar";

export default function LandingPage() {
  return (
    <div
      className="bg-containerBackground text-[#2D2A26] min-h-screen font-ebgaramond"
      style={{ minWidth: "360px" }}
    >
      <NavBar />

      <section className="relative text-center py-20 overflow-hidden min-h-[600px]">
        <picture>
          <source srcSet="/hero-background.webp" type="image/webp" />
          <img
            src="/hero-background.png"
            alt=""
            className="absolute inset-0 w-full h-full object-cover "
            aria-hidden="true"
            fetchpriority="high"
          />
        </picture>
        <div className="p-8 max-w-2xl mx-auto rounded-lg relative">
          <picture>
            <source srcSet="/logo-transparent-128.webp" type="image/webp" />
            <img
              src="/logo-transparent.png"
              alt="Fire Whisper Logo"
              width="128"
              height="128"
              className="w-32 h-32 mx-auto absolute top-2 left-1/2 transform -translate-x-1/2"
              fetchpriority="high"
            />
          </picture>

          <h1 className="text-7xl font-bold text-[#FFB84D] mt-28">
            Fire Whisper
          </h1>
          <p className="text-xl mt-4 text-[#F5E8D0]">
            Forge Your Saga in a World of Norse Legend
          </p>
          <div className="mt-6 flex flex-col sm:flex-row sm:space-x-4 space-y-4 sm:space-y-0 items-center justify-center">
            <button className="bg-[#FFB84D] text-[#2D2A26] px-6 py-2 rounded shadow hover:bg-[#ffc76d] font-bold">
              Begin Your Adventure
            </button>
            <button
              className="bg-[#FFB84D] text-[#2D2A26] px-6 py-2 rounded shadow hover:bg-[#ffc76d] font-bold"
              onClick={() => userManager.signinRedirect()}
            >
              Continue Your Saga
            </button>
          </div>
        </div>
      </section>

      <picture>
        <source srcSet="/separator-texture.webp" type="image/webp" />
        <img
          src="/separator-texture.png"
          alt=""
          className="w-full h-8 object-cover bg-center bg-repeat-x"
          style={{ backgroundSize: "auto 100%", backgroundColor: "#3E2713" }}
          aria-hidden="true"
        />
      </picture>

      {/* Features */}
      <section className="grid grid-cols-1 md:grid-cols-4 gap-6 px-8 py-10 bg-primaryBackground text-[#F5E8D0] text-center">
        {[
          {
            icon: (
              <picture>
                <source srcSet="/narrative-header-96.webp" type="image/webp" />
                <img
                  src="/narrative-header.png"
                  alt="Narrative Icon"
                  className="w-20 h-20 mx-auto"
                />
              </picture>
            ),
            title: (
              <>
                <span>Epic</span>
                <br />
                <span>Narrative</span>
              </>
            ),
            desc: "Engage in rich, interactive story with meaningful choices",
          },
          {
            icon: (
              <picture>
                <source srcSet="/character-header-96.webp" type="image/webp" />
                <img
                  src="/character-header.png"
                  alt="Character Icon"
                  className="w-20 h-20 mx-auto"
                />
              </picture>
            ),
            title: (
              <>
                <span>Character</span>
                <br />
                <span>Development</span>
              </>
            ),
            desc: "Build your hero with diverse skills, gear, and abilities",
          },
          {
            icon: (
              <picture>
                <source srcSet="/world-header-96.webp" type="image/webp" />
                <img
                  src="/world-header.png"
                  alt="World Icon"
                  className="w-20 h-20 mx-auto"
                />
              </picture>
            ),
            title: (
              <>
                <span>Immersive</span>
                <br />
                <span>World</span>
              </>
            ),
            desc: "Explore a realm filled with danger, mystery, and wonder",
          },
          {
            icon: (
              <picture>
                <source srcSet="/emberlyn-header-96.webp" type="image/webp" />
                <img
                  src="/emberlyn-header.png"
                  alt="Emberlyn Icon"
                  className="w-20 h-20 mx-auto"
                />
              </picture>
            ),
            title: (
              <>
                <span>Emberlyn</span>
                <br />
                <span>Guide</span>
              </>
            ),
            desc: "Seek guidance from a mystical fairy companion",
          },
        ].map((f, i) => (
          <div
            key={i}
            className="bg-containerBackground text-[#2D2A26] border border-[#2D2A26] p-6 rounded-xl shadow-lg"
          >
            <div className="text-[#FFB84D] text-4xl">{f.icon}</div>
            <h2 className="text-3xl font-bold mb-2 leading-snug min-h-[4.5rem] break-words whitespace-normal text-balance">
              {f.title}
            </h2>
            <p className="text-base leading-relaxed">{f.desc}</p>
          </div>
        ))}
      </section>

      <picture>
        <source srcSet="/separator-texture.webp" type="image/webp" />
        <img
          src="/separator-texture.png"
          alt=""
          className="w-full h-8 object-cover bg-center bg-repeat-x"
          style={{ backgroundSize: "auto 100%" }}
          aria-hidden="true"
        />
      </picture>

      {/* How It Works */}
      <section className="bg-primaryBackground text-[#2D2A26] py-10 text-center px-8">
        <div className="bg-containerBackground max-w-5xl mx-auto px-8 md:px-12 py-10 rounded-xl border-4 border-[#3E2713] shadow-lg">
          <h2 className="text-3xl font-bold tracking-wide mb-6">
            HOW IT WORKS
          </h2>
          <div className="flex flex-col md:flex-row justify-between items-center gap-12 relative">
            <div className="flex flex-col items-center">
              <picture>
                <source srcSet="/step-1.webp" type="image/webp" />
                <img
                  src="/step-1.png"
                  alt="Step 1"
                  className="w-20 h-20 mb-3"
                  loading="lazy"
                />
              </picture>
              <p className="text-base leading-relaxed">Create your character</p>
            </div>
            <div className="hidden md:block w-16 h-0.5 bg-primaryBackground"></div>
            <div className="flex flex-col items-center">
              <picture>
                <source srcSet="/step-2.webp" type="image/webp" />
                <img
                  src="/step-2.png"
                  alt="Step 2"
                  className="w-20 h-20 mb-3"
                  loading="lazy"
                />
              </picture>
              <p className="text-base leading-relaxed">Shape your destiny</p>
            </div>
            <div className="hidden md:block w-16 h-0.5 bg-primaryBackground"></div>
            <div className="flex flex-col items-center">
              <picture>
                <source srcSet="/step-3.webp" type="image/webp" />
                <img
                  src="/step-3.png"
                  alt="Step 3"
                  className="w-20 h-20 mb-3"
                  loading="lazy"
                />
              </picture>
              <p className="text-base leading-relaxed">Uncover the lore</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-primaryBackground text-[#F5E8D0] text-sm p-4 flex justify-between items-center">
        <div className="space-x-6">
          <a href="#">TERMS</a>
          <a href="#">PRIVACY</a>
          <a href="#">SUPPORT</a>
        </div>
      </footer>
    </div>
  );
}
