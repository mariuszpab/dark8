<script lang="ts">
  import BrowserView from './components/BrowserView.svelte'
  import AgentPanel from './components/AgentPanel.svelte'
  import Toolbar from './components/Toolbar.svelte'
</script>

<main style="display:flex; height:100vh;">
  <div style="flex:1; display:flex; flex-direction:column;">
    <Toolbar />
    <BrowserView />
  </div>
  <aside style="width:360px; border-left:1px solid #ddd;">
    <AgentPanel />
  </aside>
</main>
