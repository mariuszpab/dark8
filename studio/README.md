# DARK8 Studio (Tauri scaffold)

This directory contains a minimal Tauri scaffold for `DARK8_STUDIO`.

Setup (requires Rust & Node)

```bash
# Install Rust: https://rustup.rs/
rustup toolchain install stable
cargo install create-tauri-app # optional

# From project root:
cd studio
cargo build
cargo run
```

Development

During development, you can point the Tauri web assets to the `web/` folder (Monaco/UI) by configuring Tauri dev server or using `tauri dev` with appropriate frontend tooling. See Tauri docs for more details.
