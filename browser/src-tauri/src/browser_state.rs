use std::sync::Mutex;

pub struct BrowserState {
    pub last_url: Mutex<Option<String>>,
}

impl Default for BrowserState {
    fn default() -> Self {
        Self {
            last_url: Mutex::new(None),
        }
    }
}
