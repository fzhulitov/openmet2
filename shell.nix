{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.gcc         # Компилятор, который включает libstdc++
    pkgs.python3     # Python
    pkgs.poetry
    pkgs.python311Packages.numpy       # NumPy
    pkgs.python311Packages.pandas      # Pandas
    pkgs.python311Packages.aiohttp
    pkgs.python311Packages.sqlalchemy
    pkgs.python311Packages.openpyxl
  ];
}
