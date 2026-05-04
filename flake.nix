{
  description = "OpenRAM development environment (Nix)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f system);
    in
    {
      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        {
          default = pkgs.mkShell {
            packages = [
              # FOSSI PDK ciel (nixpkgs `ciel` is unrelated: AOSC ciel-rs, wants root)
              pkgs.pdk-ciel

              # EDA / verification tools
              pkgs.klayout
              pkgs.magic-vlsi
              # Use the LVS-focused netgen package; the generic netgen package
              # may require a local build that can fail on some hosts.
              pkgs.netgen-vlsi
              pkgs.ngspice
              pkgs.iverilog
              pkgs.xyce
              pkgs.xyce-parallel
              pkgs.trilinos
              pkgs.trilinos-mpi

              # Dev conveniences
              pkgs.git
              pkgs.gnumake
              pkgs.curl
            ];

            shellHook = ''
              export OPENRAM_USE_CONDA=0
              echo "OpenRAM: using tools from Nix devShell"
            '';
          };
        });
    };
}

