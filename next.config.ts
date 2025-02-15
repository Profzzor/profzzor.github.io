import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  trailingSlash: true,  // Optional: Adds trailing slashes to URLs
  output: "export",     // Enables static export of the app
};

export default nextConfig;
