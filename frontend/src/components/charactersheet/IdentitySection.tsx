import React from "react";
import { GiElfHelmet } from "react-icons/gi";

const SectionHeader = ({ icon: Icon, title }) => (
  <div className="flex items-center text-2xl font-bold pb-1 mb-2">
    <Icon className="mr-2 text-[#3E2713]" size={28} />
    <span className="uppercase tracking-wide">{title}</span>
  </div>
);

const AppearanceDisplay = ({ appearance }) => (
  <p>
    <strong>Appearance:</strong> {appearance}
  </p>
);

const BackgroundDisplay = ({ background }) => (
  <p>
    <strong>Background:</strong> {background}
  </p>
);

const PathDisplay = ({ path }) => {
  if (!path) return null;

  return (
    <p>
      <strong>Path:</strong> {path.ethos} / {path.approach}
    </p>
  );
};

const IdentitySection = ({ identity }) => {
  if (!identity) return null;

  return (
    <section>
      <SectionHeader icon={GiElfHelmet} title="Identity" />
      <div className="space-y-2">
        <AppearanceDisplay appearance={identity.appearance} />
        <BackgroundDisplay background={identity.background} />
        <PathDisplay path={identity.path} />
      </div>
    </section>
  );
};

export default IdentitySection;
