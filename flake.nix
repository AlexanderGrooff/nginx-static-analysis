{
  description = "A Nix-flake-based Python development environment";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs";
  };

  outputs =
    { self
    , flake-utils
    , nixpkgs
    }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      # Define constants
      pyVersion = "311";
      venvDir = "./.venv";
      requirements = "./requirements/development.txt";

      overlays = [
        (self: super: {
          python = super."python${pyVersion}";
        })
      ];

      pkgs = import nixpkgs { inherit overlays system; };
    in
    {
      devShells.default = pkgs.mkShell {
        inherit venvDir;
        # Define system packages to be present
        buildInputs = with pkgs; [
            python
            virtualenv
        ] ++
          # Python system packages
          (with pkgs."python${pyVersion}Packages"; [
            wheel
            venvShellHook
            pre-commit
        ]);

        # This is to expose the venv in PYTHONPATH
        postShellHook = ''
            PYTHONPATH=\$PWD/\${venvDir}/\${pkgs.python.sitePackages}/:\$PYTHONPATH
            # Check if the requirements are installed
            pip freeze | grep -q loguru || pip install -r ${requirements}
        '';
      };
    });
}
