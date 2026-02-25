<script lang="ts">
  import { createEventDispatcher } from 'svelte'
  let url = ''
  const dispatch = createEventDispatcher()
  function open() {
    dispatch('open', { url })
  }
</script>

<div style="padding:8px; display:flex; gap:8px; align-items:center;">
  <input bind:value={url} placeholder="https://example.com" style="flex:1; padding:8px;" />
  <button on:click={open}>Open</button>
</div>
