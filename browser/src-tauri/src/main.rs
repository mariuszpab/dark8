#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod agent_bridge;
mod browser_state;

use browser_state::BrowserState;

fn main() {
    tauri::Builder::default()
        .manage(BrowserState::default())
        .invoke_handler(tauri::generate_handler![
            agent_bridge::agent_open_url,
            agent_bridge::agent_ping
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
