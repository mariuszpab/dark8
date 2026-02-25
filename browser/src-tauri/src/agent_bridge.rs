use tauri::Manager;
use tauri::State;
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
pub struct OpenUrlPayload {
    pub url: String,
}

#[derive(Serialize)]
pub struct UrlResponse {
    pub status: String,
    pub title: Option<String>,
    pub url: String,
}

// Simple command to be called from the agent via HTTP/WebSocket or gh tool
#[tauri::command]
pub async fn agent_open_url(payload: OpenUrlPayload, app_handle: tauri::AppHandle) -> Result<UrlResponse, String> {
    // In a full app we'd route this to the WebView instance; for now, acknowledge receipt.
    Ok(UrlResponse {
        status: "ok".to_string(),
        title: None,
        url: payload.url,
    })
}

#[tauri::command]
pub async fn agent_ping() -> Result<String, String> {
    Ok("pong".into())
}
