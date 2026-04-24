{
  description = "Frechy - French grammar practice CLI";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pythonEnv = pkgs.python3.withPackages (ps: [ 
        ps.httpx
        ps.rich
        ps.python-dotenv
      ]);
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          pythonEnv
          pkgs.ruff
        ];
        shellHook = ''
          export PYTHONPATH="${self}"
        '';
      };
    };
}
