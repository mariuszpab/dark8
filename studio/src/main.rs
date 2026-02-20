#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct ChatReq {
    prompt: String,
    model: Option<String>,
}

#[tauri::command]
async fn fs_read(path: String) -> Result<serde_json::Value, String> {
    let url = format!("http://127.0.0.1:8000/fs/read?path={}", urlencoding::encode(&path));
    let res = reqwest::get(&url).await.map_err(|e| e.to_string())?;
    let j = res.json::<serde_json::Value>().await.map_err(|e| e.to_string())?;
    Ok(j)
}

#[tauri::command]
async fn fs_write(path: String, content: String) -> Result<serde_json::Value, String> {
    let url = format!("http://127.0.0.1:8000/fs/write?path={}", urlencoding::encode(&path));
    let client = reqwest::Client::new();
    let res = client
        .post(&url)
        .json(&content)
        .send()
        .await
        .map_err(|e| e.to_string())?;
    let j = res.json::<serde_json::Value>().await.map_err(|e| e.to_string())?;
    Ok(j)
}

#[tauri::command]
async fn agent_chat(prompt: String) -> Result<serde_json::Value, String> {
    let req = ChatReq { prompt, model: None };
    let url = "http://127.0.0.1:8000/agent/chat";
    let client = reqwest::Client::new();
    let res = client
        .post(url)
        .json(&req)
        .send()
        .await
        .map_err(|e| e.to_string())?;
    let j = res.json::<serde_json::Value>().await.map_err(|e| e.to_string())?;
    Ok(j)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![fs_read, fs_write, agent_chat])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
