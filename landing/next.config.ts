import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Static HTML export, served at "/" next to the Flask app (see ../vercel.json).
  output: "export",
  /* config options here */
};

export default nextConfig;
