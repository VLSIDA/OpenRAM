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
            # Pip wheels (e.g. numpy in .venv) need common shared libs at runtime on Nix.
            LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
              pkgs.stdenv.cc.cc.lib
              pkgs.zlib
            ];

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

              # Python + pip (user installs, venvs; prefer Nix where possible)
              pkgs.python3
              pkgs.python3Packages.pip
            ];

            shellHook = ''
              export OPENRAM_USE_CONDA=0
              # PEP 668: Nix `python3` is externally managed. Put a repo-local venv first on PATH
              # so `make library` uses it. Use $PWD (writable checkout), not `toString self` (nix store).
              OPENRAM_VENV="''${OPENRAM_HOME}/.venv"
              if [ ! -x "$OPENRAM_VENV/bin/python3" ]; then
                echo "OpenRAM: creating venv at $OPENRAM_VENV"
                ${pkgs.python3}/bin/python3 -m venv "$OPENRAM_VENV"
              fi
              export VIRTUAL_ENV="$OPENRAM_VENV"
              export PATH="$OPENRAM_VENV/bin:$PATH"
              echo "OpenRAM: Nix devShell (venv on PATH: $OPENRAM_VENV)"
            '';
          };
        });
    };
}

